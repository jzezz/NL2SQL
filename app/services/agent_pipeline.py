import json
import re

from vanna.core.user import User

from app.agent.vanna_setup import (
    create_planner_agent,
    create_sql_agent,
    create_verifier_agent,
)


def _extract_text_from_stream(stream):
    async def collect():
        response_text = ""
        async for chunk in stream:
            if hasattr(chunk, "simple_component") and chunk.simple_component:
                response_text += getattr(chunk.simple_component, "text", "")
        return response_text

    return collect()


def _extract_json(text: str):
    if not text:
        return None

    text = text.strip()

    try:
        return json.loads(text)
    except Exception:
        pass

    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        return None

    candidate = match.group(0)
    try:
        return json.loads(candidate)
    except Exception:
        return None


async def _run_agent(agent, prompt: str):
    user = User(id="default_user")
    stream = agent.send_message(user, prompt)
    return await _extract_text_from_stream(stream)


async def plan_question(question: str):
    agent = create_planner_agent()
    prompt = (
        "Classify the user question.\n"
        f"Question: {question}"
    )
    text = await _run_agent(agent, prompt)
    return _extract_json(text) or {
        "intent": "other",
        "needs_chart": False,
        "suggested_granularity": "none",
        "notes": "Fallback planner output"
    }, text


async def generate_sql(question: str, plan: dict | None = None):
    agent = create_sql_agent()
    user = User(id="default_user")

    schema_context = (
        "Database Schema:\n"
        "patients(id, first_name, last_name, email, phone, date_of_birth, gender, city, registered_date)\n"
        "doctors(id, name, specialization, department, phone)\n"
        "appointments(id, patient_id, doctor_id, appointment_date, status, notes)\n"
        "treatments(id, appointment_id, treatment_name, cost, duration_minutes)\n"
        "invoices(id, patient_id, invoice_date, total_amount, paid_amount, status)\n\n"
    )

    plan_text = json.dumps(plan or {}, ensure_ascii=False)
    prompts = [
        schema_context + f"Planner JSON: {plan_text}\nReturn ONLY SQL.\nQuestion: {question}",
        schema_context + f"STRICT: Only SQL. No explanation.\nPlanner JSON: {plan_text}\nQuestion: {question}",
        schema_context + f"Use ONLY given tables. No hallucination.\nPlanner JSON: {plan_text}\nQuestion: {question}",
    ]

    last_response = ""
    for prompt in prompts:
        try:
            stream = agent.send_message(user, prompt)
        except Exception as e:
            return None, str(e)

        response_text = await _extract_text_from_stream(stream)
        last_response = response_text

        match = re.search(r"(SELECT[\s\S]+?)(?:;|$)", response_text, re.IGNORECASE)
        if not match:
            continue

        sql = re.sub(r"\s+", " ", match.group(1)).strip().rstrip(";")
        if sql:
            return sql, response_text

    return None, last_response


async def verify_sql(question: str, sql: str, plan: dict | None = None):
    agent = create_verifier_agent()
    payload = {
        "question": question,
        "plan": plan or {},
        "sql": sql
    }
    prompt = (
        "Review this SQL for a SQLite clinic database.\n"
        f"{json.dumps(payload, ensure_ascii=False)}\n\n"
        "Return JSON only."
    )

    text = await _run_agent(agent, prompt)
    return _extract_json(text) or {
        "approved": False,
        "corrected_sql": "",
        "reason": "Fallback verifier output"
    }, text
