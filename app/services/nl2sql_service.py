from vanna.core.user import User
from app.agent.vanna_setup import create_agent
from app.core.database import get_connection
from app.services.validation import extract_sql, validate_sql


async def generate_sql(question: str, agent, user):
    """
    Generate SQL from natural language.
    Retries once with stricter instruction if needed.
    """

    attempts = [
        question,
        f"Return ONLY a valid SQLite SELECT query. No explanation.\n\nQuestion: {question}"
    ]

    for attempt in attempts:
        stream = agent.send_message(user, attempt)

        response_text = ""

        async for chunk in stream:
            if hasattr(chunk, "simple_component") and chunk.simple_component:
                response_text += getattr(chunk.simple_component, "text", "")

        sql = extract_sql(response_text)

        print("\nMODEL OUTPUT:\n", response_text)
        print("EXTRACTED SQL:\n", sql)

        if sql and validate_sql(sql):
            return sql, response_text

    return None, response_text


async def process_question(question: str):
    """
    End-to-end pipeline:
    Question → SQL → Execute → Response
    """

    agent = create_agent()
    user = User(id="default_user")

    sql, model_output = await generate_sql(question, agent, user)

    if not sql:
        return {
            "success": False,
            "error": "Model failed to generate valid SQL",
            "model_output": model_output
        }

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(sql)

        rows = cursor.fetchall()

        columns = []
        if cursor.description:
            columns = [desc[0] for desc in cursor.description]

        conn.close()

        return {
            "success": True,
            "question": question,
            "sql": sql,
            "columns": columns,
            "rows": rows,
            "row_count": len(rows)
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "sql": sql
        }