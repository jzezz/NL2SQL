import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Central configuration for the application.
    """

    DATABASE_PATH = os.getenv("DATABASE_PATH", "data/clinic.db")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


settings = Settings()