from app.core.database import get_connection
from app.services.agent_pipeline import plan_question, generate_sql, verify_sql
from app.services.validation import validate_sql, contains_valid_tables
from app.services.chart_service import generate_chart


def generate_summary(question: str, rows: list):
    """
    Generates a meaningful summary based on result structure.
    """

    if not rows:
        return "No data found for the given query."

    q = question.lower()

    if "how many" in q or "count" in q:
        return f"Total count is {rows[0][0]}."

    if "revenue" in q or "sum" in q:
        if len(rows) > 1:
            return f"Showing revenue distribution for {len(rows)} patients."
        return f"Total revenue is {rows[0][0]}."

    return f"Query returned {len(rows)} rows."


def fix_common_sql_errors(sql: str) -> str:
    """
    Fix schema mismatches without breaking correct column names.
    """

    if not sql:
        return sql

    sql = sql.replace("patient_records", "patients")
    sql = sql.replace("transactions", "invoices")
    sql = sql.replace("p.name", "p.first_name || ' ' || p.last_name")
    sql = sql.replace("i.amount", "i.total_amount")

    return sql


async def process_question(question: str):
    """
    Full NL -> Plan -> SQL -> Verify -> Execute pipeline.
    """

    plan, planner_output = await plan_question(question)
    sql, model_output = await generate_sql(question, plan)

    if not sql:
        error_detail = model_output or "Unknown error"
        return {
            "success": False,
            "error": f"Model failed: {error_detail[:500]}",
            "model_output": model_output,
            "plan": plan,
            "planner_output": planner_output,
        }

    sql = fix_common_sql_errors(sql.strip().rstrip(";"))

    verification, verifier_output = await verify_sql(question, sql, plan)
    corrected_sql = (verification or {}).get("corrected_sql") or sql
    corrected_sql = fix_common_sql_errors(corrected_sql.strip().rstrip(";"))

    if verification and not verification.get("approved", False):
        if validate_sql(corrected_sql) and contains_valid_tables(corrected_sql):
            sql = corrected_sql
        else:
            return {
                "success": False,
                "error": verification.get("reason", "Verifier rejected the SQL"),
                "sql_query": corrected_sql,
                "plan": plan,
                "planner_output": planner_output,
                "verification": verification,
                "verifier_output": verifier_output,
            }
    else:
        sql = corrected_sql

    if not (validate_sql(sql) and contains_valid_tables(sql)):
        return {
            "success": False,
            "error": "SQL failed validation after verification",
            "sql_query": sql,
            "plan": plan,
            "planner_output": planner_output,
            "verification": verification,
            "verifier_output": verifier_output,
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
        chart = generate_chart(columns, rows, question) if plan.get("needs_chart", True) else None

        return {
            "success": True,
            "question": question,
            "message": message,
            "sql_query": sql,
            "columns": columns,
            "rows": rows,
            "row_count": len(rows),
            "chart": chart,
            "plan": plan,
            "planner_output": planner_output,
            "verification": verification,
            "verifier_output": verifier_output,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "sql_query": sql,
            "plan": plan,
            "planner_output": planner_output,
            "verification": verification,
            "verifier_output": verifier_output,
        }
