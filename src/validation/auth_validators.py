from pydantic import BaseModel, Field
from .custom_validators import password_validator


class LoginData(BaseModel):
    phone: str = Field(...)
    password: str = Field(...)
