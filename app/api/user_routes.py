from fastapi import APIRouter, Depends, Response
from app.schemas.project_schema import User, UserInDB, UserRequest
from app.services.user_service import register_user
from app.services.auth_service import create_access_token
from app.api.dependencies import get_current_user, get_db, get_all_users
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.services.user_service import get_user_by_username, verify_password
from datetime import timedelta

router = APIRouter()


# Define the token expiration duration
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Registration route


@router.post("/register")
async def register(user: UserRequest, db: Session = Depends(get_db)):
    return await register_user(user, db)


# Protected route (example)
@router.get("/profile")
async def profile(current_user: UserInDB = Depends(get_current_user)):
    print("called")
    return current_user

# protected route


@router.get("/users")
async def profile(users: UserInDB = Depends(get_all_users)):
    print("called")
    return users


@router.get("/test")
async def test():
    print("called")
    return {"msg": "Test successful!"}


@router.post("/token")
async def login_for_access_token(
    response: Response,  # To set cookies in the response
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    # 1. Retrieve the user from the database
    user = get_user_by_username(db, form_data.username)

    # 2. Verify credentials
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Generate a token if credentials are valid
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username})

    # 4. Set the token as a secure, HTTP-only cookie
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,  # Prevent access from JavaScript
        secure=True,    # Use HTTPS
        samesite="Lax",  # Prevent CSRF attacks
        path="/",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60  # Token expiration in seconds
    )

    # 5. Return a message to the client
    return {"msg": "Login successful!"}


@router.post("/logout")
def logout(response: Response):
    # Overwrite the cookie with a past expiry date
    response.set_cookie(
        key="access_token",
        value="",
        httponly=True,
        expires=0,  # Immediate expiration
        path="/"
    )
    return {"message": "Logged out and token invalidated"}
