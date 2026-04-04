# NL2SQL System using Vanna AI

## Overview

This project implements a Natural Language to SQL (NL2SQL) system using Vanna AI.  
The system allows users to ask questions in plain English and automatically converts them into SQL queries, executes them on a SQLite database, and returns structured results along with optional visualizations.

The system is designed to be robust, accurate, and aligned with real-world database querying scenarios.

---

## Features

- Convert natural language questions into SQL queries
- Execute queries on a SQLite database
- Return structured results (columns, rows, row count)
- Generate charts for analytical queries
- Handle hallucinations and schema mismatches
- Retry mechanism for improving SQL generation
- Validation layer to ensure safe SQL execution

---

## Tech Stack

- Python 3.10
- FastAPI
- Vanna AI
- Google Gemini (LLM)
- SQLite
- Plotly (for visualization)

---

## Project Structure
```
nl2sql-vanna-ai/
│
├── app/
│ ├── main.py # FastAPI entry point
│ ├── agent/
│ │ └── vanna_setup.py # Vanna agent configuration
│ ├── api/
│ │ └── routes.py # API endpoints (/chat)
│ ├── core/
│ │ └── database.py # Database connection
│ ├── services/
│ │ ├── nl2sql_service.py # NL → SQL → Execution pipeline
│ │ ├── validation.py # SQL extraction & validation
│ │ └── chart_service.py # Chart generation
│
├── scripts/
│ ├── setup_database.py
│ └── seed_memory.py
│
├── data/
│ └── clinic.db
│
├── tests/
│
├── requirements.txt
├── README.md
```

---

## Setup Instructions

### 1. Clone the repository
git clone https://github.com/iYashrajPatil/nlp2sql-vanna-ai
```
cd nl2sql-vanna-ai
```

---

### 2. Create virtual environment (Windows PowerShell)
```
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install dependencies
```
pip install -r requirements.txt
```

---

### 4. Configure environment variables

Create a `.env` file in the root:
GOOGLE_API_KEY=your_gemini_api_key

---

### 5. Setup database
```
python scripts/setup_database.py
```
---

### 6. Run the application
```
uvicorn app.main:app --reload
```

Open:http://127.0.0.1:8000/docs


---

## API Usage

### POST `/chat`

#### Request:
```json
{
  "question": "Show revenue per patient"
}
```
## Response
```json
{
  "success": true,
  "sql_query": "...",
  "columns": [...],
  "rows": [...],
  "chart": {...}
}
```
---
## Example Queries

- How many patients do we have?
- List all patients
- Show all appointments
- Total revenue generated
- Show revenue per patient
- Top 5 patients by spending

---
## Challenges Faced & Solutions

### 1. LLM Hallucination
- Issue: The model sometimes generated non-existent tables such as `transactions` or `patient_records`.
- Solution:
  - Added strict schema definitions in the prompt
  - Implemented table validation to allow only known tables
  - Added a correction layer to replace common hallucinated table names

---

### 2. Schema Mismatch
- Issue: The model used incorrect column names like `amount` instead of actual columns such as `total_amount` or `paid_amount`.
- Solution:
  - Updated prompt with exact database schema
  - Added runtime SQL correction logic to fix column mismatches
  - Verified schema using SQLite PRAGMA queries

---

### 3. Inconsistent SQL Output
- Issue: The model sometimes returned explanations or markdown instead of raw SQL.
- Solution:
  - Enforced strict instruction: "Output ONLY SQL"
  - Implemented retry mechanism with stricter prompts
  - Built a robust SQL extraction function to clean responses

---

### 4. SQL Extraction Issues
- Issue: SQL queries were not always correctly extracted from model responses.
- Solution:
  - Implemented regex-based extraction for multi-line queries
  - Removed markdown and extra text before processing
  - Selected the last valid SQL query from multiple attempts

---

### 5. SQL Safety and Validation
- Issue: Risk of unsafe queries (INSERT, DELETE, etc.) or invalid syntax.
- Solution:
  - Allowed only SELECT queries
  - Blocked destructive keywords (INSERT, UPDATE, DELETE, DROP, ALTER)
  - Ensured queries contain valid structure (SELECT + FROM)

---

### 6. Retry and Reliability
- Issue: Model responses were sometimes inconsistent.
- Solution:
  - Implemented multi-attempt SQL generation strategy
  - Used progressively stricter prompts in retries
  - Accepted only validated SQL outputs

---

## Design Decisions

- Used Vanna AI for structured agent-based SQL generation
- Separated system into clear layers:
  - Agent (SQL generation)
  - Validation (safety and correctness)
  - Execution (database interaction)
- Added deterministic validation and correction to reduce dependency on LLM accuracy
- Used SQLite for simplicity and portability

---

## Limitations

- Complex queries with deep nesting may still require multiple attempts
- System performance depends on LLM response quality
- Chart generation is basic and can be enhanced further
- No user authentication or multi-user support

---

## Future Improvements

- Add caching for repeated queries
- Improve visualization intelligence and chart selection
- Support multiple database types (PostgreSQL, MySQL)
- Add user authentication and session management
- Improve handling of complex analytical queries

---

## Conclusion

This project demonstrates a robust NL2SQL system that converts natural language into executable SQL queries with high reliability.

Key strengths of the system:
- Strong schema grounding to reduce hallucination
- SQL validation and correction layer for safety
- Reliable execution pipeline with retry logic
- Clean API interface with optional visualization support

The system is designed with real-world considerations and provides a solid foundation for scalable AI-driven data querying applications.

