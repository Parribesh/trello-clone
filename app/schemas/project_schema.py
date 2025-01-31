from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class User(BaseModel):
    username: str
    email: str


class UserRequest(BaseModel):
    username: str
    email: str
    password: str


class UserInDB(User):
    id: int
    hashed_password: str


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    project_id: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Project(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    tasks: List[Task] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None
    stage: str


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    stage: str
    project_id: int


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    stage: str
    project_id: int


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    project_id: int
    created_at: datetime
    updated_at: datetime
    stage: str


class ProjectResponse(Project):
    id: int
    title: str
    description: Optional[str] = None
    tasks: List[TaskResponse]
    created_at: datetime
    updated_at: datetime
    users: List[UserInDB]
