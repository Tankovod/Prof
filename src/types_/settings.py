from passlib.context import CryptContext
from pydantic import SecretStr, BaseConfig, PostgresDsn


class Settings(BaseConfig):
    DATABASE_URL: PostgresDsn = "postgresql+asyncpg://drov:drov@127.0.0.1:5432/drov"
    SECRET_KEY: SecretStr = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"

