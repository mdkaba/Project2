# backend/app/api/v1/schemas.py
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# --- Chat Schemas ---

class ChatMessageInput(BaseModel):
    query: str
    conversation_id: Optional[str] = None # ID to track conversation history
    # Optional metadata from frontend
    metadata: Optional[Dict[str, Any]] = None

class ChatMessageOutput(BaseModel):
    response: str
    conversation_id: str # Return conversation ID (new or existing)
    agent_name: Optional[str] = None # Which agent handled the request
    # Optional context documents used
    context_docs: Optional[List[Dict[str, Any]]] = None
    # Optional debugging/trace info
    debug_info: Optional[Dict[str, Any]] = None

# --- Potentially add other schemas later (e.g., DocumentUpload, User) --- 