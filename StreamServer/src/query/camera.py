from datetime import datetime, timedelta
from minio.error import InvalidResponseError
from pytz import UTC

from config import VIDEO_BUCKET
from database import minio_client


def list_objects_with_timestamp(bucket_name: str = VIDEO_BUCKET) -> list[tuple[str, datetime]]:
    """List objects in the specified bucket with their last modified timestamp"""
    try:
        objects = minio_client.list_objects(bucket_name, recursive=True)
        jpeg_objects = [(obj.object_name, obj.last_modified) for obj in objects if obj.object_name.endswith('.jpg') or obj.object_name.endswith('.jpeg')]
        return jpeg_objects
    except InvalidResponseError as err:
        print(err)
        return []


def filter_objects_by_date(objects_with_timestamp: list, interval: str) -> list:
    """List objects with timestamp within the specified interval. Supported intervals: 'today', 'week', 'month', 'all'"""
    now_datetime = datetime.now(UTC)

    if interval == "today":
        start_datetime = now_datetime - timedelta(days=1)
    elif interval == "week":
        start_datetime = now_datetime - timedelta(days=7)
    elif interval == "month":
        start_datetime = now_datetime - timedelta(days=30)
    elif interval == "all":
        start_datetime = datetime.min.replace(tzinfo=UTC)  # Consider all dates
    else:
        raise ValueError("Invalid interval. Supported intervals: 'today', 'week', 'month', 'all'")

    return [obj for obj, timestamp in objects_with_timestamp if start_datetime <= timestamp <= now_datetime]
