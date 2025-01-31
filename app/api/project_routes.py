from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.services.project_service import ProjectService
from app.schemas.project_schema import ProjectResponse, ProjectCreate, ProjectUpdate
from app.api.dependencies import get_db, get_current_user
from app.models.User import User as DBUser
router = APIRouter()
project_service = ProjectService()


@router.post("/", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db), user: DBUser = Depends(get_current_user)):
    return project_service.create_project(db, project, user_id=user.id)


@router.get("/", response_model=List[ProjectResponse])
def read_all_projects(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), user: DBUser = Depends(get_current_user)):
    all_projects = project_service.get_projects(
        db, user_id=user.id, skip=skip, limit=limit)
    paginated_projects = all_projects[skip: skip + limit]
    return paginated_projects


@router.get("/user", response_model=List[ProjectResponse])
def read_projects(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    user: DBUser = Depends(get_current_user)
):
    # Fetch all projects belonging to the current user
    all_projects = project_service.get_all_projects_by_user(
        db, user_id=user.id)
    # Apply pagination to the list of projects
    paginated_projects = all_projects[skip: skip + limit]

    return paginated_projects


@router.post("/{project_id}/add", response_model=ProjectResponse)
async def add_to_project(project_id: int, db: Session = Depends(get_db), user: DBUser = Depends(get_current_user)):
    project = project_service.get_project(db, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    # we need to check if the user is the owner of the project
    # if project.user_id != user.id:
    #     raise HTTPException(
    #         status_code=403, detail="Not authorized to access this project")

    # Assuming there's a method in project_service to handle the addition logic
    updated_project = ProjectService.assign_user_to_project(
        db, project_id, user.id)
    return updated_project


@router.get("/{project_id}", response_model=ProjectResponse)
def read_project(project_id: int, db: Session = Depends(get_db), user: DBUser = Depends(get_current_user)):
    project = project_service.get_project(db, project_id)
    if project.user_id != user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this project")
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project: ProjectUpdate, db: Session = Depends(get_db)):
    updated_project = project_service.update_project(db, project_id, project)
    if updated_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return updated_project


@router.delete("/{project_id}", response_model=ProjectResponse)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    deleted_project = project_service.delete_project(db, project_id)
    if deleted_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return deleted_project
