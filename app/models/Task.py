from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from app.db.base import Base
from enum import Enum as PyEnum
from sqlalchemy import ForeignKey


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    stage = Column(Enum('TODO', 'In Progress', 'completed',
                   name="taskstage_enum"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    project = relationship("Project", back_populates="tasks")

    def __repr__(self):
        return f"<Task(title={self.title}, stage={self.stage})>"
