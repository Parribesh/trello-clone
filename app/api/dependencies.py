from fastapi import Request, HTTPException, status, Depends
from app.services.auth_service import verify_token
from app.db.crud import get_user_by_username
from fastapi.security import OAuth2PasswordBearer
from app.db.database import SessionLocal
from sqlalchemy.orm import Session
from app.db.crud import get_users
# Dependency for extracting user information from the JWT token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(request: Request, db: Session = Depends(get_db)):
    # Retrieve the token from cookies
    token = request.cookies.get("access_token")
    print(f"token: {token}")
    if token and token.startswith("Bearer "):
        token = token[len("Bearer "):]

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing token in cookies"
        )
    # Verify the token
    username = verify_token(token)  # Get the username from the JWT
    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user


def get_all_users(request: Request, db: Session = Depends(get_db)):
    # Retrieve the token from cookies
    token = request.cookies.get("access_token")
    print(f"token: {token}")
    if token and token.startswith("Bearer "):
        token = token[len("Bearer "):]

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing token in cookies"
        )
    # Verify the token
    _ = verify_token(token)  # Get the username from the JWT
    users = get_users(db)
    if not users:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Users not found"
        )
    return users
