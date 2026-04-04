import sys
import os

# Add project root to path so 'app' can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import get_connection


def check_schema():
    conn = get_connection()
    cursor = conn.cursor()

    print("\n--- PATIENTS TABLE ---")
    cursor.execute("PRAGMA table_info(patients)")
    print(cursor.fetchall())

    print("\n--- INVOICES TABLE ---")
    cursor.execute("PRAGMA table_info(invoices)")
    print(cursor.fetchall())

    conn.close()


if __name__ == "__main__":
    check_schema()