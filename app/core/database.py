import sqlite3
from app.core.config import settings


def get_connection():
    """
    Create and return a SQLite connection.
    """
    return sqlite3.connect(settings.DATABASE_PATH)