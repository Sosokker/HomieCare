from datetime import datetime
from fastapi import APIRouter, HTTPException

from scheme import RecommendationData, HealthData

router = APIRouter()

@router.post("/recommendation/", response_model=list[RecommendationData])
async def get_health_recommendation(data: HealthData):
    recommendation = []
    current_time = datetime.now()

    INDOOR_HIGH_TEMP = 30
    INDOOR_LOW_TEMP = 20
    INDOOR_VERY_LOW_TEMP = 15
    OUTDOOR_HIGH_TEMP = 35
    OUTDOOR_LOW_TEMP = 10
    PM25_HIGH = 50
    PM25_VERY_HIGH = 100
    PM10_HIGH = 50
    PM10_VERY_HIGH = 100

    if data.indoor_temp > INDOOR_HIGH_TEMP:
        recommendation.append(RecommendationData(timestamp=current_time,
                                                 recommendation="It's quite warm indoors. Consider using a fan or air conditioning.",
                                                 status="warning"))
    elif data.indoor_temp < INDOOR_LOW_TEMP:
        recommendation.append(RecommendationData(timestamp=current_time,
                                                 recommendation="Indoor temperature is low. Wear warm clothing or adjust heating.",
                                                 status="warning"))
    elif data.indoor_temp < INDOOR_VERY_LOW_TEMP:
        recommendation.append(RecommendationData(timestamp=current_time,
                                                recommendation="Indoor temperature is very low. Take measures to stay warm.",
                                                status="danger"))

    if data.outdoor_temp > OUTDOOR_HIGH_TEMP:
        recommendation.append(RecommendationData(timestamp=current_time,
                                                recommendation="The outdoor temperature is high. Avoid prolonged outdoor activities.",
                                                status="warning"))
    elif data.outdoor_temp < OUTDOOR_LOW_TEMP:
        recommendation.append(RecommendationData(timestamp=current_time,
                                                recommendation="It's very cold outside. Dress warmly and limit outdoor exposure.",
                                                status="danger"))

    if data.outdoor_pm25 > PM25_HIGH:
        recommendation.append(RecommendationData(timestamp=current_time,
                                                recommendation="The PM2.5 levels are elevated outdoors. Limit outdoor exposure.",
                                                status="warning"))
    elif data.outdoor_pm25 > PM25_VERY_HIGH:
        recommendation.append(RecommendationData(timestamp=current_time,
                                                recommendation="High PM2.5 levels detected. Avoid outdoor activities in polluted areas.",
                                                status="danger"))

    if data.outdoor_pm10 > PM10_HIGH:
        recommendation.append(RecommendationData(timestamp=current_time,
                                                recommendation="The PM10 levels are high outdoors. Avoid areas with heavy pollution.",
                                                status="warning"))
    elif data.outdoor_pm10 > PM10_VERY_HIGH:
        recommendation.append(RecommendationData(timestamp=current_time,
                                                recommendation="High PM10 levels detected. Consider staying indoors or using masks.",
                                                status="danger"))

    if not recommendation:
        recommendation.append(RecommendationData(timestamp=current_time,
                                                recommendation="Everything good ;).",
                                                status="normal"))

    return recommendation