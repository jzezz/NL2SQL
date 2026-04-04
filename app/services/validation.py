import re


# Allowed tables to prevent hallucinated SQL
ALLOWED_TABLES = {
    "patients",
    "doctors",
    "appointments",
    "treatments",
    "invoices"
}


def clean_text(text: str):
    """
    Removes markdown and unnecessary formatting from LLM output.
    """

    if not text:
        return ""

    # Remove ```sql, ```sqlite etc
    text = re.sub(r"```[a-zA-Z]*", "", text)
    text = text.replace("```", "")

    return text.strip()


def extract_sql(text: str):
    """
    Robust SQL extraction from LLM output.
    Handles:
    - markdown
    - explanations
    - multiline queries
    - repeated attempts
    """

    if not text:
        return None

    text = clean_text(text)

    # Find all SELECT queries
    matches = re.findall(
        r"(SELECT[\s\S]+?)(?:;|$)",
        text,
        re.IGNORECASE
    )

    if not matches:
        return None

    # Take last query (usually most refined)
    sql = matches[-1].strip()

    # Normalize
    sql = re.sub(r"\s+", " ", sql)
    sql = sql.rstrip(";").strip()

    return sql


def validate_sql(sql: str):
    """
    Validates SQL safety and structure.
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

    # Block destructive queries
    forbidden = ["insert", "update", "delete", "drop", "alter"]

    for word in forbidden:
        if word in sql_clean:
            return False

    return True


def contains_valid_tables(sql: str):
    """
    Validates that only allowed tables are used.
    Supports:
    - JOINs
    - aliases
    - subqueries
    """

    if not sql:
        return False

    sql_lower = sql.lower()

    # Extract tables after FROM and JOIN
    tables = re.findall(
        r"(?:from|join)\s+([a-zA-Z_][a-zA-Z0-9_]*)",
        sql_lower
    )

    if not tables:
        return False

    for table in tables:
        if table not in ALLOWED_TABLES:
            print("Invalid table detected:", table)
            return False

    return True