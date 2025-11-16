from fastapi import FastAPI
from shared.models import UserRequest, AgentResponse
from loguru import logger

app = FastAPI()

@app.on_event("startup")
def startup():
    logger.add("logs/search.log", rotation="5 MB")

@app.post("/tool/run")
async def run_tool(req: UserRequest):
    # prototype: return canned response
    q = req.text
    return AgentResponse(request_id=req.request_id, agent="search", status="ok",
                         result={"answer": f"Search mock answer for: {q}"}).dict()
