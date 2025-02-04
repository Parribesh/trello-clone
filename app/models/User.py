from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from app.db.base import Base
from app.models.association import user_project


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())

    # Define the relationship: a user can have multiple projects
    projects = relationship(
        "Project", secondary=user_project, back_populates="users")

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"
