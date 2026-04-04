import asyncio

from app.agent.vanna_setup import create_agent
from vanna.core.user import User


async def seed():
    agent = create_agent()
    user = User(id="default_user")

    questions = [
        "Give me SQL to count total patients",
        "Generate SQL for total revenue",
        "Show SQL for top 5 patients by spending"
    ]

    for q in questions:
        print(f"Seeding: {q}")

        stream = agent.send_message(user, q)

        async for _ in stream:
            pass  # just consume to let agent learn

    print("Memory seeded via interactions")


if __name__ == "__main__":
    asyncio.run(seed())