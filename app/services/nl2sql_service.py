from vanna.core.user import User
from app.agent.vanna_setup import create_agent
from app.core.database import get_connection
from app.services.validation import extract_sql, validate_sql, contains_valid_tables
from app.services.chart_service import generate_chart


def generate_summary(question: str, rows: list):
    """
    Generates a meaningful summary based on result structure.
    """

    if not rows:
        return "No data found for the given query."

    q = question.lower()

    # Count queries
    if "how many" in q or "count" in q:
        return f"Total count is {rows[0][0]}."

    # Revenue / aggregation
    if "revenue" in q or "sum" in q:
        # If grouped result (multiple rows)
        if len(rows) > 1:
            return f"Showing revenue distribution for {len(rows)} patients."
        else:
            return f"Total revenue is {rows[0][0]}."

    return f"Query returned {len(rows)} rows."


def fix_common_sql_errors(sql: str) -> str:
    """
    Fix schema mismatches without breaking correct column names.
    """

    if not sql:
        return sql

    # Fix hallucinated tables
    sql = sql.replace("patient_records", "patients")
    sql = sql.replace("transactions", "invoices")

    # Fix patient name issue
    sql = sql.replace("p.name", "p.first_name || ' ' || p.last_name")

    # Fix ONLY incorrect amount usage (safe replacements)
    sql = sql.replace("i.amount", "i.total_amount")
    sql = sql.replace(" amount ", " total_amount ")

    return sql


async def generate_sql(question: str, agent, user):
    """
    Generates SQL using Vanna agent with retry + correction.
    """

    schema_context = (
        "Database Schema:\n"
        "patients(id, first_name, last_name, age, gender)\n"
        "doctors(id, name, specialization)\n"
        "appointments(id, patient_id, doctor_id, date)\n"
        "treatments(id, patient_id, description, cost)\n"
        "invoices(id, patient_id, invoice_date, total_amount, paid_amount, status)\n\n"
    )

    attempts = [
        schema_context + f"Return ONLY SQL.\nQuestion: {question}",
        schema_context + f"STRICT: Only SQL. No explanation.\nQuestion: {question}",
        schema_context + f"Use ONLY given tables. No hallucination.\nQuestion: {question}",
    ]

    last_response = ""

    for attempt in attempts:
        try:
            stream = agent.send_message(user, attempt)
        except Exception as e:
            print("LLM ERROR:", str(e))
            return None, str(e)

        response_text = ""

        async for chunk in stream:
            if hasattr(chunk, "simple_component") and chunk.simple_component:
                response_text += getattr(chunk.simple_component, "text", "")

        last_response = response_text

        sql = extract_sql(response_text)

        print("\nMODEL OUTPUT:\n", response_text)
        print("EXTRACTED SQL:\n", sql)

        if not sql:
            continue

        sql = sql.strip().rstrip(";")

        # Apply correction layer
        sql = fix_common_sql_errors(sql)

        # Validate
        if validate_sql(sql) and contains_valid_tables(sql):
            return sql, response_text

    return None, last_response


async def process_question(question: str):
    """
    Full NL → SQL → Execution pipeline.
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
            columns = [col[0] for col in cursor.description]

        conn.close()

        message = generate_summary(question, rows)
        chart = generate_chart(columns, rows, question)

        return {
            "success": True,
            "question": question,
            "message": message,
            "sql_query": sql,
            "columns": columns,
            "rows": rows,
            "row_count": len(rows),
            "chart": chart
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "sql_query": sql
        }