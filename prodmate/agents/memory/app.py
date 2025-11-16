from fastapi import FastAPI
from shared.models import UserRequest, AgentResponse
from shared.memory import LongTermMemory
from loguru import logger

app = FastAPI()
mem = LongTermMemory()

@app.on_event("startup")
def startup():
    logger.add("logs/memory.log", rotation="5 MB")

@app.post("/tool/run")
async def run_tool(req: UserRequest):
    text = req.text
    # simple commands: "remember: I wake at 6"
    if ":" in text:
        k,v = text.split(":",1)
        key = k.strip().lower()
        val = v.strip()
        mem.set(f"{req.user_id}:{key}", val)
        return AgentResponse(request_id=req.request_id, agent="memory", status="ok",
                             result={"message":"saved","key":key,"value":val}).dict()
    # read memory
    if "what do i" in text.lower() or "remember" in text.lower():
        # naive read all for user
        res = {k:v for k,v in mem.find_prefix(f"{req.user_id}:").items()}
        return AgentResponse(request_id=req.request_id, agent="memory", status="ok",
                             result={"memory":res}).dict()
    return AgentResponse(request_id=req.request_id, agent="memory", status="ok",
                         result={"message":"no action"}).dict()
