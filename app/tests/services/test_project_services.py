import pytest
from sqlalchemy.orm import Session
from app.models.Project import Project
from app.schemas.project_schema import ProjectCreate, ProjectUpdate
from app.services.project_service import ProjectService
from app.db.database import SessionLocal, engine
from app.utils.logger import setup_logger, log_message
import logging

logger = setup_logger("test_project_services")


@pytest.fixture(scope="function")
def db_session():
    # Create a new database session for testing
    db = SessionLocal()
    yield db
    db.close()


def test_get_project(db_session: Session):
    # Step 1: Create a new project
    project_data = ProjectCreate(
        title="Test Project",
        description="Test Description",
        stage="active"
    )
    created_project = ProjectService.create_project(db_session, project_data)

    # Ensure the project is created
    assert created_project is not None
    assert created_project.title == "Test Project"
    assert created_project.description == "Test Description"

    # Step 2: Test the get_project method
    fetched_project = ProjectService.get_project(
        db_session, created_project.id)
    print(f"Fetched Project: {fetched_project}")

    # Assertions to verify the fetched project
    assert fetched_project is not None
    assert fetched_project.id == created_project.id
    assert fetched_project.title == created_project.title
    assert fetched_project.description == created_project.description


def test_get_projects(db_session: Session):
    projects = ProjectService.get_projects(db_session, skip=0, limit=10)
    assert len(projects) <= 10


def test_create_project(db_session: Session, caplog):
    project_data = ProjectCreate(
        title="Test Project", description="Test Description", stage="active")
    with caplog.at_level(logging.DEBUG):
        project = ProjectService.create_project(db_session, project_data)
        log_message(logger, "debug", f"Created Project: {project}")

    # Assert log message
    assert "Created Project:" in caplog.text

    # Assert other test conditions
    assert project is not None
    assert project.title == "Test Project"
    assert project.description == "Test Description"


def test_update_project(db_session: Session):
    project_id = 1
    update_data = ProjectUpdate(name="Updated Project")
    project = ProjectService.update_project(
        db_session, project_id, update_data)
    assert project is not None
    assert project.name == "Updated Project"


def test_delete_project(db_session: Session):
    # Step 1: Create a new project
    project_data = ProjectCreate(
        title="Test Project",
        description="Test Description",
        stage="active"
    )
    created_project = ProjectService.create_project(db_session, project_data)

    # Ensure the project is created
    assert created_project is not None
    assert created_project.title == "Test Project"
    assert created_project.description == "Test Description"

    # Step 2: Delete the created project
    deleted_project = ProjectService.delete_project(
        db_session, created_project.id)

    # Step 3: Assert the project was deleted
    # Assuming delete_project returns None after deletion
    assert deleted_project.id == created_project.id

    # Step 4: Try to fetch the deleted project and confirm it no longer exists
    fetched_project = ProjectService.get_project(
        db_session, created_project.id)
    assert fetched_project is None
