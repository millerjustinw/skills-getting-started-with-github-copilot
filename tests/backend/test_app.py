from fastapi.testclient import TestClient

from src.app import activities, app

client = TestClient(app)


def test_get_activities_returns_all_activities():
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert activity_name in payload
    assert "participants" in payload[activity_name]


def test_signup_for_activity_adds_participant():
    # Arrange
    activity_name = "Programming Class"
    email = "test_student@mergington.edu"
    original_participants = activities[activity_name]["participants"][:]

    try:
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 200
        assert email in activities[activity_name]["participants"]
        assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    finally:
        activities[activity_name]["participants"] = original_participants


def test_unregister_participant_removes_email():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    original_participants = activities[activity_name]["participants"][:]

    try:
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        assert response.status_code == 200
        assert email not in activities[activity_name]["participants"]
        assert response.json()["message"] == f"Removed {email} from {activity_name}"
    finally:
        activities[activity_name]["participants"] = original_participants
