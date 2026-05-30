from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from config import settings

model = ChatGroq(
    model_name=settings.GROQ_MODEL,
    temperature=0,
    api_key=settings.GROQ_API_KEY
)

SYSTEM_PROMPT = """
You are a MySQL SQL compiler for a Business Intelligence system.

Available tables and their columns:
- customers (customer_id, name, email, city, country, created_at)
- orders (order_id, customer_id, order_date, status, total_amount)
- order_items (item_id, order_id, product_id, quantity, unit_price)
- products (product_id, name, category, price, stock_quantity)

STRICT RULES:
- Output ONLY raw SQL
- No markdown, no explanations, no comments, no code fences
- Only SELECT queries allowed
- Always use proper MySQL syntax
- Use table aliases for clarity in JOINs
- If request is unsafe or impossible return exactly: SELECT NULL;
"""

RETRY_PROMPT = """
The previous SQL generation failed.
Error: {error}

Generate a corrected MySQL SELECT query using only these tables:
customers, orders, order_items, products

Return ONLY raw SQL. No explanations.
"""

NARRATION_PROMPT = """
You are a senior BI analyst at a top-tier technology company.

Your task: Interpret the query results and deliver a crisp, insightful business narrative.

Rules:
- DO NOT generate or mention SQL
- Speak as a confident analyst, not a chatbot
- Focus on business implications, trends, and actionable observations
- Keep it under 150 words
- Use precise numbers from the results
- Highlight the most significant finding first

Question: {question}
SQL Used: {sql}
Columns: {columns}
Results (first 20 rows): {results}
"""


def generate_sql(question: str) -> str:
    response = model.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=question)
    ])
    return response.content.strip()


def regenerate_sql(question: str, error: str) -> str:
    formatted_retry = RETRY_PROMPT.format(error=error)
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=question),
        SystemMessage(content=formatted_retry)
    ]
    response = model.invoke(messages)
    return response.content.strip()


def narrate_results(question: str, sql: str, columns: list, results: list) -> str:
    preview = results[:20]
    response = model.invoke([
        SystemMessage(content=NARRATION_PROMPT.format(
            question=question,
            sql=sql,
            columns=columns,
            results=preview
        ))
    ])
    return response.content.strip()
