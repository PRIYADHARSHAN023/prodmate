from fastapi import FastAPI, HTTPException, Request
import httpx
from loguru import logger
import os
import sys

# ------------------------------
# FIX: Add shared folder to path
# ------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), "prodmate"))
SHARED_PATH = os.path.join(BASE_DIR, "shared")
sys.path.append(SHARED_PATH)
# ------------------------------

from shared.models import UserRequest, AgentResponse

app = FastAPI()
AGENT_URLS = {
    "task_manager": os.getenv("TASK_AGENT","http://localhost:8101"),
    "schedule": os.getenv("SCHEDULE_AGENT","http://localhost:8102"),
    "reminder": os.getenv("REMINDER_AGENT","http://localhost:8103"),
    "memory": os.getenv("MEMORY_AGENT","http://localhost:8104"),
    "search": os.getenv("SEARCH_AGENT","http://localhost:8105"),
}

@app.on_event("startup")
def startup():
    logger.add("logs/coordinator.log", rotation="5 MB", backtrace=True, diagnose=True)
    logger.info("Coordinator starting")

@app.post("/api/v1/handle")
async def handle(req: UserRequest, request: Request):
    text = req.text.lower()
    
    # naive dispatch rules
    if "task" in text or "todo" in text or "add task" in text:
        agent = "task_manager"
    elif "schedule" in text or "availability" in text:
        agent = "schedule"
    elif "remind" in text or "reminder" in text:
        agent = "reminder"
    elif "remember" in text or "preference" in text:
        agent = "memory"
    else:
        agent = "search"

    url = f"{AGENT_URLS[agent]}/tool/run"
    headers = {"X-Trace-Id": req.request_id}

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(url, json=req.dict(), headers=headers)

    if r.status_code != 200:
        logger.error(f"Agent {agent} error: {r.text}")
        raise HTTPException(status_code=500, detail="Agent error")

    resp = AgentResponse(**r.json())
    logger.info(f"Request {req.request_id} routed to {agent} -> {resp.status}")
    return resp.dict()

@app.post("/api/v1/operation/{op_id}/complete")
async def complete_op(op_id: str, decision: dict):
    agent = "reminder"
    url = f"{AGENT_URLS[agent]}/operation/{op_id}/complete"

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(url, json=decision)

    if r.status_code != 200:
        raise HTTPException(status_code=500, detail="Operation completion failed")

    return r.json()

