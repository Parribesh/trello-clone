# Database connection logic
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Or your preferred database URL

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
