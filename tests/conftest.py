import pytest
import sys
from pathlib import Path

# Add src directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    from fastapi.testclient import TestClient
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to initial state before each test"""
    # Store initial state
    initial_state = {
        "Soccer": {
            "description": "Team sport focusing on soccer skills and competitive matches",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 22,
            "participants": ["alex@mergington.edu"]
        },
        "Basketball": {
            "description": "Basketball training and intramural games",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["james@mergington.edu"]
        },
        "Debate Club": {
            "description": "Develop public speaking and critical thinking skills",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["sarah@mergington.edu"]
        },
        "Science Olympiad": {
            "description": "Compete in science and engineering challenges",
            "schedule": "Saturdays, 10:00 AM - 12:00 PM",
            "max_participants": 15,
            "participants": ["noah@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore painting, drawing, and mixed media techniques",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["isabella@mergington.edu"]
        },
        "Drama Club": {
            "description": "Participate in theatrical productions and acting workshops",
            "schedule": "Mondays and Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["lucas@mergington.edu"]
        },
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        }
    }
    
    # Yield to run the test
    yield
    
    # Reset after test
    activities.clear()
    activities.update(initial_state)
