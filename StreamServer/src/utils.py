"""
This module contains utility functions that are used in the project.
"""

import re
import json

from typing import Never
from pydantic import BaseModel
from scheme import Camera


def serialize_value(value) -> any:
    """Serialize the given value to a JSON serializable value."""
    if isinstance(value, list):
        if all(isinstance(item, BaseModel) for item in value):
            return [item.dict() for item in value]
        else:
            return value
    elif isinstance(value, BaseModel):
        return value.dict()
    else:
        return value


def save_to_config(key, value) -> None:
    """Save the given key-value pair to the config file."""
    try:
        with open('config.json', 'r') as file:
            config_data = json.load(file)
    except:
        config_data = {}
    config_data[key] = serialize_value(value)

    with open('config.json', 'w') as file:
        json.dump(config_data, file, indent=4)


def read_cameras_from_config(file_path) -> list[Camera] | list[Never]:
    """Read the cameras data from the config file."""
    try:
        with open(file_path, 'r') as file:
            config_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    cameras_data = config_data.get('cameras', [])
    cameras = [Camera(**cam_data) for cam_data in cameras_data]

    return cameras


def video_url_validation(url: str) -> bool:
    """Validate if the given URL is a rtsp/rtmp URL or not."""
    rtmp_pattern = r'^rtmp://.*$'
    rtsp_pattern = r'^rtsp://.*$'

    if re.match(rtmp_pattern, url) or re.match(rtsp_pattern, url):
        return True
    else:
        return False