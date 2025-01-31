from typing import List, Optional
from app.models.Project import Project
from app.schemas.project_schema import ProjectCreate, ProjectUpdate
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.User import User


class ProjectService:
    @staticmethod
    def get_project(db: Session, project_id: int) -> Optional[Project]:
        return db.query(Project).filter(Project.id == project_id).first()

    @staticmethod
    def get_projects(db: Session, user_id: int, skip: int = 0, limit: int = 10) -> List[Project]:
        return db.query(Project).filter(~Project.users.any(User.id == user_id)).offset(skip).limit(limit).all()

    @staticmethod
    def get_all_projects_by_user(db: Session, user_id: int) -> List[Project]:
        # Fetch all projects that belong to the user
        test_projects = (db.query(Project).all())
        print(f'project size: {len(test_projects)}')
        for project in test_projects:
            print(f'user size: {len(project.users)}')
        projects = db.query(Project).filter(
            Project.users.any(User.id == user_id)).all()
        return projects

    @staticmethod
    def create_project(db: Session, project: ProjectCreate, user_id: int) -> Project:
        # Query the user from user_id
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")

        # Create a new Project instance from ProjectCreate, and set the necessary fields
        db_project = Project(
            title=project.title,  # Mapping the title to name field in Project
            description=project.description,
            stage=project.stage,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        db_project.users.append(user)

        # Add the project to the session
        db.add(db_project, user)
        db.commit()  # Commit the transaction
        # Refresh to get the latest data (e.g., generated ID)
        db.refresh(db_project)

        return db_project

    @staticmethod
    def update_project(db: Session, project_id: int, project: ProjectUpdate) -> Optional[Project]:
        db_project = ProjectService.get_project(db, project_id)
        if db_project:
            for key, value in project.dict(exclude_unset=True).items():
                setattr(db_project, key, value)
            db.commit()
            db.refresh(db_project)
        return db_project

    @staticmethod
    def delete_project(db: Session, project_id: int) -> Optional[Project]:
        db_project = db.query(Project).filter(Project.id == project_id).first()
        if db_project:
            db.delete(db_project)
            db.commit()
        return db_project

    @staticmethod
    def assign_user_to_project(db: Session, project_id: int, user_id: int) -> Optional[Project]:
        # Query the project from project_id
        project = ProjectService.get_project(db, project_id)
        if not project:
            raise ValueError("Project not found")

        # Query the user from user_id
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")

        # Add the user to the project's users
        project.users.append(user)

        # Commit the transaction
        db.commit()
        db.refresh(project)

        return project
