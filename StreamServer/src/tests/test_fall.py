import pytest
from fastapi.testclient import TestClient
from main import app
from models import ActionData
from analytic.action.action_model import ActionModel
from database import SessionLocal

client = TestClient(app)
action_model = ActionModel()


def test_fall_detection_and_notification():
    action_model.IS_FALL_DOWN = True
    response = client.get("/camera/action/test")

    assert response.status_code == 200


