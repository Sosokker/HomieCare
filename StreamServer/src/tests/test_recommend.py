import pytest
from fastapi.testclient import TestClient
from main import app
from scheme import HealthData

client = TestClient(app)

@pytest.fixture
def sample_health_data():
    return HealthData(
        indoor_temp=25,
        outdoor_temp=30,
        outdoor_pm25=40,
        outdoor_pm10=60,
        outdoor_humidity=30
    )

def test_get_health_recommendation(sample_health_data):
    response = client.post("/recommend/recommendation/", json=sample_health_data.model_dump())
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    for item in response.json():
        assert "timestamp" in item
        assert "recommendation" in item
        assert "status" in item
