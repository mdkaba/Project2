from fastapi import APIRouter
from pydantic import BaseModel
from app.chat.agent_manager import route_query

router = APIRouter()

class ChatInput(BaseModel):
    message: str

@router.post("/chat")
def chat_route(data: ChatInput):
    response = route_query(data.message)
    return {"response": response}