# NL2SQL Vanna AI

A modern natural-language-to-SQL application built with FastAPI, Vanna AI, Gemini, and SQLite. The app lets you ask questions in plain English, generates SQL, verifies the query, executes it against a clinic database, and returns structured results with an optional chart preview.

## What It Does

- Converts plain English questions into SQL
- Uses a planner agent, SQL agent, and verifier agent
- Runs safe `SELECT` queries against SQLite
- Returns rows, columns, row count, and a short summary
- Generates lightweight chart data for analytics questions
- Includes a clean web UI and FastAPI docs

## Tech Stack

- Python 3.10+
- FastAPI
- Vanna AI
- Google Gemini
- SQLite
- HTML, CSS, and vanilla JavaScript for the UI

## Project Layout

- `app/main.py` - FastAPI entry point
- `app/api/ui.py` - Web UI served at `/`
- `app/api/routes.py` - `/chat` API endpoint
- `app/api/health.py` - health check endpoint
- `app/agent/vanna_setup.py` - agent setup and LLM configuration
- `app/services/agent_pipeline.py` - planner, SQL generator, and verifier flow
- `app/services/nl2sql_service.py` - end-to-end question handling
- `scripts/setup_database.py` - database creation and seeding
- `data/clinic.db` - generated SQLite database

## Features

- Natural language question answering
- Multi-agent flow for better reliability
- SQL validation and correction
- SQLite-backed clinic schema
- Interactive browser UI
- Swagger/OpenAPI docs
- Fast local development workflow

## Prerequisites

- Python 3.10 or newer
- Git
- A Google Gemini API key

## Local Setup

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

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Create `.env`

Create a file named `.env` in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

Optional:

```env
DATABASE_PATH=data/clinic.db
```

### 5. Create the database

```powershell
python scripts/setup_database.py
```

### 6. Run the backend

```powershell
uvicorn app.main:app --reload
```

### 7. Open the app

- UI: http://127.0.0.1:8000/
- API docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

## Example Questions

- How many patients do we have?
- List all doctors
- Show total revenue
- Top 5 patients by spending
- Show appointments for this month

## How To Push To GitHub

If the remote is already configured, use:

```powershell
git status
git add .
git commit -m "Polish UI and add agent pipeline"
git push origin main
```

If you want to verify the remote first:

```powershell
git remote -v
```

## Deploying To Vercel

Important: this project uses SQLite, so Vercel is best for a demo or light usage. For production workloads, a managed external database is a better fit.

### Vercel setup steps

1. Push your latest code to GitHub.
2. Go to [Vercel](https://vercel.com/) and create a new project.
3. Import the GitHub repository `nlp2sql-vanna-ai`.
4. Vercel should detect the Python/FastAPI app from `app/main.py` because the file exports a FastAPI instance named `app`.
5. Add the environment variable:
   - `GOOGLE_API_KEY`
6. In the project settings, set the Build Command to:

```bash
python scripts/setup_database.py
```

7. Keep the output directory empty.
8. Deploy the project.
9. After deployment, test:
   - `/` for the UI
   - `/docs` for the API docs
   - `/health` for the health check

### Notes about Vercel

- Vercel Python support runs FastAPI as a serverless function.
- The FastAPI app is configured with `vercel.json` to allow a longer function duration.
- Because serverless deployments are stateless, SQLite is best treated as a demo database unless you move to an external hosted database.

## Vercel Config

The repo includes `vercel.json` with a `maxDuration` setting for the FastAPI function.

## Troubleshooting

### Missing Gemini key

Make sure `.env` contains `GOOGLE_API_KEY` locally or the same variable is set in Vercel.

### Database missing

Run:

```powershell
python scripts/setup_database.py
```

### Dependency issues

Run:

```powershell
pip install -r requirements.txt
```

### API not responding

Restart the server:

```powershell
uvicorn app.main:app --reload
```

## Summary

This project demonstrates a practical NL2SQL system with a clean UI, a multi-agent backend, SQL safety checks, and a ready-to-run clinic database.
