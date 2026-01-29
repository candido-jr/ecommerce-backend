import os

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


def _get_env(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise RuntimeError(f"{name} environment variable is required")
    return value


class Settings(BaseModel):
    DATABASE_URL: str = _get_env("DATABASE_URL")

    JWT_SECRET: str = _get_env("JWT_SECRET")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(_get_env("ACCESS_TOKEN_EXPIRE_MINUTES"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(_get_env("REFRESH_TOKEN_EXPIRE_DAYS"))

    # cookie settings
    REFRESH_COOKIE_NAME: str = _get_env("REFRESH_COOKIE_NAME")
    COOKIE_SECURE: bool = _get_env("COOKIE_SECURE").lower() in {"1", "true", "yes"}
    COOKIE_SAMESITE: str = _get_env("COOKIE_SAMESITE")


settings = Settings()
