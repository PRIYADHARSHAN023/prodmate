from fastapi import FastAPI, Request
from shared.models import UserRequest, AgentResponse
from shared.memory import LongTermMemory
from uuid import uuid4
from loguru import logger

app = FastAPI()
mem = LongTermMemory()

@app.on_event("startup")
def startup():
    logger.add("logs/task_manager.log", rotation="5 MB")

@app.post("/tool/run")
async def run_tool(req: UserRequest):
    text = req.text
    if ":" in text:
        parts = text.split(":",1)
        payload = parts[1].strip()
    else:
        payload = text
    task_id = str(uuid4())
    mem.set(f"task:{req.user_id}:{task_id}", {"text": payload, "done": False})
    return AgentResponse(request_id=req.request_id, agent="task_manager", status="ok",
                         result={"task_id": task_id, "text": payload}).dict()
