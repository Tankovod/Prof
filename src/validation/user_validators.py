from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from .custom_validators import PasswordStr


class User(BaseModel):
    email: EmailStr
    first_name: str = Field(default=..., max_length=32, min_length=2)
    last_name: str = Field(default=..., max_length=32, min_length=2)
    phone: str = Field(default=..., min_length=9, max_length=13, pattern="[+0-9]$")
    password: PasswordStr = Field(
        default=...,
        min_length=8,
        max_length=64,
    )
    # disabled: bool = False

    class Config:
        from_attributes = True


class UserInDB(User):
    hashed_password: str



