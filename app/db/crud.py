from app.models.user_model import User as DBUser
from sqlalchemy.orm import Session


def create_user(db: Session, username: str, email: str, hashed_password: str):
    db_user = DBUser(username=username, email=email,
                     hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_username(db: Session, username: str):
    return db.query(DBUser).filter(DBUser.username == username).first()


def get_users(db: Session):
    return db.query(DBUser).all()
