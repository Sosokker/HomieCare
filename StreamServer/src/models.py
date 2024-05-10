"""
This file contains the SQLAlchemy model for the weather data.
"""

from sqlalchemy import Column, Integer, Float, DateTime, Text
from sqlalchemy.orm import relationship

from database import Base


class WeatherData(Base):
    __tablename__ = "data"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    outdoor_temp = Column(Float)
    outdoor_feels_like = Column(Float)
    outdoor_pressure = Column(Integer)
    outdoor_humidity = Column(Integer)
    outdoor_weather = Column(Text)
    outdoor_description = Column(Text)
    outdoor_pm25 = Column(Integer)
    outdoor_pm10 = Column(Integer)
    indoor_temp = Column(Float)
    indoor_light = Column(Integer)


class PredictionData(Base):
    __tablename__ = "prediction"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    outdoor_temp = Column(Float)
    outdoor_feels_like = Column(Float)
    outdoor_pressure = Column(Integer)
    outdoor_humidity = Column(Integer)
    indoor_temp = Column(Float)


# class ActionData(Base):
#     __tablename__ = "action"

#     id = Column(Integer, primary_key=True)
#     timestamp = Column(DateTime)
#     action = Column(Text)
#     probability = Column(Float)
#     camera_id = Column(Integer)