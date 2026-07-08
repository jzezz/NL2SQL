import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import initialize_database

if __name__ == "__main__":
    initialize_database()
    print("Database setup complete.")
