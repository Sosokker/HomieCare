# import pytest
# from fastapi.testclient import TestClient
# from main import app

# @pytest.fixture
# def client():
#     with TestClient(app) as client:
#         yield client

# def test_list_cameras(client):
#     response = client.get("/camera/list")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)

# @pytest.mark.parametrize("camera_id", [1, 2, 3])
# def test_stream_video(client, camera_id):
#     response = client.get(f"/stream/{camera_id}")
#     assert response.status_code == 200
#     assert "multipart/x-mixed-replace; boundary=frame" in response.headers["content-type"]

# @pytest.mark.parametrize("camera_id", [1, 2, 3])
# def test_stream_action_video(client, camera_id):
#     response = client.get(f"/stream/action/{camera_id}")
#     assert response.status_code == 200
#     assert "multipart/x-mixed-replace; boundary=frame" in response.headers["content-type"]