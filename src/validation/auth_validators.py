from pydantic import BaseModel, Field
from .custom_validators import password_validator


class LoginData(BaseModel):
    phone: str = Field(default=...)
    password: str = Field(default=...)


# class RegistrationResponse(BaseModel):
