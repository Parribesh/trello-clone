import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.crud import create_user, get_user_by_username
from app.services.auth_service import hash_password
from app.db.database import SessionLocal

# Set up the test client
client = TestClient(app)


@pytest.fixture(scope="function")
def test_db():
    # Create a new database session for testing
    db = SessionLocal()
    yield db
    db.close()


@pytest.fixture(scope="function")
def create_user_in_db(test_db):
    # Check if the user already exists to prevent the integrity error
    existing_user = get_user_by_username(test_db, "testuser")

    if not existing_user:
        # Define user data as a dictionary if the user does not exist
        user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword"
        }

        # Hash the password from the dictionary
        hashed_password = hash_password(user_data["password"])

        # Create the user in the database
        user = create_user(
            test_db, user_data["username"], user_data["email"], hashed_password
        )
        return user
    else:
        # If the user exists, use the existing user data directly
        return existing_user
    
def test_login_for_access_token(create_user_in_db):
    # Arrange: Prepare the form data (login credentials)
    form_data = {
        "username": "testuser",
        "password": "testpassword"
    }

    # Act: Send the request to the login endpoint to get the access token
    response = client.post("/api/auth/token", data=form_data)

    # Assert: Check if the response is successful and contains the access token
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_invalid_login(test_db):
    # Arrange: Prepare invalid form data (wrong password)
    form_data = {
        "username": "testuser",
        "password": "wrongpassword"
    }

    # Act: Send the request to the login endpoint with incorrect credentials
    response = client.post("/api/auth/token", data=form_data)

    # Assert: Check if the response returns Unauthorized status
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"
