from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

from .llm import generate_sql, regenerate_sql, narrate_results
from .validator import classify_intent, validate_sql, clean_sql, add_limit
from .executor import execute_sql

app = FastAPI(title="BI Agent API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_RETRIES = 3


class QuestionRequest(BaseModel):
    question: str


class SQLRequest(BaseModel):
    sql: str


class NarrateRequest(BaseModel):
    question: str
    sql: str
    columns: list
    results: list


class AskResponse(BaseModel):
    question: str
    sql: str
    columns: list
    results: list
    narration: str
    guardrail_status: str
    logs: list[str]
    attempts: int


@app.post("/ask", response_model=AskResponse)
async def ask(request: QuestionRequest):
    logs = []
    question = request.question.strip()
    guardrail_status = "SAFE"

    # Step 1: Intent classification
    logs.append(f"[INTENT CHECK] Analyzing: '{question}'")
    safe, message = classify_intent(question)
    if not safe:
        guardrail_status = "BLOCKED"
        logs.append(f"[BLOCKED] {message}")
        raise HTTPException(status_code=400, detail={
            "message": message,
            "guardrail_status": guardrail_status,
            "logs": logs
        })

    logs.append(f"[INTENT CHECK] {message}")

    # Step 2: Generate SQL
    logs.append("[LLM] Generating SQL from question...")
    sql = generate_sql(question)
    sql = clean_sql(sql)
    logs.append(f"[LLM] Raw SQL: {sql}")

    # Step 3: Retry loop
    final_sql = sql
    attempts = 0

    for attempt in range(MAX_RETRIES):
        attempts = attempt + 1

        if attempt == 2:
            logs.append("[RETRY] Hard reset — regenerating SQL from scratch...")
            final_sql = generate_sql(question)
            final_sql = clean_sql(final_sql)
            guardrail_status = "REWRITTEN"

        is_safe, msg = validate_sql(final_sql)
        logs.append(f"[VALIDATE] Attempt {attempts}: {msg}")

        if not is_safe:
            if "syntax error" in msg.lower():
                logs.append(f"[RETRY] Syntax error detected — regenerating...")
                final_sql = regenerate_sql(question, msg)
                final_sql = clean_sql(final_sql)
                guardrail_status = "REWRITTEN"
                logs.append(f"[RETRY] New SQL: {final_sql}")
                continue
            elif "invalid table" in msg.lower():
                guardrail_status = "BLOCKED"
                logs.append(f"[BLOCKED] {msg}")
                raise HTTPException(status_code=400, detail={
                    "message": msg,
                    "guardrail_status": guardrail_status,
                    "logs": logs
                })
            elif "only select allowed" in msg.lower():
                guardrail_status = "BLOCKED"
                logs.append(f"[BLOCKED] Non-SELECT query rejected")
                raise HTTPException(status_code=400, detail={
                    "message": "Only SELECT queries are permitted.",
                    "guardrail_status": guardrail_status,
                    "logs": logs
                })
            else:
                guardrail_status = "BLOCKED"
                logs.append(f"[BLOCKED] {msg}")
                raise HTTPException(status_code=400, detail={
                    "message": msg,
                    "guardrail_status": guardrail_status,
                    "logs": logs
                })

        # Step 4: Execute
        try:
            safe_sql = add_limit(final_sql)
            logs.append(f"[EXECUTE] Running: {safe_sql}")
            cols, results = execute_sql(safe_sql)
            logs.append(f"[EXECUTE] Success — {len(results)} rows returned")

            # Step 5: Narrate
            logs.append("[NARRATE] Generating business insight...")
            narration = narrate_results(question, safe_sql, cols, results)
            logs.append("[NARRATE] Complete")

            serializable_results = [list(row) for row in results]

            return AskResponse(
                question=question,
                sql=safe_sql,
                columns=cols,
                results=serializable_results,
                narration=narration,
                guardrail_status=guardrail_status,
                logs=logs,
                attempts=attempts
            )

        except Exception as e:
            err = str(e).lower()
            logs.append(f"[ERROR] Execution failed: {e}")

            if "unknown column" in err or "syntax" in err:
                final_sql = regenerate_sql(question, str(e))
                final_sql = clean_sql(final_sql)
                guardrail_status = "REWRITTEN"
                logs.append(f"[RETRY] Corrected SQL: {final_sql}")
            else:
                raise HTTPException(status_code=500, detail={
                    "message": f"Database error: {e}",
                    "guardrail_status": "ERROR",
                    "logs": logs
                })

    logs.append("[FAIL] Max retries reached")
    raise HTTPException(status_code=500, detail={
        "message": "Failed after maximum retries.",
        "guardrail_status": "ERROR",
        "logs": logs
    })


@app.post("/validate_sql")
async def validate_sql_endpoint(request: SQLRequest):
    sql = clean_sql(request.sql)
    is_valid, message = validate_sql(sql)
    return {"valid": is_valid, "message": message, "sql": sql}


@app.post("/execute_sql")
async def execute_sql_endpoint(request: SQLRequest):
    sql = clean_sql(request.sql)
    is_valid, msg = validate_sql(sql)
    if not is_valid:
        raise HTTPException(status_code=400, detail=msg)
    try:
        safe_sql = add_limit(sql)
        cols, results = execute_sql(safe_sql)
        return {"columns": cols, "results": [list(r) for r in results], "row_count": len(results)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/narrate")
async def narrate_endpoint(request: NarrateRequest):
    narration = narrate_results(request.question, request.sql, request.columns, request.results)
    return {"narration": narration}


@app.get("/health")
async def health():
    return {"status": "ok", "service": "BI Agent API"}


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
