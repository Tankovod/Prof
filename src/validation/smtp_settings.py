from pydantic import EmailStr, Field
from pydantic_settings import BaseSettings


class SMTPSettings(BaseSettings):
    SMTP_USER: EmailStr
    SMTP_PASS: str = Field(min_length=5)
    SMTP_HOST: str = Field(default="smtp.gmail.com")
    SMTP_PORT: int = Field(default=465)


smtp_settings = SMTPSettings()
