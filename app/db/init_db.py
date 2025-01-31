# app/db/init_db.py
from app.db.database import engine
from app.models.User import User  # Import User model
from app.models.Project import Project  # Import Project model
from app.models.Task import Task  # Import Task model
from app.db.base import Base

# Create all tables in the database
# This will create the "users" table if it doesn't exist


def init_db():
    from app.db.database import SessionLocal
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Database tables created successfully.")
