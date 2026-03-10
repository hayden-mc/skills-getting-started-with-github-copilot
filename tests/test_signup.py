from urllib.parse import quote

from src.app import activities


def signup_path(activity_name: str) -> str:
    encoded_activity = quote(activity_name, safe="")
    return f"/activities/{encoded_activity}/signup"


def test_signup_adds_new_participant(client):
    activity_name = "Chess Club"
    email = "alex@mergington.edu"
    before_count = len(activities[activity_name]["participants"])

    response = client.post(signup_path(activity_name), params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert len(activities[activity_name]["participants"]) == before_count + 1
    assert email in activities[activity_name]["participants"]


def test_signup_rejects_missing_activity(client):
    response = client.post(signup_path("Unknown Club"), params={"email": "new@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_rejects_duplicate_participant(client):
    activity_name = "Chess Club"
    email = activities[activity_name]["participants"][0]

    response = client.post(signup_path(activity_name), params={"email": email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_rejects_when_activity_is_full(client):
    activity_name = "Robotics Club"
    email = "overflow@mergington.edu"
    activity = activities[activity_name]
    remaining_slots = activity["max_participants"] - len(activity["participants"])

    for index in range(remaining_slots):
        activity["participants"].append(f"filled{index}@mergington.edu")

    response = client.post(signup_path(activity_name), params={"email": email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"
    assert email not in activity["participants"]
