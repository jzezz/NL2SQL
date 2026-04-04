import re


def extract_sql(text: str):
    """
    Extract SQL from model output reliably.
    """

    if not text:
        return None

    # Remove markdown formatting
    text = text.replace("```sql", "").replace("```", "")

    # Extract SELECT query
    match = re.search(r"SELECT[\s\S]*", text, re.IGNORECASE)

    if not match:
        return None

    sql = match.group(0).strip()

    # Remove trailing semicolon
    sql = sql.rstrip(";").strip()

    return sql


def validate_sql(sql: str):
    """
    Keep validation simple and correct.
    Do NOT over-restrict.
    """

    if not sql:
        return False

    sql_clean = sql.strip().lower()

    # Must start with SELECT
    if not sql_clean.startswith("select"):
        return False

    # Must contain FROM
    if " from " not in sql_clean:
        return False

    # Block only dangerous operations
    forbidden = ["insert", "update", "delete", "drop", "alter"]

    for word in forbidden:
        if word in sql_clean:
            return False

    return True