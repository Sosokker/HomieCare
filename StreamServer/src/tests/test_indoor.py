import pytest
from fastapi.testclient import TestClient
from routers.prediction import _fetch_data_from_api
from database import SessionLocal
from main import app
from datetime import datetime
from models import PredictionData

client = TestClient(app)


@pytest.fixture
def sample_weather_data():
    # Sample weather data for testing
    return {
        "list": [
            {
                "dt": datetime.now().timestamp(),
                "main": {
                    "temp": 25,
                    "feels_like": 26,
                    "pressure": 1010,
                    "humidity": 50
                }
            }
        ]
    }

def test_get_tomorrow_indoor_temp():
    db_session = SessionLocal()

    response = client.get("/weather/indoor/predict/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    for item in response.json():
        assert "timestamp" in item
        assert "indoor_temp" in item
        assert "outdoor_temp" in item

    # Clean up dependency overrides
    app.dependency_overrides.clear()
