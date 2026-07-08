# NL2SQL Vanna AI

NL2SQL Vanna AI is a FastAPI-based natural language to SQL application. It lets a user ask questions in plain English, turns those questions into SQL with a Vanna/Gemini agent pipeline, verifies the SQL for safety, runs it against a SQLite clinic database, and returns structured results in both JSON and a browser UI.

## What The Project Does

The project provides an end-to-end NL2SQL workflow:

- Accepts a question in plain English
- Plans the request with an AI agent
- Generates SQL from the question
- Verifies and corrects the SQL before execution
- Runs the query against a SQLite database
- Returns rows, columns, row count, and a short summary
- Produces lightweight chart data when the query is chart-friendly
- Exposes both a web UI and API docs

## Features

- Natural language to SQL generation
- Multi-agent pipeline for planning, generation, and verification
- SQL safety checks to block destructive queries
- SQLite clinic database with seeded sample data
- FastAPI backend with `/chat` and `/health` endpoints
- Simple browser UI at `/`
- Swagger/OpenAPI docs at `/docs`
- Clean result formatting with summary text
- Chart preview support for analytical queries
- Easy local development setup

## Tech Stack

- Python 3.10+
- FastAPI
- Vanna AI
- Google Gemini
- SQLite
- Vanilla HTML, CSS, and JavaScript

## Project Structure

- `app/main.py` - FastAPI entry point
- `app/api/ui.py` - web UI served at `/`
- `app/api/routes.py` - `/chat` API route
- `app/api/health.py` - health check route
- `app/agent/vanna_setup.py` - agent setup and Gemini configuration
- `app/services/agent_pipeline.py` - planner, SQL generator, and verifier flow
- `app/services/nl2sql_service.py` - full question processing pipeline
- `scripts/setup_database.py` - creates and seeds the SQLite database
- `data/clinic.db` - generated database file

## Installation

### 1. Clone the repository

```powershell
git clone https://github.com/iYashrajPatil/nlp2sql-vanna-ai.git
cd nl2sql-vanna-ai
```

### 2. Create a virtual environment

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Create the `.env` file

Create a file named `.env` in the project root and add your Gemini API key:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

Optional:

```env
DATABASE_PATH=data/clinic.db
```

### 5. Set up the database

```powershell
python scripts/setup_database.py
```

### 6. Start the app

```powershell
uvicorn app.main:app --reload
```

## Usage

Open the app in your browser:

- UI: `http://127.0.0.1:8000/`
- API docs: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`

### Example Questions

- How many patients do we have?
- List all doctors
- Show total revenue
- Top 5 patients by spending
- Show appointments for this month

### API Example

`POST /chat`

Request:

```json
{
  "question": "How many patients do we have?"
}
```

Response:

```json
{
  "success": true,
  "question": "How many patients do we have?",
  "message": "Total count is 200.",
  "sql_query": "SELECT COUNT(*) FROM patients",
  "columns": ["COUNT(*)"],
  "rows": [[200]],
  "row_count": 1,
  "chart": null
}
```

## Screenshots

Add screenshots of the UI and API response here.

Suggested files:

- `docs/screenshots/home.png`
- `docs/screenshots/query-result.png`
- `docs/screenshots/swagger.png`

Example layout:

```md
![Home](docs/screenshots/home.png)
![Query Result](docs/screenshots/query-result.png)
![Swagger Docs](docs/screenshots/swagger.png)
```

## Development Notes

- The app uses a SQLite database stored in `data/clinic.db`
- The database is created and seeded by `scripts/setup_database.py`
- The agent pipeline includes planning, SQL generation, and verification
- The UI is intentionally minimal and clean rather than flashy

## Troubleshooting

### Missing database

Run:

```powershell
python scripts/setup_database.py
```

### Missing API key

Make sure `.env` contains:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

### Dependency issues

Run:

```powershell
pip install -r requirements.txt
```

### Server not starting

Run:

```powershell
uvicorn app.main:app --reload
```

## Summary

NL2SQL Vanna AI is a practical AI-assisted SQL querying system that combines a simple UI, a safe execution pipeline, and multi-agent reasoning to make database querying easier for non-technical users.
