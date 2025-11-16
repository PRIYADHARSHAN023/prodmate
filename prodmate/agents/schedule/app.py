from fastapi import FastAPI
from shared.models import UserRequest, AgentResponse
from shared.memory import LongTermMemory
from uuid import uuid4
from loguru import logger

app = FastAPI()
mem = LongTermMemory()

@app.on_event("startup")
def startup():
    logger.add("logs/schedule.log", rotation="5 MB")

@app.post("/tool/run")
async def run_tool(req: UserRequest):
    # naive free-slot mock
    result = {"free_slots": ["2025-11-20T10:00","2025-11-20T15:00"], "note":"Mock free slots"}
    return AgentResponse(request_id=req.request_id, agent="schedule", status="ok", result=result).dict()
