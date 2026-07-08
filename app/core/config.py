import os
from dotenv import load_dotenv

load_dotenv()


def _is_vercel() -> bool:
    return os.environ.get("VERCEL", "").lower() == "1" or os.environ.get("VERCEL_ENV", "")


def _default_db_path() -> str:
    if _is_vercel():
        return "/tmp/data/clinic.db"
    return "data/clinic.db"


class Settings:
    """
    Central configuration for the application.
    """

    DATABASE_PATH = os.getenv("DATABASE_PATH", _default_db_path())
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    ON_VERCEL: bool = _is_vercel()


settings = Settings()