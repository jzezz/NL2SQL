def generate_chart(columns, rows, question: str):
    """
    Generates chart data for frontend.

    Supports:
    - Bar chart (default)
    - Line chart (time-based queries)
    - Pie chart (distribution queries)
    """

    if not rows or not columns:
        return None

    # Need at least 2 columns for visualization
    if len(columns) < 2:
        return None

    try:
        x = [row[0] for row in rows]
        y = [row[1] for row in rows]

        question_lower = question.lower()

        # Decide chart type based on query intent
        if "distribution" in question_lower or "share" in question_lower:
            chart_type = "pie"
        elif "trend" in question_lower or "over time" in question_lower or "date" in columns[0].lower():
            chart_type = "line"
        else:
            chart_type = "bar"

        return {
            "type": chart_type,
            "x": x,
            "y": y,
            "x_label": columns[0],
            "y_label": columns[1]
        }

    except Exception:
        return None