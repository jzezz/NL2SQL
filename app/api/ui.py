from fastapi import APIRouter
from fastapi.responses import HTMLResponse


router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def home():
    return HTMLResponse(
        content="""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>NL2SQL Vanna AI</title>
  <style>
    :root {
      --bg: #f6f5f2;
      --panel: #ffffff;
      --panel-2: #fafafa;
      --text: #111827;
      --muted: #6b7280;
      --border: #e5e7eb;
      --accent: #111827;
      --accent-soft: #f3f4f6;
      --success: #16a34a;
      --danger: #dc2626;
      --warning: #b45309;
      --shadow: 0 22px 60px rgba(17, 24, 39, 0.08);
      --radius: 22px;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: "Segoe UI Variable", "Segoe UI", ui-sans-serif, system-ui, sans-serif;
      color: var(--text);
      background:
        radial-gradient(circle at top left, rgba(17,24,39,0.06), transparent 28%),
        radial-gradient(circle at top right, rgba(17,24,39,0.04), transparent 24%),
        linear-gradient(180deg, #fbfbfa 0%, #f3f4f1 100%);
      min-height: 100vh;
    }
    .shell {
      max-width: 1200px;
      margin: 0 auto;
      padding: 32px 20px 48px;
    }
    .topbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      margin-bottom: 28px;
    }
    .brand {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .brand h1 {
      margin: 0;
      font-size: clamp(2rem, 5vw, 3.2rem);
      letter-spacing: -0.04em;
      line-height: 0.95;
    }
    .brand p {
      margin: 0;
      color: var(--muted);
      font-size: 0.98rem;
    }
    .pill {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      border: 1px solid var(--border);
      background: rgba(255,255,255,0.7);
      backdrop-filter: blur(12px);
      color: var(--muted);
      padding: 10px 14px;
      border-radius: 999px;
      font-size: 0.88rem;
      box-shadow: 0 6px 24px rgba(0,0,0,0.03);
    }
    .grid {
      display: grid;
      grid-template-columns: 1.1fr 0.9fr;
      gap: 20px;
    }
    .card {
      background: rgba(255,255,255,0.86);
      backdrop-filter: blur(10px);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
    }
    .card-header {
      padding: 20px 20px 0;
    }
    .card-body {
      padding: 20px;
    }
    .section-title {
      margin: 0 0 6px;
      font-size: 1rem;
      letter-spacing: -0.02em;
    }
    .section-subtitle {
      margin: 0;
      color: var(--muted);
      font-size: 0.92rem;
      line-height: 1.5;
    }
    .textarea {
      width: 100%;
      min-height: 126px;
      border-radius: 16px;
      border: 1px solid var(--border);
      background: var(--panel);
      color: var(--text);
      padding: 16px;
      font: inherit;
      resize: vertical;
      outline: none;
      box-shadow: inset 0 1px 0 rgba(255,255,255,0.7);
    }
    .textarea:focus {
      border-color: #c7cdd6;
      box-shadow: 0 0 0 4px rgba(17,24,39,0.06);
    }
    .row {
      display: flex;
      gap: 12px;
      align-items: center;
      flex-wrap: wrap;
    }
    .button {
      appearance: none;
      border: 0;
      border-radius: 14px;
      padding: 12px 16px;
      background: var(--accent);
      color: white;
      cursor: pointer;
      font-weight: 600;
      font-size: 0.95rem;
      transition: transform .15s ease, opacity .15s ease, background .15s ease;
    }
    .button:hover { transform: translateY(-1px); }
    .button:disabled { opacity: 0.55; cursor: not-allowed; transform: none; }
    .button .spinner {
      display: inline-block;
      width: 14px;
      height: 14px;
      border: 2px solid rgba(255,255,255,0.38);
      border-top-color: #fff;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
      vertical-align: -2px;
      margin-right: 8px;
    }
    .button.secondary {
      background: var(--accent-soft);
      color: var(--text);
      border: 1px solid var(--border);
    }
    .chips {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 14px;
    }
    .chip {
      border: 1px solid var(--border);
      background: #fff;
      color: var(--text);
      border-radius: 999px;
      padding: 9px 12px;
      font-size: 0.88rem;
      cursor: pointer;
      transition: background .15s ease, transform .15s ease;
    }
    .chip:hover {
      background: #f8fafc;
      transform: translateY(-1px);
    }
    .meta {
      display: grid;
      gap: 12px;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      margin-top: 16px;
    }
    .stat {
      padding: 14px;
      border: 1px solid var(--border);
      border-radius: 16px;
      background: var(--panel-2);
    }
    .stat span {
      display: block;
      color: var(--muted);
      font-size: 0.82rem;
      margin-bottom: 6px;
    }
    .stat strong {
      font-size: 1rem;
      letter-spacing: -0.02em;
    }
    .output {
      display: grid;
      gap: 14px;
    }
    .output-box {
      border: 1px solid var(--border);
      border-radius: 16px;
      background: #fff;
      overflow: hidden;
    }
    .output-box header {
      padding: 12px 14px;
      border-bottom: 1px solid var(--border);
      background: #fcfcfc;
      font-size: 0.88rem;
      font-weight: 600;
    }
    .output-box pre {
      margin: 0;
      padding: 14px;
      overflow: auto;
      white-space: pre-wrap;
      word-break: break-word;
      font-size: 0.92rem;
      line-height: 1.55;
    }
    .skeleton {
      display: grid;
      gap: 10px;
    }
    .skeleton-line {
      height: 12px;
      border-radius: 999px;
      background: linear-gradient(90deg, #eceff3 0%, #f8fafc 45%, #eceff3 100%);
      background-size: 220% 100%;
      animation: shimmer 1.5s ease-in-out infinite;
    }
    .table-wrap {
      overflow: auto;
      border-radius: 16px;
      border: 1px solid var(--border);
      background: #fff;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.92rem;
    }
    th, td {
      padding: 12px 14px;
      text-align: left;
      border-bottom: 1px solid #f0f1f3;
      vertical-align: top;
    }
    th {
      color: #374151;
      background: #fcfcfc;
      font-weight: 600;
      position: sticky;
      top: 0;
    }
    .status {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      color: var(--muted);
      font-size: 0.9rem;
    }
    .dot {
      width: 10px;
      height: 10px;
      border-radius: 999px;
      background: #9ca3af;
    }
    .dot.ok { background: var(--success); }
    .dot.err { background: var(--danger); }
    .chart {
      display: grid;
      gap: 10px;
    }
    .bar-row {
      display: grid;
      grid-template-columns: minmax(120px, 220px) 1fr 72px;
      gap: 12px;
      align-items: center;
    }
    .bar-label {
      font-size: 0.92rem;
      color: #374151;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .bar-track {
      height: 12px;
      border-radius: 999px;
      background: #eef2f7;
      overflow: hidden;
    }
    .bar-fill {
      height: 100%;
      border-radius: inherit;
      background: linear-gradient(90deg, #111827, #374151);
    }
    .chart-empty, .panel-empty {
      border: 1px dashed #d9dee5;
      border-radius: 16px;
      background: linear-gradient(180deg, #fff, #fcfcfc);
      padding: 18px;
      color: var(--muted);
      font-size: 0.92rem;
      line-height: 1.55;
    }
    .toast {
      position: fixed;
      right: 18px;
      bottom: 18px;
      z-index: 50;
      min-width: 280px;
      max-width: min(380px, calc(100vw - 36px));
      padding: 14px 15px;
      border-radius: 16px;
      border: 1px solid var(--border);
      background: rgba(255,255,255,0.94);
      box-shadow: 0 14px 40px rgba(17,24,39,0.12);
      transform: translateY(18px);
      opacity: 0;
      pointer-events: none;
      transition: opacity .2s ease, transform .2s ease;
      display: flex;
      gap: 12px;
      align-items: flex-start;
    }
    .toast.show {
      opacity: 1;
      transform: translateY(0);
      pointer-events: auto;
    }
    .toast .toast-dot {
      width: 10px;
      height: 10px;
      border-radius: 999px;
      margin-top: 6px;
      background: var(--accent);
      flex: 0 0 auto;
    }
    .toast.success .toast-dot { background: var(--success); }
    .toast.error .toast-dot { background: var(--danger); }
    .toast.warning .toast-dot { background: var(--warning); }
    .toast strong {
      display: block;
      margin-bottom: 3px;
      font-size: 0.92rem;
    }
    .toast p {
      margin: 0;
      color: var(--muted);
      font-size: 0.88rem;
      line-height: 1.45;
    }
    .toast button {
      margin-left: auto;
      border: 0;
      background: transparent;
      color: var(--muted);
      cursor: pointer;
      font-size: 1.1rem;
      line-height: 1;
    }
    @keyframes shimmer {
      0% { background-position: 220% 0; }
      100% { background-position: -220% 0; }
    }
    @keyframes spin {
      to { transform: rotate(360deg); }
    }
    .footer-note {
      margin-top: 14px;
      color: var(--muted);
      font-size: 0.85rem;
      line-height: 1.5;
    }
    @media (max-width: 980px) {
      .grid { grid-template-columns: 1fr; }
      .meta { grid-template-columns: 1fr; }
    }
    @media (max-width: 640px) {
      .shell { padding: 18px 14px 28px; }
      .topbar { align-items: flex-start; flex-direction: column; }
      .bar-row { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <div class="shell">
    <div class="topbar">
      <div class="brand">
        <div class="pill">NL2SQL Vanna AI</div>
        <h1>Ask your database in plain English.</h1>
        <p>A minimal, shadcn-inspired interface for querying the clinic database and reviewing SQL output.</p>
      </div>
      <div class="pill" id="health-pill"><span class="dot" id="health-dot"></span><span id="health-text">Checking backend...</span></div>
    </div>

    <div class="grid">
      <section class="card">
        <div class="card-header">
          <h2 class="section-title">Query</h2>
          <p class="section-subtitle">Ask a question, then review the generated SQL, results, and chart data.</p>
        </div>
        <div class="card-body">
          <textarea id="question" class="textarea" placeholder="For example: Show total revenue by month"></textarea>
          <div class="row" style="margin-top: 14px;">
            <button class="button" id="run-btn"><span id="run-btn-label">Run query</span></button>
            <button class="button secondary" id="clear-btn">Clear</button>
          </div>
          <div class="chips" id="examples">
            <button class="chip" data-q="How many patients do we have?">How many patients do we have?</button>
            <button class="chip" data-q="List all doctors">List all doctors</button>
            <button class="chip" data-q="Show total revenue">Show total revenue</button>
            <button class="chip" data-q="Top 5 patients by spending">Top 5 patients by spending</button>
          </div>

          <div class="meta">
            <div class="stat"><span>Status</span><strong id="result-status">Idle</strong></div>
            <div class="stat"><span>Rows</span><strong id="result-rows">-</strong></div>
            <div class="stat"><span>SQL</span><strong id="result-sql">-</strong></div>
          </div>
        </div>
      </section>

      <section class="card">
        <div class="card-header">
          <h2 class="section-title">Output</h2>
          <p class="section-subtitle">The response comes back as structured JSON, so it is easy to debug and extend.</p>
        </div>
        <div class="card-body output">
          <div class="output-box">
            <header>Message</header>
            <div id="message-wrap" class="panel-empty">Run a query to see the summary.</div>
          </div>
          <div class="output-box">
            <header>SQL Query</header>
            <pre id="sql" style="margin:0;">-</pre>
          </div>
          <div class="output-box">
            <header>Agent Trace</header>
            <pre id="agent-trace" style="margin:0;">Planner and verifier output will appear here after a query runs.</pre>
          </div>
        </div>
      </section>
    </div>

    <div class="grid" style="margin-top: 20px;">
      <section class="card">
        <div class="card-header">
          <h2 class="section-title">Results</h2>
          <p class="section-subtitle">Rows returned from SQLite.</p>
        </div>
        <div class="card-body">
          <div class="table-wrap" id="table-wrap">
            <table>
              <thead><tr id="table-head"><th>No data yet</th></tr></thead>
              <tbody id="table-body"><tr><td>Run a query to populate this table.</td></tr></tbody>
            </table>
          </div>
        </div>
      </section>

      <section class="card">
        <div class="card-header">
          <h2 class="section-title">Chart</h2>
          <p class="section-subtitle">A simple visual preview when the response includes chart-friendly data.</p>
        </div>
        <div class="card-body">
          <div id="chart" class="chart">
            <div class="chart-empty">Chart rendering will appear here when the API returns chart data.</div>
          </div>
        </div>
      </section>
    </div>
  </div>

  <div class="toast" id="toast" role="status" aria-live="polite">
    <div class="toast-dot"></div>
    <div>
      <strong id="toast-title">Ready</strong>
      <p id="toast-message">Ask a question to begin.</p>
    </div>
    <button id="toast-close" aria-label="Dismiss notification">×</button>
  </div>

  <script>
    const questionEl = document.getElementById('question');
    const runBtn = document.getElementById('run-btn');
    const runBtnLabel = document.getElementById('run-btn-label');
    const clearBtn = document.getElementById('clear-btn');
    const messageWrap = document.getElementById('message-wrap');
    const sqlEl = document.getElementById('sql');
    const agentTraceEl = document.getElementById('agent-trace');
    const resultRowsEl = document.getElementById('result-rows');
    const resultStatusEl = document.getElementById('result-status');
    const resultSqlEl = document.getElementById('result-sql');
    const tableHead = document.getElementById('table-head');
    const tableBody = document.getElementById('table-body');
    const chartEl = document.getElementById('chart');
    const healthText = document.getElementById('health-text');
    const healthDot = document.getElementById('health-dot');
    const toast = document.getElementById('toast');
    const toastTitle = document.getElementById('toast-title');
    const toastMessage = document.getElementById('toast-message');
    const toastClose = document.getElementById('toast-close');
    let toastTimer = null;

    document.getElementById('examples').addEventListener('click', (event) => {
      const button = event.target.closest('[data-q]');
      if (!button) return;
      questionEl.value = button.dataset.q;
      questionEl.focus();
    });

    clearBtn.addEventListener('click', () => {
      questionEl.value = '';
      setMessage('Run a query to see the summary.', 'panel-empty');
      sqlEl.textContent = '-';
      agentTraceEl.textContent = 'Planner and verifier output will appear here after a query runs.';
      resultRowsEl.textContent = '-';
      resultStatusEl.textContent = 'Idle';
      resultSqlEl.textContent = '-';
      renderEmptyTable();
      renderEmptyChart();
      showToast('Cleared', 'The page is reset and ready for a new query.', 'warning');
    });

    runBtn.addEventListener('click', runQuery);
    questionEl.addEventListener('keydown', (event) => {
      if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
        runQuery();
      }
    });

    async function checkHealth() {
      try {
        const response = await fetch('/health');
        const data = await response.json();
        if (data.status === 'ok') {
          healthText.textContent = 'Backend online';
          healthDot.classList.add('ok');
          showToast('Backend connected', 'FastAPI and SQLite are responding normally.', 'success');
          return;
        }
        throw new Error('Unexpected health payload');
      } catch (error) {
        healthText.textContent = 'Backend offline';
        healthDot.classList.add('err');
        showToast('Backend offline', 'Check that uvicorn is still running on port 8000.', 'error');
      }
    }

    async function runQuery() {
      const question = questionEl.value.trim();
      if (!question) {
        questionEl.focus();
        showToast('Add a question', 'Type a natural language question before running a query.', 'warning');
        return;
      }

      runBtn.disabled = true;
      runBtnLabel.innerHTML = '<span class="spinner"></span>Running';
      resultStatusEl.textContent = 'Running...';
      setMessage('Thinking...', 'panel-empty');
      sqlEl.textContent = 'Generating SQL...';
      agentTraceEl.textContent = 'Planner is classifying the question...';
      resultSqlEl.textContent = '...';
      resultRowsEl.textContent = '...';
      renderEmptyTable('Loading results...');
      renderEmptyChart('Waiting for chart data...');
      showToast('Query started', 'Generating SQL and fetching rows from SQLite.', 'warning');

      try {
        const response = await fetch('/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ question })
        });

        const data = await response.json();
        if (!response.ok || !data.success) {
          throw new Error(data.error || 'Query failed');
        }

        resultStatusEl.textContent = 'Success';
        setMessage(data.message || 'Query completed.', 'panel-empty');
        sqlEl.textContent = data.sql_query || '-';
        agentTraceEl.textContent = formatAgentTrace(data);
        resultSqlEl.textContent = data.sql_query || '-';
        resultRowsEl.textContent = String(data.row_count ?? data.rows?.length ?? 0);

        renderTable(data.columns || [], data.rows || []);
        renderChart(data.chart);
        showToast('Query complete', 'The response has been loaded into the table and chart areas.', 'success');
      } catch (error) {
        resultStatusEl.textContent = 'Error';
        setMessage(error.message || 'Something went wrong.', 'panel-empty');
        sqlEl.textContent = '-';
        agentTraceEl.textContent = formatAgentTrace({ error: error.message || 'Something went wrong.' }, true);
        resultSqlEl.textContent = '-';
        resultRowsEl.textContent = '-';
        renderEmptyTable('No results to display.');
        renderEmptyChart('No chart available.');
        showToast('Query failed', error.message || 'Something went wrong.', 'error');
      } finally {
        runBtn.disabled = false;
        runBtnLabel.textContent = 'Run query';
      }
    }

    function renderEmptyTable(message = 'Run a query to populate this table.') {
      tableHead.innerHTML = '<th>No data yet</th>';
      tableBody.innerHTML = `<tr><td>${escapeHtml(message)}</td></tr>`;
    }

    function renderTable(columns, rows) {
      if (!columns.length || !rows.length) {
        renderEmptyTable('No rows returned.');
        return;
      }

      tableHead.innerHTML = columns.map((column) => `<th>${escapeHtml(column)}</th>`).join('');
      tableBody.innerHTML = rows.map((row) => {
        const values = Array.isArray(row) ? row : columns.map((column) => row[column]);
        return `<tr>${values.map((value) => `<td>${formatValue(value)}</td>`).join('')}</tr>`;
      }).join('');
    }

    function renderEmptyChart(message) {
      chartEl.innerHTML = `<div class="chart-empty">${escapeHtml(message)}</div>`;
    }

    function renderChart(chart) {
      if (!chart || !chart.x || !chart.y || !chart.x.length) {
        renderEmptyChart('This query did not return chart data.');
        return;
      }

      const values = chart.y.map((value) => Number(value) || 0);
      const max = Math.max(...values, 1);
      chartEl.innerHTML = chart.x.map((label, index) => {
        const value = values[index] || 0;
        const width = Math.max((value / max) * 100, 4);
        return `
          <div class="bar-row">
            <div class="bar-label">${escapeHtml(String(label))}</div>
            <div class="bar-track"><div class="bar-fill" style="width:${width}%"></div></div>
            <div style="text-align:right;color:#6b7280;">${escapeHtml(String(chart.y[index]))}</div>
          </div>
        `;
      }).join('');
    }

    function setMessage(text, className) {
      messageWrap.className = className;
      messageWrap.textContent = text;
    }

    function showToast(title, message, tone = 'success') {
      clearTimeout(toastTimer);
      toast.className = `toast show ${tone}`;
      toastTitle.textContent = title;
      toastMessage.textContent = message;
      toastTimer = setTimeout(hideToast, 4200);
    }

    function hideToast() {
      toast.className = 'toast';
    }

    function formatValue(value) {
      if (value === null || value === undefined) return '<span style="color:#9ca3af;">null</span>';
      if (typeof value === 'number') return String(value);
      return escapeHtml(String(value));
    }

    function formatAgentTrace(data, errorMode = false) {
      const trace = {
        plan: data?.plan || null,
        planner_output: data?.planner_output || null,
        verification: data?.verification || null,
        verifier_output: data?.verifier_output || null
      };
      if (errorMode) {
        trace.error = data?.error || 'Unknown error';
      }
      return JSON.stringify(trace, null, 2);
    }

    function escapeHtml(text) {
      return text
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#39;');
    }

    toastClose.addEventListener('click', hideToast);

    checkHealth();
  </script>
</body>
</html>
        """.strip()
    )
