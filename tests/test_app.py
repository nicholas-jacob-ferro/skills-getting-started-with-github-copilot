import pytest

from fastapi.testclient import TestClient
import src.app as app_module

@pytest.fixture(autouse=True)
def reset_activities():
    app_module._reset_activities()

client = TestClient(app_module.app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_and_unregister():
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Ensure not already signed up
    client.post(f"/activities/{activity}/unregister", params={"email": email})
    # Sign up
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Duplicate signup should fail
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 400
    # Unregister
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 200
    assert f"Unregistered {email}" in response.json()["message"]
    # Unregister again should fail (either 400 or 404 is acceptable)
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code in (400, 404)

def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup", params={"email": "nobody@mergington.edu"})
    assert response.status_code == 404

def test_unregister_activity_not_found():
    response = client.post("/activities/Nonexistent/unregister", params={"email": "nobody@mergington.edu"})
    assert response.status_code == 404
