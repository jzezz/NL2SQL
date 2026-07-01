import os
import sqlite3
from app.core.config import settings


def get_connection():
    """
    Create and return a SQLite connection.
    """
    db_dir = os.path.dirname(settings.DATABASE_PATH)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)

    return sqlite3.connect(settings.DATABASE_PATH)
