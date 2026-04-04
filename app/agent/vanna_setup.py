import os
from dotenv import load_dotenv

from vanna import Agent, AgentConfig
from vanna.core.registry import ToolRegistry
from vanna.core.user import UserResolver, User

from vanna.tools import RunSqlTool, VisualizeDataTool
from vanna.tools.agent_memory import (
    SaveQuestionToolArgsTool,
    SearchSavedCorrectToolUsesTool
)

from vanna.integrations.sqlite import SqliteRunner
from vanna.integrations.local.agent_memory import DemoAgentMemory
from vanna.integrations.google import GeminiLlmService


load_dotenv()

DB_PATH = "data/clinic.db"


class DefaultUserResolver(UserResolver):
    """
    Minimal async resolver required by Vanna.
    """
    async def resolve_user(self, request_context=None) -> User:
        return User(id="default_user")


def create_agent():
    """
    Initialize the Vanna agent.
    The agent is used only for generating SQL, not executing it.
    """

    if not os.path.exists(DB_PATH):
        raise FileNotFoundError("Database not found. Run setup_database.py first.")

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found")

    llm_service = GeminiLlmService(
        model="gemini-2.5-flash",
        api_key=api_key
    )

    # Tools are still registered to match assignment architecture
    sql_runner = SqliteRunner(database_path=DB_PATH)
    memory = DemoAgentMemory()

    tool_registry = ToolRegistry()

    tool_registry.register_local_tool(
        RunSqlTool(sql_runner=sql_runner),
        ["*"]
    )

    tool_registry.register_local_tool(
        VisualizeDataTool(),
        ["*"]
    )

    tool_registry.register_local_tool(
        SaveQuestionToolArgsTool(),
        ["*"]
    )

    tool_registry.register_local_tool(
        SearchSavedCorrectToolUsesTool(),
        ["*"]
    )

    # Strong instructions to force SQL-only output
    config = AgentConfig(
        name="nl2sql-agent",
        instructions=(
            "You are a SQLite SQL generator.\n\n"

            "You MUST strictly use ONLY the tables and columns listed below.\n"
            "Do NOT invent or assume any table names.\n\n"

            "ALLOWED TABLES:\n"
            "- patients(id, name, age, gender)\n"
            "- doctors(id, name, specialization)\n"
            "- appointments(id, patient_id, doctor_id, date)\n"
            "- treatments(id, patient_id, description, cost)\n"
            "- invoices(id, patient_id, amount, date)\n\n"

            "STRICT RULES:\n"
            "- Output ONLY SQL\n"
            "- Use ONLY the tables listed above\n"
            "- Do NOT use patient_records, transactions, or any other table\n"
            "- Query MUST start with SELECT\n"
            "- Do NOT include markdown or explanation\n\n"

            "EXAMPLES:\n"
            "Question: How many patients?\n"
            "Answer: SELECT COUNT(*) FROM patients\n\n"

            "Question: Total revenue?\n"
            "Answer: SELECT SUM(amount) FROM invoices\n\n"
        
        )
    )

    agent = Agent(
        config=config,
        llm_service=llm_service,
        tool_registry=tool_registry,
        agent_memory=memory,
        user_resolver=DefaultUserResolver()
    )

    return agent