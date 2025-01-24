from app.db.schemas.user import User
from app.db.crud import create_user, get_user_by_username
from app.services.auth_service import create_access_token, hash_password, verify_password
from fastapi import HTTPException, status
from sqlalchemy.orm import Session


async def register_user(user: User, db: Session):
    existing_user = get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_password = hash_password(user.password)
    user_in_db = create_user(db, user.username, user.email, hashed_password)
    return {"msg": "User registered successfully!"}
