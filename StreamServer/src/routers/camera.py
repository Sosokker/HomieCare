from datetime import timedelta

from fastapi import APIRouter, HTTPException

from query.camera import list_objects_with_timestamp, filter_objects_by_date

from config import VIDEO_BUCKET
from database import minio_client


router = APIRouter()


@router.get("/snapshot/{interval}", response_model=list[str])
async def get_snapshot(interval: str):
    """Return the list of URLs of camera snapshot within the specified interval. Supported intervals: 'today', 'week', 'month', 'all'"""
    try:
        res = filter_objects_by_date(list_objects_with_timestamp(), interval)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))

    if not res:
        raise HTTPException(status_code=404, detail="No snapshot found")

    return [minio_client.presigned_get_object(VIDEO_BUCKET, obj, expires=timedelta(days=1), response_headers={'response-content-type': 'image/jpeg'}) for obj in res]