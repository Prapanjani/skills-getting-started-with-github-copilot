from fastapi.testclient import TestClient
from src import app as app_module


client = TestClient(app_module)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Basic expected activity
    assert "Chess Club" in data


def test_signup_duplicate_and_unregister_flow():
    activity = "Chess Club"
    email = "testuser@example.com"

    # Ensure clean state: attempt to delete if present
    client.delete(f"/activities/{activity}/signup?email={email}")

    # Sign up first time -> success
    resp1 = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp1.status_code == 200
    assert f"Signed up {email}" in resp1.json().get("message", "")

    # Sign up second time -> should be rejected (duplicate)
    resp2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp2.status_code == 400

    # Verify participant shows up in activities
    resp3 = client.get("/activities")
    participants = resp3.json()[activity]["participants"]
    assert email in participants

    # Unregister -> success
    resp4 = client.delete(f"/activities/{activity}/signup?email={email}")
    assert resp4.status_code == 200
    assert f"Unregistered {email}" in resp4.json().get("message", "")

    # Unregister again -> not found
    resp5 = client.delete(f"/activities/{activity}/signup?email={email}")
    assert resp5.status_code == 404
