from src.app import activities

REQUIRED_ACTIVITY_KEYS = {"description", "schedule", "max_participants", "participants"}


def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_seeded_activities(client):
    response = client.get("/activities")
    payload = response.json()

    assert response.status_code == 200
    assert set(payload.keys()) == set(activities.keys())


def test_get_activities_returns_expected_activity_shape(client):
    response = client.get("/activities")
    payload = response.json()

    assert response.status_code == 200

    for activity_details in payload.values():
        assert REQUIRED_ACTIVITY_KEYS.issubset(activity_details.keys())
        assert isinstance(activity_details["description"], str)
        assert isinstance(activity_details["schedule"], str)
        assert isinstance(activity_details["max_participants"], int)
        assert isinstance(activity_details["participants"], list)


def test_get_activities_returns_participant_emails(client):
    response = client.get("/activities")
    payload = response.json()

    assert response.status_code == 200

    for activity_details in payload.values():
        participants = activity_details["participants"]
        assert all(isinstance(email, str) and "@" in email for email in participants)
