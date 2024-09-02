from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    user_id: Optional[int]
    username: str
    email: str


class UserAdded(User):
    response: str = "User added."


class UserUpdated(User):
    response: str = "User updated."


class UserDeleted(BaseModel):
    response: str = "User deleted."


class UserAlreadyExistsInDB(User):
    response: str = "Username or email already exists."
