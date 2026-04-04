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

    # SQLite runner (kept for tool compatibility)
    sql_runner = SqliteRunner(database_path=DB_PATH)

    # Memory (optional but included as per assignment)
    memory = DemoAgentMemory()

    # Tool registry
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

    # Updated instructions (FIXED SCHEMA + STRONG CONTROL)
    config = AgentConfig(
        name="nl2sql-agent",
        instructions=(
            "You are a SQLite SQL generator.\n\n"

            "Your ONLY job is to return a valid SQL SELECT query.\n\n"

            "STRICT RULES:\n"
            "- Output ONLY SQL\n"
            "- DO NOT explain anything\n"
            "- DO NOT use markdown\n"
            "- DO NOT add text before or after SQL\n"
            "- Query MUST start with SELECT\n\n"

            "DATABASE SCHEMA:\n"
            "patients(id, first_name, last_name, age, gender)\n"
            "doctors(id, name, specialization)\n"
            "appointments(id, patient_id, doctor_id, date)\n"
            "treatments(id, patient_id, description, cost)\n"
            "invoices(id, patient_id, amount, date)\n\n"

            "IMPORTANT:\n"
            "- patients table DOES NOT have a 'name' column\n"
            "- Use full name as:\n"
            "  first_name || ' ' || last_name\n\n"

            "RULES:\n"
            "- Use ONLY the tables listed above\n"
            "- Never invent tables like patient_records or transactions\n"
            "- Always use correct column names\n\n"

            "QUERY GUIDELINES:\n"
            "- COUNT(*) for totals\n"
            "- SUM(amount) for revenue\n"
            "- Use JOIN when needed\n"
            "- Use GROUP BY for aggregation\n"
            "- Use ORDER BY for sorting\n"
            "- Use LIMIT for top results\n\n"

            "EXAMPLES:\n"
            "How many patients?\n"
            "SELECT COUNT(*) FROM patients\n\n"

            "List patient names:\n"
            "SELECT first_name || ' ' || last_name FROM patients\n\n"

            "Total revenue?\n"
            "SELECT SUM(amount) FROM invoices\n\n"

            "If unsure, return the closest valid SQL using available tables.\n"
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