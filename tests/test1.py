import asyncio
import sqlite3
import re

from app.agent.vanna_setup import create_agent
from vanna.core.user import User


def extract_sql(text):
    match = re.search(r"SELECT .*", text, re.IGNORECASE | re.DOTALL)
    return match.group(0) if match else None


async def main():
    agent = create_agent()
    user = User(id="default_user")

    question = "How many patients do we have?"

    stream = agent.send_message(user, question)

    final_text = ""

    async for chunk in stream:
        if hasattr(chunk, "simple_component") and chunk.simple_component:
            text = getattr(chunk.simple_component, "text", "")
            final_text += text

    print("\nModel Response:\n", final_text)

    # Try extracting SQL
    sql = extract_sql(final_text)

    #  Fallback if agent failed
    if not sql:
        print("\nFallback triggered")
        sql = "SELECT COUNT(*) AS total_patients FROM patients"

    print("\nExecuting SQL:\n", sql)

    # Execute query
    conn = sqlite3.connect("data/clinic.db")
    cursor = conn.cursor()

    cursor.execute(sql)
    result = cursor.fetchall()

    print("\nResult:", result)


if __name__ == "__main__":
    asyncio.run(main())