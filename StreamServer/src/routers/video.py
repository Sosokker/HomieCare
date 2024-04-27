import cv2
import time

from cv2 import VideoCapture, imencode
from contextlib import asynccontextmanager
from datetime import datetime
from threading import Thread

from fastapi import APIRouter, BackgroundTasks, FastAPI, HTTPException
from fastapi.responses import StreamingResponse

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from database import minio_client
from config import TEMP_VIDEO_FILE, VIDEO_BUCKET
from scheme import Camera
from utils import save_to_config, read_cameras_from_config

from analytic.action.action_model import generate_action_model_frame


jobstores = {
'default': MemoryJobStore()
}
scheduler = AsyncIOScheduler(jobstores=jobstores, timezone='Asia/Bangkok')

@asynccontextmanager
async def lifespan(application: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()

router = APIRouter()

cameras: list[Camera] = read_cameras_from_config('config.json')

# --- UTILITY FUNCTIONS ---

def generate_camera_id() -> int:
    if not cameras:
        return 1
    cameras.sort(key=lambda x: x.camera_id)
    return cameras[-1].camera_id + 1

def upload_to_minio(camera_id):
    current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    temp_file_name = f"camera_{camera_id}_{current_time}.avi"
    minio_client.fput_object(VIDEO_BUCKET, temp_file_name, f"{TEMP_VIDEO_FILE}_{camera_id}.avi")

# --- BACKGROUND SCHEDULER ---

# TODO: Save video to Minio

@scheduler.scheduled_job('interval', seconds=60)
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
        cap.release()
    save_to_config(key="cameras", value=cameras)


# --- ROUTER ENDPOINTS ---

@router.post("/add", response_model=dict)
async def add_camera(link: str):
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
    return cameras


@router.get("/stream/{camera_id}")
async def stream_video(camera_id: int) -> StreamingResponse:
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
    camera = next((c for c in cameras if c.camera_id == camera_id), None)
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    
    if not camera.status:
        raise HTTPException(status_code=400, detail="Camera is not available")
    
    cap = VideoCapture(camera.link)
    if not cap.isOpened():
        raise HTTPException(status_code=404, detail="Camera is closed or not available")

    return StreamingResponse(generate_action_model_frame(camera.link), media_type="multipart/x-mixed-replace; boundary=frame")


@router.delete("/remove/{camera_id}", response_model=dict)
async def disconnect_camera(camera_id: int) -> dict:
    global video_writer
    for camera in cameras:
        if camera.camera_id == camera_id:
            cameras.remove(camera)
            save_to_config(key="cameras", value=cameras)
            return {"message": f"Camera {camera_id} disconnected successfully"}
    raise HTTPException(status_code=404, detail=f"Camera {camera_id} not found")