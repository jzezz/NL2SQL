import os
from dotenv import load_dotenv

from app.core.config import settings


load_dotenv()

DB_PATH = settings.DATABASE_PATH


class DefaultUserResolver:
    async def resolve_user(self, request_context=None):
        from vanna.core.user import User
        return User(id="default_user")


def create_agent():
    return create_sql_agent()


def _build_llm_service():
    provider = settings.LLM_PROVIDER

    if provider == "google":
        return _build_gemini_llm()
    elif provider in ("openai", "groq"):
        return _build_openai_compatible_llm()
    else:
        raise ValueError(
            f"Unknown LLM_PROVIDER '{provider}'. Use 'google', 'openai', or 'groq'."
        )


def _build_gemini_llm():
    from vanna.integrations.google.gemini import GeminiLlmService

    api_key = settings.GOOGLE_API_KEY
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY not found. Set it in Vercel env vars "
            "or switch to a different LLM_PROVIDER."
        )

    return GeminiLlmService(
        model="gemini-2.0-flash",
        api_key=api_key,
    )


def _build_openai_compatible_llm():
    from app.services.openai_llm import OpenAILlmService

    api_key = settings.LLM_API_KEY
    if not api_key:
        raise ValueError(
            "LLM_API_KEY not found. Set it in Vercel env vars."
        )

    provider = settings.LLM_PROVIDER
    if provider == "groq":
        base_url = settings.LLM_BASE_URL or "https://api.groq.com/openai/v1"
        model = settings.LLM_MODEL or "llama3-8b-8192"
    else:
        base_url = settings.LLM_BASE_URL or "https://api.openai.com/v1"
        model = settings.LLM_MODEL or "gpt-4o-mini"

    return OpenAILlmService(
        api_key=api_key,
        model=model,
        base_url=base_url,
    )


def _base_agent(config, llm_service, tool_registry=None):
    from vanna import Agent
    from vanna.integrations.local.agent_memory import DemoAgentMemory

    return Agent(
        config=config,
        llm_service=llm_service,
        tool_registry=tool_registry,
        agent_memory=DemoAgentMemory(),
        user_resolver=DefaultUserResolver(),
    )


def _empty_tool_registry():
    from vanna.core.registry import ToolRegistry
    return ToolRegistry()


def create_planner_agent():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError("Database not found. Run setup_database.py first.")

    llm_service = _build_llm_service()

    from vanna import AgentConfig
    config = AgentConfig(
        name="query-planner",
        instructions=(
            "You are a planning agent for an NL2SQL system.\n\n"
            "Your job is to classify the user question and return JSON only.\n\n"
            "Return this shape exactly:\n"
            "{\n"
            '  "intent": "count|list|aggregate|trend|comparison|lookup|other",\n'
            '  "needs_chart": true|false,\n'
            '  "suggested_granularity": "row|day|month|category|none",\n'
            '  "notes": "short explanation"\n'
            "}\n\n"
            "Rules:\n"
            "- JSON only\n"
            "- No markdown\n"
            "- No extra text\n"
            "- Prefer needs_chart=true for aggregates, trends, and comparisons\n"
        ),
    )

    return _base_agent(config, llm_service, _empty_tool_registry())


def create_verifier_agent():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError("Database not found. Run setup_database.py first.")

    llm_service = _build_llm_service()

    from vanna import AgentConfig
    config = AgentConfig(
        name="sql-verifier",
        instructions=(
            "You are a SQL verifier for a SQLite NL2SQL system.\n\n"
            "Your job is to review SQL and return JSON only.\n\n"
            "Return this shape exactly:\n"
            "{\n"
            '  "approved": true|false,\n'
            '  "corrected_sql": "SQL string or empty string",\n'
            '  "reason": "short explanation"\n'
            "}\n\n"
            "Rules:\n"
            "- JSON only\n"
            "- No markdown\n"
            "- No extra text\n"
            "- If the SQL is valid, set approved=true and repeat it in corrected_sql\n"
            "- If the SQL is invalid, fix only schema-safe issues\n"
            "- Never allow INSERT, UPDATE, DELETE, DROP, ALTER, or PRAGMA\n"
        ),
    )

    return _base_agent(config, llm_service, _empty_tool_registry())


def create_sql_agent():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError("Database not found. Run setup_database.py first.")

    llm_service = _build_llm_service()

    from vanna import Agent, AgentConfig
    from vanna.core.registry import ToolRegistry
    from vanna.integrations.sqlite import SqliteRunner
    from vanna.integrations.local.agent_memory import DemoAgentMemory
    from vanna.tools import RunSqlTool, VisualizeDataTool
    from vanna.tools.agent_memory import (
        SaveQuestionToolArgsTool,
        SearchSavedCorrectToolUsesTool,
    )

    sql_runner = SqliteRunner(database_path=DB_PATH)
    memory = DemoAgentMemory()

    tool_registry = ToolRegistry()
    tool_registry.register_local_tool(RunSqlTool(sql_runner=sql_runner), ["*"])
    tool_registry.register_local_tool(VisualizeDataTool(), ["*"])
    tool_registry.register_local_tool(SaveQuestionToolArgsTool(), ["*"])
    tool_registry.register_local_tool(SearchSavedCorrectToolUsesTool(), ["*"])

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
            "patients(id, first_name, last_name, email, phone, date_of_birth, gender, city, registered_date)\n"
            "doctors(id, name, specialization, department, phone)\n"
            "appointments(id, patient_id, doctor_id, appointment_date, status, notes)\n"
            "treatments(id, appointment_id, treatment_name, cost, duration_minutes)\n"
            "invoices(id, patient_id, invoice_date, total_amount, paid_amount, status)\n\n"
            "IMPORTANT:\n"
            "- patients table DOES NOT have a 'name' column\n"
            "- Use full name as: first_name || ' ' || last_name\n\n"
            "RULES:\n"
            "- Use ONLY the tables listed above\n"
            "- Never invent tables like patient_records or transactions\n"
            "- Always use correct column names\n\n"
            "QUERY GUIDELINES:\n"
            "- COUNT(*) for totals\n"
            "- SUM(total_amount) for revenue\n"
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
            "SELECT SUM(total_amount) FROM invoices\n\n"
            "If unsure, return the closest valid SQL using available tables.\n"
        ),
    )

    return Agent(
        config=config,
        llm_service=llm_service,
        tool_registry=tool_registry,
        agent_memory=memory,
        user_resolver=DefaultUserResolver(),
    )
