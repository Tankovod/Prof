from pydantic import SecretStr, PostgresDsn, RedisDsn, Field, EmailStr
from pydantic_settings import BaseSettings
from os import getenv


class Settings(BaseSettings):
    DATABASE_ASYNC_URL: PostgresDsn
    SECRET_KEY: SecretStr  # = getenv('SECRET_KEY')
    ALGORITHM: str  # = getenv('ALGORITHM')
    CELERY_BROKER_URL: RedisDsn  # = getenv('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND: RedisDsn  # = getenv('CELERY_RESULT_BACKEND')
    REDIS_URL: RedisDsn = Field(default='redis://redis:6379/2')
    CELERY_RESULT_EXPIRES: int  # = getenv('CELERY_RESULT_EXPIRES')
    ACCESS_TOKEN_EXPIRE_MINUTES: int


settings = Settings()
