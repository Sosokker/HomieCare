import os
import cv2
import time
from fastapi.websockets import WebSocketState
import httpx

from cv2 import VideoCapture, imencode
from contextlib import asynccontextmanager
from datetime import datetime
from threading import Thread
from database import SessionLocal

from fastapi import APIRouter, Depends, FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from database import minio_client
from config import VIDEO_BUCKET, LINE_NOTIFY_TOKEN
from scheme import Camera
from utils import save_to_config, read_cameras_from_config
from models import ActionData

from analytic.action.action_model import ActionModel


jobstores = {
'default': MemoryJobStore()
}
scheduler = AsyncIOScheduler(jobstores=jobstores, timezone='Asia/Bangkok')

#Dependency
def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally:
        db.close()

cameras: list[Camera] = read_cameras_from_config('config.json')

# ------ Action Model ------
action_model = ActionModel()

def run_action_model_continuously():
    while True:
        for camera in cameras:
            if camera.status:
                action_model.run_action_model(camera.link)
        time.sleep(30)

action_thread = Thread(target=run_action_model_continuously, daemon=True)

@asynccontextmanager
async def lifespan(application: FastAPI):
    scheduler.start()
    action_thread.start()
    yield
    scheduler.shutdown()
    action_thread.join()

router = APIRouter()

# --- UTILITY FUNCTIONS ---

def generate_camera_id() -> int:
    if not cameras:
        return 1
    cameras.sort(key=lambda x: x.camera_id)
    return cameras[-1].camera_id + 1

def upload_to_minio(cap: VideoCapture, camera_id: int):
    """Upload Image to Minio Bucket"""
    current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    image_name = f"{camera_id}_{current_time}.jpg"
    
    ret, frame = cap.read()
    if not ret:
        raise ValueError("Failed to read frame from VideoCapture")
    
    success = cv2.imwrite(image_name, frame)
    if not success:
        raise ValueError("Failed to write frame as JPEG image")
    
    try:
        with open(image_name, "rb") as image_file:
            minio_client.put_object(VIDEO_BUCKET, image_name, image_file, length=os.path.getsize(image_name))
    except Exception as e:
        raise RuntimeError(f"Failed to upload image to Minio bucket: {e}")
    finally:
        os.remove(image_name)

# --- BACKGROUND SCHEDULER ---


@scheduler.scheduled_job('interval', seconds=30, max_instances=2)
def check_camera_status():
    """
    Check if the camera is available or not
    If the camera is available, set status to True
    else set status to False
    """
    global cameras
    for camera in cameras:
        cap = VideoCapture(camera.link)
        if not cap.isOpened() or cap is None:
            camera.status = False
        else:
            camera.status = True
            upload_to_minio(cap, camera.camera_id)
        cap.release()
    save_to_config(key="cameras", value=cameras)

@scheduler.scheduled_job('interval', seconds=10)
def add_action_to_database():
    """Add action data to the database"""
    global cameras
    for camera in cameras:
        if camera.status:
            try:
                for i in range(10):
                    action = ActionData(action=action_model.ACTION_LIST.pop(i), timestamp=datetime.now())
                    db = SessionLocal()
                    db.add(action)
                    db.commit()
                    db.close()
                action_model.ACTION_LIST.clear()
            except Exception as e:
                print(f"Failed to add action data to database: {e}")
                continue

@scheduler.scheduled_job('interval', seconds=10)
def check_falldown_action():
    """If action Fall Down is detected, notify the user"""
    if action_model.IS_FALL_DOWN:
        # send post to https://notify-api.line.me/api/notify
        # Authorization: Bearer use LINE_NOTIFY_TOKEN (ChannelAccessToken)
        httpx.post("https://notify-api.line.me/api/notify", headers={"Authorization": f"Bearer {LINE_NOTIFY_TOKEN}"}, data={"message": "Fall Down detected!"})
        action_model.IS_FALL_DOWN = False

# --- ROUTER ENDPOINTS ---

@router.post("/add", response_model=dict)
async def add_camera(link: str):
    """Add a new camera to the system."""
    if link:
        id = generate_camera_id()
        camera = Camera(camera_id=id, link=link, status=False)
        cameras.append(camera)
        save_to_config(key="cameras", value=cameras)
        return {"message": "Camera added successfully", "camera_id": id}
    else:
        raise HTTPException(status_code=400, detail="Invalid RTSP link")


@router.get("/list", response_model=list[Camera])
async def list_cameras() -> list[Camera]:
    """List all available cameras."""
    return cameras


@router.get("/stream/{camera_id}")
async def stream_video(camera_id: int) -> StreamingResponse:
    """Stream video from the camera with the given camera_id."""
    camera = next((c for c in cameras if c.camera_id == camera_id), None)
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    
    if not camera.status:
        raise HTTPException(status_code=400, detail="Camera is not available")
    
    cap = VideoCapture(camera.link)
    if not cap.isOpened():
        raise HTTPException(status_code=404, detail="Camera is closed or not available")
    
    def generate_frames():
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                raise HTTPException(status_code=500, detail="Connection to camera lost")
            ret, buffer = imencode('.jpg', frame)
            if not ret:
                raise HTTPException(status_code=500, detail="Connection to camera lost")
            yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n'

    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")


@router.get("/stream/action/{camera_id}")
async def stream_action_video(camera_id: int) -> StreamingResponse:
    """Stream video from the camera with the given camera_id with action model."""
    camera = next((c for c in cameras if c.camera_id == camera_id), None)
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    
    if not camera.status:
        raise HTTPException(status_code=400, detail="Camera is not available")
    
    cap = VideoCapture(camera.link)
    if not cap.isOpened():
        raise HTTPException(status_code=404, detail="Camera is closed or not available")

    return StreamingResponse(action_model.generate_action_model_frame(camera.link), media_type="multipart/x-mixed-replace; boundary=frame")


@router.delete("/remove/{camera_id}", response_model=dict)
async def disconnect_camera(camera_id: int) -> dict:
    """Disconnect the camera with the given camera_id."""
    global video_writer
    for camera in cameras:
        if camera.camera_id == camera_id:
            cameras.remove(camera)
            save_to_config(key="cameras", value=cameras)
            return {"message": f"Camera {camera_id} disconnected successfully"}
    raise HTTPException(status_code=404, detail=f"Camera {camera_id} not found")


@router.websocket("/ws/{camera_id}")
async def websocket_endpoint(camera_id: int, websocket: WebSocket):
    """Stream video from the camera with the given camera_id using WebSocket."""
    camera = next((c for c in cameras if c.camera_id == camera_id), None)
    if not camera:
        await websocket.close(code=1000)
        return
    
    if not camera.status:
        await websocket.close(code=1000)
        return
    
    cap = VideoCapture(camera.link)
    if not cap.isOpened():
        await websocket.close(code=1000)
        return
    
    try:
        await websocket.accept()

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            ret, buffer = imencode('.png', frame)
            if not ret:
                break
                
            if websocket.client_state != WebSocketState.DISCONNECTED:
                await websocket.send_bytes(buffer.tobytes())
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(f"Error sending frame: {e}")
    finally:
        cap.release()
        await websocket.close(code=1000)

@router.get("/action/test", response_model=bool)
def test_notification():
    """Test notification by sending a POST request to LINE Notify API"""
    if action_model.IS_FALL_DOWN:
        return True
    return False