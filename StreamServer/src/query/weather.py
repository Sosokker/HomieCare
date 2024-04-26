from datetime import datetime, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from models import WeatherData


def _get_weather_data_query(session: Session):
    return session.query(
        WeatherData.timestamp, WeatherData.outdoor_temp, WeatherData.outdoor_feels_like,
        WeatherData.outdoor_pressure, WeatherData.outdoor_humidity, WeatherData.outdoor_weather,
        WeatherData.outdoor_description, WeatherData.outdoor_pm25, WeatherData.outdoor_pm10,
        WeatherData.indoor_temp, WeatherData.indoor_light
    ).order_by(WeatherData.timestamp.desc())

def get_weather_data(session: Session):
    """
    Get all weather data from the database.
    """
    return _get_weather_data_query(session).all()

def get_last_n_day_data(session: Session, n: int):
    """
    Get the weather data for the last n days from the database.
    """
    start_date = datetime.now() - timedelta(days=n)
    return _get_weather_data_query(session).filter(WeatherData.timestamp >= start_date).all()

def get_indoor_data(session: Session, limit: int = 10):
    """
    Get the latest indoor data from the database.
    """
    return session.query(
        WeatherData.timestamp, WeatherData.indoor_temp, WeatherData.indoor_light
    ).order_by(WeatherData.timestamp.desc()).limit(limit).all()

def get_outdoor_data(session: Session, limit: int = 10):
    """
    Get the latest outdoor data from the database.
    """
    return session.query(
        WeatherData.timestamp, WeatherData.outdoor_temp, WeatherData.outdoor_feels_like,
        WeatherData.outdoor_pressure, WeatherData.outdoor_humidity, WeatherData.outdoor_weather,
        WeatherData.outdoor_description, WeatherData.outdoor_pm25, WeatherData.outdoor_pm10
    ).order_by(WeatherData.timestamp.desc()).limit(limit).all()

def _get_average_data_query(session: Session, columns, n: int):
    start_date = datetime.now() - timedelta(days=n)
    return session.query(*columns).filter(WeatherData.timestamp >= start_date)

def get_average_outdoor_data_last_n_day(session: Session, n: int):
    """
    Get the average outdoor data for the last n days from the database.
    """
    columns = [
        func.avg(WeatherData.outdoor_temp), func.avg(WeatherData.outdoor_feels_like),
        func.avg(WeatherData.outdoor_pressure), func.avg(WeatherData.outdoor_humidity),
        func.avg(WeatherData.outdoor_pm25), func.avg(WeatherData.outdoor_pm10)
    ]
    return _get_average_data_query(session, columns, n).first()

def get_average_indoor_data_last_n_day(session: Session, n: int):
    """
    Get the average indoor data for the last n days from the database.
    """
    columns = [func.avg(WeatherData.indoor_temp), func.avg(WeatherData.indoor_light)]
    return _get_average_data_query(session, columns, n).first()