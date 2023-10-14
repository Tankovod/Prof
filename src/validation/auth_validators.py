from pydantic import BaseModel, Field


class LoginData(BaseModel):
    phone: str = Field(default=...)
    password: str = Field(default=...)


# class RegistrationResponse(BaseModel):
