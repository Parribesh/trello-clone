import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.schemas.project_schema import ProjectCreate, ProjectUpdate
from app.api.dependencies import get_db

client = TestClient(app)

@pytest.fixture
def db_session():
    # Setup the database session here
    yield Session()

@pytest.fixture
def override_get_db(db_session):
    def _override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = _override_get_db

def test_create_project(override_get_db):
    project_data = {"name": "Test Project", "description": "Test Description"}
    response = client.post("/projects/", json=project_data)
    assert response.status_code == 200
    assert response.json()["name"] == project_data["name"]

def test_read_projects(override_get_db):
    response = client.get("/projects/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_project(override_get_db):
    project_id = 1
    response = client.get(f"/projects/{project_id}")
    if response.status_code == 200:
        assert response.json()["id"] == project_id
    else:
        assert response.status_code == 404

def test_update_project(override_get_db):
    project_id = 1
    update_data = {"name": "Updated Project", "description": "Updated Description"}
    response = client.put(f"/projects/{project_id}", json=update_data)
    if response.status_code == 200:
        assert response.json()["name"] == update_data["name"]
    else:
        assert response.status_code == 404

def test_delete_project(override_get_db):
    project_id = 1
    response = client.delete(f"/projects/{project_id}")
    if response.status_code == 200:
        assert response.json()["id"] == project_id
    else:
        assert response.status_code == 404