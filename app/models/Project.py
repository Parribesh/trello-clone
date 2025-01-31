from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from app.db.base import Base
from enum import Enum as PyEnum
from sqlalchemy import ForeignKey
from app.models.association import user_project


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    stage = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    users = relationship("User", secondary=user_project,
                         back_populates="projects")
    tasks = relationship("Task", back_populates="project")

    def __repr__(self):
        return f"<Project(id={self.id}, title={self.title}, stage={self.stage})>"
