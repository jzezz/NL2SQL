# NL2SQL Vanna AI

A natural language to SQL interface for querying a clinic database using Vanna AI and LLMs. Ask questions in plain English and get SQL queries, results, and charts.

## Features

- **Natural Language Queries**: Ask questions like "How many patients do we have?" or "Show total revenue by month"
- **Automatic SQL Generation**: Uses LLMs to generate safe, validated SQL
- **Interactive Web UI**: Clean, responsive interface for querying and viewing results
- **Data Visualization**: Automatic chart generation (bar, line, pie) for numeric results
- **Multi-LLM Support**: Works with Google Gemini, Groq, or OpenAI
- **Production Ready**: Deployed on Vercel with serverless SQLite

## Tech Stack

- **Backend**: FastAPI, Python 3.11+
- **LLM Integration**: Vanna AI (supports Gemini, Groq, OpenAI)
- **Database**: SQLite with synthetic clinic data
- **Frontend**: Vanilla HTML/CSS/JS (no build step)
- **Deployment**: Vercel (serverless)

## Screenshots

### Home Page
![Home Page](docs/home%20page.png)

### SQL Statement
![SQL Statement](docs/SQl%20statement.png)

### Result Table
![Result Table](docs/result%20table.png)

## Quick Start

### Prerequisites

- Python 3.11+
- LLM API key (choose one):
  - **Groq** (free, recommended) — https://console.groq.com
  - **OpenAI** — https://platform.openai.com
  - **Google Gemini** — https://aistudio.google.com/apikey

### Local Development

```bash
# Clone and enter
git clone https://github.com/your-username/nl2sql-vanna-ai.git
cd nl2sql-vanna-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Initialize database
python scripts/setup_database.py

# Run server
uvicorn app.main:app --reload
```

Open http://localhost:8000

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `LLM_PROVIDER` | Yes | `groq`, `openai`, or `google` |
| `LLM_API_KEY` | Yes* | API key for chosen provider |
| `LLM_MODEL` | No | Model name (defaults per provider) |
| `LLM_BASE_URL` | No | Custom base URL (for proxies) |
| `GOOGLE_API_KEY` | Yes* | Required if `LLM_PROVIDER=google` |
| `DATABASE_PATH` | No | SQLite path (default: `data/clinic.db`) |

*Only required for the selected provider.

**Example `.env` for Groq:**
```env
LLM_PROVIDER=groq
LLM_API_KEY=gsk_your_groq_key
LLM_MODEL=llama3-8b-8192
```

## Deploy to Vercel

1. Push this repo to GitHub
2. Import project in Vercel
3. Add Environment Variables in Vercel Dashboard → Settings → Environment Variables:
   - `LLM_PROVIDER` = `groq`
   - `LLM_API_KEY` = `gsk_...`
3. Deploy

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Web UI |
| `GET` | `/health` | Health check + diagnostics |
| `GET` | `/test-llm` | Test LLM connectivity |
| `POST` | `/chat` | Execute NL query |

### `/chat` Request
```json
{ "question": "How many patients?" }
```

### `/chat` Response
```json
{
  "success": true,
  "question": "How many patients?",
  "message": "Total count is 200.",
  "sql_query": "SELECT COUNT(*) FROM patients",
  "columns": ["COUNT(*)"],
  "rows": [[200]],
  "row_count": 1,
  "chart": { "type": "bar", "x": ["Total"], "y": [200], ... }
}
```

## Database Schema

The app uses a synthetic clinic database with 5 tables:

| Table | Rows | Description |
|-------|------|-------------|
| `patients` | 200 | Patient demographics |
| `doctors` | 15 | Doctor info |
| `appointments` | 500 | Appointment records |
| `treatments` | 350 | Treatments per appointment |
| `invoices` | 300 | Billing records |

## Project Structure

```
nl2sql-vanna-ai/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── api/
│   │   ├── routes.py        # /chat endpoint
│   │   ├── health.py        # /health, /test-llm
│   │   └── ui.py            # Web UI (HTML)
│   ├── core/
│   │   ├── config.py        # Settings & env vars
│   │   └── database.py      # DB connection + initialization
│   ├── services/
│   │   ├── nl2sql_service.py    # Main pipeline
│   │   ├── agent_pipeline.py    # Planner → SQL → Verifier
│   │   ├── validation.py        # SQL safety checks
│   │   ├── chart_service.py     # Chart data generation
│   │   └── openai_llm.py        # Custom OpenAI-compatible LLM service
│   └── agent/
│       └── vanna_setup.py       # Vanna agent configuration
├── scripts/
│   ├── setup_database.py    # Creates DB + synthetic data
│   └── seed_memory.py       # Optional Vanna memory seeding
├── vercel.json              # Vercel deployment config
├── requirements.txt
└── .env.example
```

## LLM Providers Comparison

| Provider | Free Tier | Best Model | Cost |
|----------|-----------|------------|------|
| **Groq** | ✅ Generous | `llama3-8b-8192` | Free |
| OpenAI | ❌ Pay-per-use | `gpt-4o-mini` | ~$0.15/1M tokens |
| Google Gemini | ✅ Limited | `gemini-2.0-flash` | Free (quota limited) |

## Contributing

1. Fork the repo
2. Create a feature branch
3. Commit your changes
4. Open a PR

## License

MIT License - feel free to use for any purpose.