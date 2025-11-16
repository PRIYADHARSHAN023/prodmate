from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import uuid4

class UserRequest(BaseModel):
    user_id: str
    request_id: Optional[str] = None
    text: str
    session_id: Optional[str] = None

    def __init__(self, **data):
        if 'request_id' not in data or data.get('request_id') is None:
            data['request_id'] = str(uuid4())
        super().__init__(**data)

class AgentResponse(BaseModel):
    request_id: str
    agent: str
    status: str  # ok | pending | error
    result: Optional[Dict[str, Any]] = None
    operation_id: Optional[str] = None
