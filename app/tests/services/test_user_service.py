from fastapi.testclient import TestClient
from app.main import app
from app.db.database import SessionLocal, engine
from app.models.user_model import User as DBUser
from app.db.crud import create_user, get_user_by_username
from app.services.auth_service import hash_password, verify_password
from app.db.schemas.user import User
from app.services.user_service import register_user
from fastapi import HTTPException
from sqlalchemy.orm import Session
import pytest


@pytest.fixture(scope="function")
def test_db():
    # Create a new database session for testing
    db = SessionLocal()
    yield db
    db.close()

# Test case for registering a user


@pytest.mark.asyncio
async def test_register_user(test_db: Session):
    # Arrange: Create a User object
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword"
    }

    # Act: Call the register_user function with the test data
    user = User(**user_data)

    # Register the user in the database using the register_user function
    response =  await register_user(user, test_db)

    # Assert: Check if the user is created successfully
    assert response["msg"] == "User registered successfully!"

    # Verify user exists in the database
    db_user = get_user_by_username(test_db, user.username)
    assert db_user is not None
    assert db_user.username == user.username
    assert db_user.email == user.email
    # Verify the password is hashed correctly
    assert verify_password(user.password, db_user.hashed_password)

# Test case for when a user with the same username already exists


def test_register_user_username_taken(test_db: Session):
    # Arrange: Create a user and register it first
    user_data = {
        "username": "existinguser",
        "email": "existinguser@example.com",
        "password": "testpassword"
    }

    user = User(**user_data)
    register_user(user, test_db)

    # Act: Try to register the user again
    new_user = User(username="existinguser",
                    email="newemail@example.com", password="newpassword")

    try:
        response = register_user(new_user, test_db)
    except HTTPException as e:
        # Assert: Check if HTTPException is raised due to username already being taken
        assert e.status_code == 400
        assert e.detail == "Username already taken"

# Test case for password hashing


def test_hash_password():
    password = "testpassword"
    hashed = hash_password(password)

    # Assert: Check that the password is hashed and not plain text
    assert hashed != password
    # Ensure the hash matches the original password
    assert verify_password(password, hashed)
