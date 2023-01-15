import os
from typing import Final, Optional


def getenv(key: str) -> str:
    v: Optional[str] = os.getenv(key)
    assert v is not None, f"Settings {key} is not found"
    return v


APP_MODULE: Final[str] = getenv("APP_MODULE")

MAIN_DB_HOST: Final[str] = getenv("MAIN_DB_HOST")
MAIN_DB_PORT: Final[str] = getenv("MAIN_DB_PORT")
MAIN_DB_DATABASE: Final[str] = getenv("MAIN_DB_NAME")
MAIN_DB_USER: Final[str] = getenv("MAIN_DB_USER")
MAIN_DB_PASSWORD: Final[str] = getenv("MAIN_DB_PASSWORD")


DATABASES = {
    "default": "verify",
    "DATABASE": {
        "main": {
            "ENGINE": "django.db.backends.postgresql",
            "DB_HOST": MAIN_DB_HOST,
            "DB_PORT": MAIN_DB_PORT,
            "DB_NAME": MAIN_DB_DATABASE,
            "DB_USER": MAIN_DB_USER,
            "DB_PASSWORD": MAIN_DB_PASSWORD,
        },
    },
}

MAIN_DATABASE_ENGINE_URL = (
    "postgresql+asyncpg://"
    f"{MAIN_DB_USER}:{MAIN_DB_PASSWORD}@"
    f"{MAIN_DB_HOST}:{MAIN_DB_PORT}/{MAIN_DB_DATABASE}"
)
