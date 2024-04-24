from fastapi import APIRouter, HTTPException
from scheme import Camera
from typing import List

router = APIRouter()

cameras: List[Camera] = []

@router.post("/add_camera", response_model=dict)
async def add_camera(rtsp_link: str):
    if rtsp_link:
        camera = Camera(rtsp_link=rtsp_link)
        cameras.append(camera)
        return {"message": "Camera added successfully"}
    else:
        raise HTTPException(status_code=400, detail="Invalid RTSP link")

@router.get("/stream_video")
async def stream_video():
    # TODO: Implement video streaming
    return {"message": "Camera disconnected successfully"}

@router.delete("/disconnect_camera/{camera_id}", response_model=dict)
async def disconnect_camera(camera_id: int):
    if 0 <= camera_id < len(cameras):
        del cameras[camera_id]
        return {"message": "Camera disconnected successfully"}
    else:
        raise HTTPException(status_code=404, detail="Camera not found")