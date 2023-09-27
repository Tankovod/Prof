from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class User(BaseModel):
    email: EmailStr
    first_name: Optional[str] = Field(..., max_length=32)
    last_name: Optional[str] = Field(..., max_length=32)
    phone: str = Field(..., min_length=9, max_length=13, pattern="[+0-9]$")
    password: str = Field(
        ...,
        min_length=8,
        max_length=64,
    )
    # disabled: bool

    class Config:
        from_attributes = True


class UserInDB(User):
    hashed_password: str


class ProductValid(BaseModel):
    title: str
    description: str
    amount: int
    units: str


class LoginData(BaseModel):
    phone: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: str | None = None

