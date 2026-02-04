import pytest


class TestGetActivities:
    """Test the GET /activities endpoint"""
    
    def test_get_activities_returns_all_activities(self, client, reset_activities):
        """Test that get_activities returns all activities"""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        assert "Soccer" in data
        assert "Basketball" in data
        assert "Chess Club" in data
        assert len(data) == 9
    
    def test_get_activities_has_correct_structure(self, client, reset_activities):
        """Test that activities have correct structure"""
        response = client.get("/activities")
        data = response.json()
        activity = data["Soccer"]
        
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert isinstance(activity["participants"], list)


class TestSignupForActivity:
    """Test the POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_for_activity_success(self, client, reset_activities):
        """Test successful signup"""
        response = client.post(
            "/activities/Soccer/signup?email=newstudent@mergington.edu"
        )
        assert response.status_code == 200
        data = response.json()
        assert "Signed up" in data["message"]
        assert "newstudent@mergington.edu" in data["message"]
    
    def test_signup_adds_participant(self, client, reset_activities):
        """Test that signup actually adds participant"""
        client.post("/activities/Soccer/signup?email=newstudent@mergington.edu")
        
        response = client.get("/activities")
        activity = response.json()["Soccer"]
        assert "newstudent@mergington.edu" in activity["participants"]
    
    def test_signup_for_nonexistent_activity_returns_404(self, client, reset_activities):
        """Test signup for non-existent activity returns 404"""
        response = client.post(
            "/activities/NoExistentActivity/signup?email=student@mergington.edu"
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_signup_duplicate_student_returns_400(self, client, reset_activities):
        """Test signup with duplicate student returns 400"""
        response = client.post(
            "/activities/Soccer/signup?email=alex@mergington.edu"
        )
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
    
    def test_signup_multiple_activities(self, client, reset_activities):
        """Test that same student can signup for different activities"""
        client.post(
            "/activities/Soccer/signup?email=newstudent@mergington.edu"
        )
        response = client.post(
            "/activities/Basketball/signup?email=newstudent@mergington.edu"
        )
        assert response.status_code == 200
        
        activities = client.get("/activities").json()
        assert "newstudent@mergington.edu" in activities["Soccer"]["participants"]
        assert "newstudent@mergington.edu" in activities["Basketball"]["participants"]


class TestUnregisterFromActivity:
    """Test the DELETE /activities/{activity_name}/unregister endpoint"""
    
    def test_unregister_success(self, client, reset_activities):
        """Test successful unregister"""
        # First signup
        client.post("/activities/Soccer/signup?email=newstudent@mergington.edu")
        
        # Then unregister
        response = client.delete(
            "/activities/Soccer/unregister?email=newstudent@mergington.edu"
        )
        assert response.status_code == 200
        data = response.json()
        assert "Unregistered" in data["message"]
    
    def test_unregister_removes_participant(self, client, reset_activities):
        """Test that unregister actually removes participant"""
        # Setup: signup first
        client.post("/activities/Soccer/signup?email=newstudent@mergington.edu")
        
        # Unregister
        client.delete(
            "/activities/Soccer/unregister?email=newstudent@mergington.edu"
        )
        
        # Verify removal
        response = client.get("/activities")
        activity = response.json()["Soccer"]
        assert "newstudent@mergington.edu" not in activity["participants"]
    
    def test_unregister_nonexistent_activity_returns_404(self, client, reset_activities):
        """Test unregister for non-existent activity returns 404"""
        response = client.delete(
            "/activities/NoExistentActivity/unregister?email=student@mergington.edu"
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_unregister_nonexistent_student_returns_400(self, client, reset_activities):
        """Test unregister for non-existent student returns 400"""
        response = client.delete(
            "/activities/Soccer/unregister?email=notasignup@mergington.edu"
        )
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]
    
    def test_unregister_existing_participant(self, client, reset_activities):
        """Test unregistering an existing participant"""
        response = client.delete(
            "/activities/Soccer/unregister?email=alex@mergington.edu"
        )
        assert response.status_code == 200
        
        # Verify removal
        activities = client.get("/activities").json()
        assert "alex@mergington.edu" not in activities["Soccer"]["participants"]


class TestIntegration:
    """Integration tests for signup and unregister flows"""
    
    def test_full_lifecycle(self, client, reset_activities):
        """Test complete signup and unregister lifecycle"""
        email = "testuser@mergington.edu"
        activity = "Art Club"
        
        # Check initial state
        initial = client.get("/activities").json()
        initial_count = len(initial[activity]["participants"])
        
        # Signup
        signup_response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        assert signup_response.status_code == 200
        
        # Verify addition
        after_signup = client.get("/activities").json()
        assert len(after_signup[activity]["participants"]) == initial_count + 1
        assert email in after_signup[activity]["participants"]
        
        # Unregister
        unregister_response = client.delete(
            f"/activities/{activity}/unregister?email={email}"
        )
        assert unregister_response.status_code == 200
        
        # Verify removal
        after_unregister = client.get("/activities").json()
        assert len(after_unregister[activity]["participants"]) == initial_count
        assert email not in after_unregister[activity]["participants"]
