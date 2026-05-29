# ⬡ NEXUS BI — Natural Language Business Intelligence Agent

A production-grade BI system that translates plain English questions into validated SQL queries, executes them against MySQL, and returns AI-generated business insights — wrapped in a premium dark-futuristic dashboard UI.

---

## Architecture

```
bi_agent/
├── backend/
│   ├── __init__.py
│   ├── main.py        ← FastAPI app + all endpoints
│   ├── llm.py         ← LLM (Groq) logic: generate, retry, narrate
│   ├── validator.py   ← Intent classification + SQL validation
│   ├── executor.py    ← MySQL connection pool + execution
│   └── config.py      ← Pydantic settings from .env
├── frontend/
│   └── app.py         ← Streamlit premium UI
├── schema.sql         ← DB setup + sample data
├── requirements.txt
├── .env.example
└── README.md
```

---

## Setup

### 1. Clone & Install

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your credentials:
#   GROQ_API_KEY   → from https://console.groq.com
#   DB_PASSWORD    → your MySQL root password
```

### 3. Initialize Database

```bash
mysql -u root -p < schema.sql
```

### 4. Start Backend (FastAPI)

```bash
# From the bi_agent/ root directory:
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

API docs available at: http://localhost:8000/docs

### 5. Start Frontend (Streamlit)

```bash
streamlit run frontend/app.py
```

Opens at: http://localhost:8501

---

## API Endpoints

| Method | Endpoint        | Description                              |
|--------|----------------|------------------------------------------|
| POST   | `/ask`          | Full pipeline: question → SQL → results → narration |
| POST   | `/validate_sql` | Validate a raw SQL string                |
| POST   | `/execute_sql`  | Execute a validated SQL string           |
| POST   | `/narrate`      | AI narration from columns + results      |
| GET    | `/health`       | Service health check                     |

### `/ask` Request & Response

```json
// Request
{ "question": "What are the top 5 customers by total spend?" }

// Response
{
  "question": "...",
  "sql": "SELECT ...",
  "columns": ["name", "total_spend"],
  "results": [["Alice Johnson", 1729.97], ...],
  "narration": "Alice Johnson leads with $1,729.97 in lifetime spend...",
  "guardrail_status": "SAFE",   // SAFE | BLOCKED | REWRITTEN
  "logs": ["[INTENT CHECK] Safe analytical intent", ...],
  "attempts": 1
}
```

---

## Security Model

### Guardrail Layers

1. **Intent Classification** — Regex blocks: `drop`, `delete`, `update`, `alter`, `truncate`, `insert`, `create`, `grant`, `revoke`, `exec`
2. **SQL Validation** — `sqlglot` AST parse ensures only `SELECT` statements
3. **Table Allowlist** — Only `customers`, `orders`, `order_items`, `products`
4. **Length Limit** — SQL capped at 1,000 chars to prevent injection
5. **LIMIT Injection** — `LIMIT 100` appended if absent
6. **Connection Pool** — Scoped, non-admin MySQL user recommended

### Retry System

- Attempt 1: Use generated SQL
- Attempt 2: Regenerate with error feedback
- Attempt 3: Hard reset — regenerate from scratch
- Max 3 attempts before failing gracefully

---

## Frontend Features

- **Dark futuristic theme** — deep graphite, neon amber, electric violet
- **Orbitron + Sora + JetBrains Mono** typography
- **3-panel layout**: Query Input · SQL · AI Insight
- **Live execution logs** with color-coded prefixes
- **Guardrail badge**: SAFE / BLOCKED / REWRITTEN
- **Syntax-highlighted SQL** with keyword colorization
- **Interactive results table** with CSV export
- **Animated canvas**: flowing data streams + relational node graph
- **Glassmorphism panels** with hover glow effects

---

## Allowed Tables & Schema

```sql
customers   (customer_id, name, email, city, country, created_at)
orders      (order_id, customer_id, order_date, status, total_amount)
order_items (item_id, order_id, product_id, quantity, unit_price)
products    (product_id, name, category, price, stock_quantity)
```

---

## Example Questions

```
What are our top 10 customers by total revenue?
Show monthly order volume for 2024
Which product categories generate the most revenue?
How many orders are in each status?
What is the average order value by country?
Show products with low stock (under 30 units)
Which customers have placed more than 2 orders?
```

---

## Production Notes

- Use a **read-only MySQL user** scoped to `bi_agent` database
- Run FastAPI behind **nginx** with SSL
- Add **rate limiting** via `slowapi` for the `/ask` endpoint
- Consider **Redis caching** for repeated identical queries
- Replace Groq with OpenAI/Anthropic for higher reliability in production
