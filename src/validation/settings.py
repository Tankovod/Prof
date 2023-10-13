from pydantic import SecretStr, PostgresDsn, RedisDsn, Field, EmailStr
from pydantic_settings import BaseSettings
from os import getenv


class Settings(BaseSettings):
    DATABASE_ASYNC_URL: PostgresDsn
    SECRET_KEY: SecretStr
    ALGORITHM: str
    CELERY_BROKER_URL: RedisDsn
    CELERY_RESULT_BACKEND: RedisDsn
    REDIS_URL: RedisDsn = Field(default='redis://redis:6379/2')
    CELERY_RESULT_EXPIRES: int
    ACCESS_TOKEN_EXPIRE_MINUTES: int


settings = Settings()
