from sqlalchemy import Table, Column, Integer, ForeignKey
from app.db.base import Base  # or wherever your Base is defined

# Association table for many-to-many relationship between User and Project
user_project = Table(
    'user_project', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('project_id', Integer, ForeignKey('projects.id'), primary_key=True)
)
