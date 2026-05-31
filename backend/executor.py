import mysql.connector
from mysql.connector import pooling
from config import settings



connection_pool = pooling.MySQLConnectionPool(
    pool_name="bi_agent_pool",
    pool_size=5,
    host=settings.DB_HOST,
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    database=settings.DB_NAME,
    connect_timeout=10
)


def execute_sql(sql: str) -> tuple[list, list]:
    conn = connection_pool.get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        cols = [d[0] for d in cursor.description]
        cursor.close()
        return cols, results
    finally:
        conn.close()


def test_connection() -> bool:
    try:
        conn = connection_pool.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        return True
    except Exception:
        return False
