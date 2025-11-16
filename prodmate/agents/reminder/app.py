from fastapi import FastAPI
from shared.models import UserRequest, AgentResponse
from uuid import uuid4
from loguru import logger

app = FastAPI()
operations = {}

@app.on_event("startup")
def startup():
    logger.add("logs/reminder.log", rotation="5 MB")

@app.post("/tool/run")
async def run_tool(req: UserRequest):
    text = req.text.lower()
    if "set reminder" in text or "remind me" in text:
        op_id = str(uuid4())
        operations[op_id] = {"req": req.dict(), "status":"pending"}
        return AgentResponse(request_id=req.request_id, agent="reminder", status="pending",
                             operation_id=op_id,
                             result={"message":"Waiting user confirmation","operation_id":op_id}).dict()
    return AgentResponse(request_id=req.request_id, agent="reminder", status="ok",
                         result={"message":"No reminder action matched"}).dict()

@app.post("/operation/{op_id}/complete")
async def complete(op_id: str, decision: dict):
    op = operations.get(op_id)
    if not op:
        return {"error":"operation not found"}, 404
    op["status"] = "completed"
    # in prod you'd schedule reminder; here we return ok
    return {"operation_id":op_id, "status":"completed"}
