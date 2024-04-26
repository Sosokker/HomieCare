from sqlalchemy import func
from sqlalchemy.orm import Session

from database import engine, SessionLocal, Base
from scheme import WeatherDataBase, IndoorDataBase, OutdoorDataBase, AverageIndoorData, AverageOutdoorData
from query.weather import (get_weather_data, get_last_n_day_data, get_indoor_data, get_outdoor_data,
                           get_average_outdoor_data_last_n_day, get_average_indoor_data_last_n_day)

from fastapi import APIRouter, Depends, HTTPException

Base.metadata.create_all(bind=engine)

router = APIRouter()

#Dependency
def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[WeatherDataBase])
async def get_latest_weather_data(db: Session = Depends(get_db)):
    weather_data = get_weather_data(db)
    if not weather_data:
        raise HTTPException(status_code=404, detail="Weather data not found")
    return weather_data


@router.get("/{days}", response_model=list[WeatherDataBase])
async def get_weather_data_last_n_days(days: int, db: Session = Depends(get_db)):
    weather_data = get_last_n_day_data(db, days)
    if not weather_data:
        raise HTTPException(status_code=404, detail=f"Weather data for the last {days} days not found")
    return weather_data


@router.get("/indoor/{days}", response_model=list[IndoorDataBase])
async def get_indoor_data_last_n_days(days: int, db: Session = Depends(get_db)):
    indoor_data = get_indoor_data(db, days)
    if not indoor_data:
        raise HTTPException(status_code=404, detail=f"Indoor data for the last {days} days not found")
    return indoor_data

@router.get("/outdoor/{days}", response_model=list[OutdoorDataBase])
async def get_outdoor_data_last_n_days(days: int, db: Session = Depends(get_db)):
    outdoor_data = get_outdoor_data(db, days)
    if not outdoor_data:
        raise HTTPException(status_code=404, detail="Outdoor data not found")
    return outdoor_data


@router.get("/average/outdoor/{days}", response_model=AverageOutdoorData)
async def get_average_outdoor_data(days: int, db: Session = Depends(get_db)):
    average_outdoor_data = get_average_outdoor_data_last_n_day(db, days)
    print("HERERERERERE ", average_outdoor_data)
    if not average_outdoor_data:
        raise HTTPException(status_code=404, detail=f"Average outdoor data for the last {days} days not found")
    
    average_outdoor_model = AverageOutdoorData(
    avg_outdoor_temp=average_outdoor_data[0],
    avg_outdoor_feels_like=average_outdoor_data[1],
    avg_outdoor_pressure=average_outdoor_data[2],
    avg_outdoor_humidity=average_outdoor_data[3],
    avg_outdoor_pm25=average_outdoor_data[4],
    avg_outdoor_pm10=average_outdoor_data[5]
)
    
    return average_outdoor_model


@router.get("/average/indoor/{days}", response_model=AverageIndoorData)
async def get_average_indoor_data(days: int, db: Session = Depends(get_db)):
    average_indoor_data = get_average_indoor_data_last_n_day(db, days)
    if not average_indoor_data:
        raise HTTPException(status_code=404, detail=f"Average indoor data for the last {days} days not found")
    
    average_indoor_model = AverageIndoorData(
        avg_indoor_temp=average_indoor_data[0],
        avg_indoor_light=average_indoor_data[1]
    )

    return average_indoor_model