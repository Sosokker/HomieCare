import httpx

from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException, status

from analytic.health.indoor_model import XgboostIndoorModel
from config import WEATHER_API_KEY, LAT, LON
from database import SessionLocal
from scheme import PredictonTemperature
from models import PredictionData
from query.prediction import get_temp_prediction_data, get_feature_prediction_data

router = APIRouter()


#Dependency
def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally:
        db.close()

# Load prediction data -> FOUND -> Return
# NOT FOUND
# Try load data from database -> Load future data from database ->  predict -> RETURN
#                             -> Not found -> Load data from api -> Predict/Save to database -> RETURN


def _fetch_data_from_api() -> dict:
    # api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API key}
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={LAT}&lon={LON}&units=metric&appid={WEATHER_API_KEY}"
    response = httpx.get(url)
    return response.json()


@router.get("/indoor/predict/", response_model=list[PredictonTemperature])
async def get_tomorrow_indoor_temp(db: Session = Depends(get_db)):
    result = get_temp_prediction_data(db)
    if not result:
        features = get_feature_prediction_data(db)
        xgboost = XgboostIndoorModel()
        if not features:
            datas = _fetch_data_from_api()
            # Save to database
            if datas:
                results = []
                for data in datas['list']:
                    ts = datetime.fromtimestamp(data['dt'])
                    data = data['main']
                    features = [data['temp'], data['feels_like'], data['pressure'], data['humidity']]
                    result = xgboost.predict(features)
                    results.append(PredictonTemperature(indoor_temp=result, timestamp=ts, outdoor_temp=data['temp']))
                    new_data_entry = PredictionData(
                        timestamp=ts,
                        indoor_temp=result,
                        outdoor_temp=data['temp'],
                        outdoor_feels_like=data['feels_like'],
                        outdoor_pressure=data['pressure'],
                        outdoor_humidity=data['humidity']
                    )
                    db.add(new_data_entry)
                    db.commit()
                result = results
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to fetch data from API"
                )
        else:
            for i in features:
                indoor = xgboost.predict([i.outdoor_temp, i.outdoor_feels_like, i.outdoor_pressure, i.outdoor_humidity])
                result.append(PredictonTemperature(timestamp=i.timestamp, indoor_temp=indoor, outdoor_temp=i.outdoor_temp))
    return result
