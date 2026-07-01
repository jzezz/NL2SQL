# Run From Scratch

This guide shows how to set up and run the project from a clean machine or fresh clone.

## 1. Prerequisites

- Python 3.10 or newer
- A Gemini API key from Google
- Git

## 2. Clone Or Open The Project

If you already have the project folder, open it in your editor.

If you are starting from a fresh clone:

```powershell
git clone https://github.com/iYashrajPatil/nlp2sql-vanna-ai
cd nl2sql-vanna-ai
```

## 3. Create A Virtual Environment

From the project root:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
venv\Scripts\Activate.ps1
```

## 4. Install Dependencies

Install the Python packages:

```powershell
pip install -r requirements.txt
```

## 5. Add Environment Variables

Create a file named `.env` in the project root.

File path:

`D:\vs code\python\nl2sql\nlp2sql-vanna-ai\.env`

Add your Gemini key:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

Optional:

```env
DATABASE_PATH=data/clinic.db
```

## 6. Build The Database

Create and seed the SQLite database:

```powershell
python scripts/setup_database.py
```

This creates:

`data/clinic.db`

## 7. Start The Backend

Run the FastAPI app:

```powershell
uvicorn app.main:app --reload
```

If your system uses a different Python launcher, run the command from the same virtual environment you activated earlier.

## 8. Open The App

Open these URLs in the browser:

- UI: `http://127.0.0.1:8000/`
- API docs: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`

## 9. Test The Project

Try these prompts in the UI or the `/chat` endpoint:

- How many patients do we have?
- List all doctors
- Show total revenue
- Top 5 patients by spending

## 10. If Something Fails

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

Reinstall packages:

```powershell
pip install -r requirements.txt
```

### Server not updating

Stop the running server and start it again with:

```powershell
uvicorn app.main:app --reload
```

## Suggested Start Order

1. Create the virtual environment
2. Install dependencies
3. Add `.env`
4. Seed the database
5. Start the server
6. Open the UI
7. Test `/chat`

