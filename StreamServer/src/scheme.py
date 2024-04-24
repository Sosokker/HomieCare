"""
This file contains the Pydantic model for the weather data.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WeatherDataBase(BaseModel):
    timestamp: Optional[datetime]
    outdoor_temp: Optional[float]
    outdoor_feels_like: Optional[float]
    outdoor_pressure: Optional[int]
    outdoor_humidity: Optional[int]
    outdoor_weather: Optional[str]
    outdoor_description: Optional[str]
    outdoor_pm25: Optional[int]
    outdoor_pm10: Optional[int]
    indoor_temp: Optional[float]
    indoor_light: Optional[int]

    class Config:
        from_attributes = True

class Camera(BaseModel):
    camera_id: int
    link: str