from src import app as app_module


class TestActivities:
    def test_get_activities_returns_activity_data(self, client):
        # Arrange
        expected_activity = app_module.activities["Chess Club"]

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        assert response.json()["Chess Club"] == expected_activity

    def test_signup_adds_student_to_activity(self, client):
        # Arrange
        activity = "Art Club"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 200
        assert email in app_module.activities[activity]["participants"]
        assert response.json()["message"] == f"Signed up {email} for {activity}"

    def test_signup_rejects_duplicate_student(self, client):
        # Arrange
        activity = "Art Club"
        email = "student@mergington.edu"
        client.post(f"/activities/{activity}/signup", params={"email": email})

        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up for this activity"
        assert app_module.activities[activity]["participants"].count(email) == 1

    def test_signup_rejects_unknown_activity(self, client):
        # Arrange
        activity = "Unknown Club"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_unregister_removes_student_from_activity(self, client):
        # Arrange
        activity = "Art Club"
        email = "student@mergington.edu"
        client.post(f"/activities/{activity}/signup", params={"email": email})

        # Act
        response = client.delete(
            f"/activities/{activity}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 200
        assert email not in app_module.activities[activity]["participants"]
        assert response.json()["message"] == f"Unregistered {email} from {activity}"

    def test_unregister_rejects_unknown_activity(self, client):
        # Arrange
        activity = "Unknown Club"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_unregister_rejects_student_not_signed_up(self, client):
        # Arrange
        activity = "Art Club"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Student is not signed up for this activity"
