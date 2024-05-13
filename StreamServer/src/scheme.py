"""
This file contains the Pydantic model for the weather data.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class IndoorDataBase(BaseModel):
    timestamp: Optional[datetime]
    indoor_temp: Optional[float]
    indoor_light: Optional[int]

    class Config:
        from_attributes = True


class OutdoorDataBase(BaseModel):
    timestamp: Optional[datetime]
    outdoor_temp: Optional[float]
    outdoor_feels_like: Optional[float]
    outdoor_pressure: Optional[int]
    outdoor_humidity: Optional[int]
    outdoor_weather: Optional[str]
    outdoor_description: Optional[str]
    outdoor_pm25: Optional[int]
    outdoor_pm10: Optional[int]

    class Config:
        from_attributes = True


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


class AverageOutdoorData(BaseModel):
    avg_outdoor_temp: Optional[float]
    avg_outdoor_feels_like: Optional[float]
    avg_outdoor_pressure: Optional[float]
    avg_outdoor_humidity: Optional[float]
    avg_outdoor_pm25: Optional[float]
    avg_outdoor_pm10: Optional[float]


class AverageIndoorData(BaseModel):
    avg_indoor_temp: Optional[float]
    avg_indoor_light: Optional[float]


class Camera(BaseModel):
    camera_id: int
    link: str
    status: bool = False


class PredictonTemperature(BaseModel):
    timestamp: Optional[datetime]
    indoor_temp: Optional[float]
    outdoor_temp: Optional[float]


class RecommendationData(BaseModel):
    timestamp: Optional[datetime]
    recommendation: Optional[str]
    status: Optional[str]


class HealthData(BaseModel):
    indoor_temp: float
    outdoor_temp: float
    outdoor_pm25: float
    outdoor_pm10: float
    outdoor_humidity: float


class ActionData(BaseModel):
    timestamp: Optional[datetime]
    action: Optional[str]