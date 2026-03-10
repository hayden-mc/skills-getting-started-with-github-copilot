from urllib.parse import quote

from src.app import activities


def unregister_path(activity_name: str) -> str:
    encoded_activity = quote(activity_name, safe="")
    return f"/activities/{encoded_activity}/participants"


def test_unregister_removes_participant(client):
    activity_name = "Chess Club"
    email = activities[activity_name]["participants"][0]
    before_count = len(activities[activity_name]["participants"])

    response = client.delete(unregister_path(activity_name), params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert len(activities[activity_name]["participants"]) == before_count - 1
    assert email not in activities[activity_name]["participants"]


def test_unregister_rejects_missing_activity(client):
    response = client.delete(unregister_path("Unknown Club"), params={"email": "new@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_rejects_email_not_signed_up(client):
    response = client.delete(
        unregister_path("Chess Club"),
        params={"email": "not-signed-up@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_only_removes_requested_participant(client):
    activity_name = "Programming Class"
    email_to_remove = activities[activity_name]["participants"][0]
    email_to_keep = activities[activity_name]["participants"][1]

    response = client.delete(
        unregister_path(activity_name),
        params={"email": email_to_remove},
    )

    assert response.status_code == 200
    assert email_to_remove not in activities[activity_name]["participants"]
    assert email_to_keep in activities[activity_name]["participants"]
