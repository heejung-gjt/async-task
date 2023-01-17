import os
from typing import Final, Optional

from dotenv import load_dotenv

load_dotenv()

def getenv(key: str) -> str:
    v: Optional[str] = os.environ.get(key)
    assert v is not None, f"Settings {key} is not found"
    return v


MAIN_DB_HOST: Final[str] = getenv("MAIN_DB_HOST")
MAIN_DB_PORT: Final[str] = getenv("MAIN_DB_PORT")
MAIN_DB_DATABASE: Final[str] = getenv("MAIN_DB_DATABASE")
MAIN_DB_USER: Final[str] = getenv("MAIN_DB_USER")
MAIN_DB_PASSWORD: Final[str] = getenv("MAIN_DB_PASSWORD")


DATABASES = {
    "default": "main",
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
