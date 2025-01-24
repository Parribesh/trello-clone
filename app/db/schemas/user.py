from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    password: str  # In practice, hash this password before storing
    role: str

class UserInDB(User):
    hashed_password: str
