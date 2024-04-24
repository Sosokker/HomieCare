from cv2 import VideoCapture, imencode

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from scheme import Camera
from utils import save_to_config, read_cameras_from_config


router = APIRouter()

cameras: list[Camera] = read_cameras_from_config('config.json')

# --- UTILITY FUNCTIONS ---

def generate_camera_id() -> int:
    if not cameras:
        return 1
    cameras.sort(key=lambda x: x.camera_id)
    return cameras[-1].camera_id + 1

# --- ROUTER ENDPOINTS ---

@router.post("/add", response_model=dict)
async def add_camera(rtsp_link: str):
    if rtsp_link:
        id = generate_camera_id()
        camera = Camera(camera_id=id, link=rtsp_link)
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
    available_cameras = [camera.camera_id for camera in cameras]
    if camera_id in available_cameras:
        for camera in cameras:
            if camera.camera_id == camera_id:
                link = camera.link
                break
        cap = VideoCapture(link)
        if not cap.isOpened():
            raise HTTPException(status_code=404, detail="Camera is closed or not available")
        
        def generate_frames():
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                ret, buffer = imencode('.jpg', frame)
                if not ret:
                    break
                yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n'

        return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")
    else:
        raise HTTPException(status_code=404, detail="No cameras available")


@router.delete("/remove/{camera_id}", response_model=dict)
async def disconnect_camera(camera_id: int) -> dict:
    for camera in cameras:
        if camera.camera_id == camera_id:
            cameras.remove(camera)
            save_to_config(key="cameras", value=cameras)
            return {"message": f"Camera {camera_id} disconnected successfully"}
    raise HTTPException(status_code=404, detail=f"Camera {camera_id} not found")