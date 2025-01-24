# app/db/init_db.py
from app.db.database import engine
from app.models.user_model import User  # Import User model

# Create all tables in the database
# This will create the "users" table if it doesn't exist


def init_db():
    from app.db.database import Base
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Database tables created successfully.")
