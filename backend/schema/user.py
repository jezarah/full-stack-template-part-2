import uuid
from pydantic import EmailStr

from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    name: str = Field(max_length=255)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    role: int = 0  # 0 - Normal User, 1 - Admin User
    access_token: str | None = Field(default=None)


# Create
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=20)


class UserCreateAdmin(UserCreate):
    role: int = 1


# Read (or Delete), id is always required
class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Update
class UserUpdate(UserBase):
    email: str | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=20)
    name: str | None = Field(default=None, max_length=255)


class UserUpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=20)
    new_password: str = Field(min_length=8, max_length=20)
