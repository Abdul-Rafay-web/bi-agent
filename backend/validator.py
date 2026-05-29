import re
from sqlglot import parse_one
from sqlglot.expressions import Select, Table

MAX_SQL_LENGTH = 1000

DANGEROUS_INTENTS = [
    "drop", "delete", "update", "alter",
    "truncate", "insert", "create", "grant",
    "revoke", "exec", "execute", "xp_", "sp_"
]

ALLOWED_TABLES = [
    "customers",
    "orders",
    "order_items",
    "products"
]


def classify_intent(question: str) -> tuple[bool, str]:
    q = question.lower()
    for word in DANGEROUS_INTENTS:
        if re.search(r'\b' + re.escape(word) + r'\b', q):
            return False, f"Blocked dangerous intent: '{word}'"
    return True, "Safe analytical intent"


def clean_sql(sql: str) -> str:
    sql = sql.replace("```sql", "").replace("```", "")
    sql = re.sub(r'--[^\n]*', '', sql)
    sql = re.sub(r'/\*.*?\*/', '', sql, flags=re.DOTALL)
    return sql.strip()


def add_limit(sql: str) -> str:
    if "LIMIT" not in sql.upper():
        return sql.rstrip(";") + " LIMIT 100"
    return sql


def validate_sql(sql: str) -> tuple[bool, str]:
    if not sql or sql.strip() == "":
        return False, "Empty SQL"

    if len(sql) > MAX_SQL_LENGTH:
        return False, "SQL too long — possible injection attempt"

    upper = sql.upper().strip()
    dangerous_keywords = ["DROP", "DELETE", "UPDATE", "ALTER", "TRUNCATE",
                          "INSERT", "CREATE", "GRANT", "REVOKE", "EXEC", "EXECUTE"]
    for kw in dangerous_keywords:
        if re.search(r'\b' + kw + r'\b', upper):
            return False, f"Only SELECT allowed — found: {kw}"

    try:
        parsed = parse_one(sql, dialect="mysql")
    except Exception as e:
        return False, f"Syntax error: {e}"

    if not isinstance(parsed, Select):
        return False, "Only SELECT allowed"

    tables = list(parsed.find_all(Table))
    for t in tables:
        if t.name.lower() not in ALLOWED_TABLES:
            return False, f"Invalid table: '{t.name}' — allowed: {ALLOWED_TABLES}"

    return True, "OK"
