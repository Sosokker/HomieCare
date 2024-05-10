from datetime import datetime, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from models import PredictionData


def get_temp_prediction_data(session: Session):
    """Get indoor temperature prediction for the next five days"""
    current_time = datetime.now()
    limit_day = current_time + timedelta(days=5)

    return session.query(
        PredictionData.timestamp, PredictionData.indoor_temp
    ).filter(
        PredictionData.timestamp >= current_time,
        PredictionData.timestamp < limit_day
    ).order_by(PredictionData.timestamp.desc()).all()


def get_feature_prediction_data(session: Session):
    """Get all features used to predict indoor temperature for the next five days"""
    current_time = datetime.now()
    limit_day = current_time + timedelta(days=5)

    return session.query(
        PredictionData.timestamp, PredictionData.outdoor_temp, PredictionData.outdoor_feels_like,
        PredictionData.outdoor_pressure, PredictionData.outdoor_humidity
    ).filter(
        PredictionData.timestamp >= current_time,
        PredictionData.timestamp < limit_day
    ).order_by(PredictionData.timestamp.desc()).all()