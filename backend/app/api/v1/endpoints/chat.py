# backend/app/api/v1/endpoints/chat.py
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict # Add Dict for ConnectionManager if uncommenting WS

from app.api.v1 import schemas # Import schemas from the same v1 level
# Import services
from app.services.chat_service import ChatService
from app.services.ollama_service import OllamaService # Needed for dependency
from app.core.database import get_db # Import DB session dependency
from app.core.logger import logger

router = APIRouter()

# --- Dependency Injection Setup ---

# Create a single OllamaService instance (or manage lifecycle as needed)
# This could also be managed within a more complex dependency system
# Be mindful of resource usage if OllamaService holds large models/connections
ollama_service_instance = OllamaService()

# Dependency function to get ChatService instance
async def get_chat_service(
    db: AsyncSession = Depends(get_db)
) -> ChatService:
    """Dependency to provide a ChatService instance with DB session and Ollama service."""
    # Consider if ollama_service needs request-specific state; if not, reusing is fine.
    return ChatService(db_session=db, ollama_service=ollama_service_instance)

# --- REST Endpoint --- 

@router.post("/", response_model=schemas.ChatMessageOutput)
async def handle_chat_message(
    chat_input: schemas.ChatMessageInput,
    chat_service: ChatService = Depends(get_chat_service) # Inject ChatService
):
    """
    Handles incoming chat messages via REST POST request.
    Orchestrates agent selection, RAG, LLM call, and history management via ChatService.
    """
    logger.info(f"Received chat message for conversation: {chat_input.conversation_id}")
    logger.debug(f"Query: {chat_input.query}")

    try:
        # Call the ChatService to process the message
        result_data = await chat_service.process_user_message(
            query=chat_input.query,
            conversation_id_str=chat_input.conversation_id
        )

        # Convert the result dict to the Pydantic output model
        # Ensure keys match the ChatMessageOutput schema fields
        result = schemas.ChatMessageOutput(
             response=result_data.get("response", "Error: No response generated."),
             conversation_id=result_data["conversation_id"], # Required field
             agent_name=result_data.get("agent_name"),
             # context_docs=result_data.get("context_docs"), # Uncomment if adding later
             # debug_info=result_data.get("debug_info") # Uncomment if adding later
         )

        logger.info(f"Sending response for conversation: {result.conversation_id}")
        return result

    except Exception as e:
        logger.exception(f"Error processing chat message in API endpoint: {e}")
        # Consider more specific error handling based on service exceptions
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# --- WebSocket Endpoint --- (Optional, can be implemented later)

# class ConnectionManager:
#     def __init__(self):
#         self.active_connections: Dict[str, WebSocket] = {}

#     async def connect(self, websocket: WebSocket, client_id: str):
#         await websocket.accept()
#         self.active_connections[client_id] = websocket
#         logger.info(f"WebSocket connected: {client_id}")

#     def disconnect(self, client_id: str):
#         if client_id in self.active_connections:
#             del self.active_connections[client_id]
#             logger.info(f"WebSocket disconnected: {client_id}")

#     async def send_personal_message(self, message: str, client_id: str):
#         if client_id in self.active_connections:
#             await self.active_connections[client_id].send_text(message)

# manager = ConnectionManager()

# @router.websocket("/ws/{client_id}")
# async def websocket_endpoint(
#     websocket: WebSocket, 
#     client_id: str, 
#     db: AsyncSession = Depends(get_db)
#     # TODO: Inject ChatService
# ):
#     await manager.connect(websocket, client_id)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             logger.info(f"Received WebSocket message from {client_id}: {data}")
#             # Assume data is JSON string like {"query": "...", "conversation_id": "..."}
#             # Parse input, call chat service, stream response back
#             try:
#                 # input_data = ChatMessageInput.parse_raw(data)
#                 # async for response_chunk in chat_service.process_user_message_stream(...):
#                 #     await manager.send_personal_message(response_chunk, client_id)
                
#                 # Placeholder streaming
#                 await manager.send_personal_message(f"Processing: {data}", client_id)
#                 await asyncio.sleep(1)
#                 await manager.send_personal_message(f"Response to: {data} (Placeholder)", client_id)

#             except Exception as e:
#                 logger.error(f"Error processing WebSocket message from {client_id}: {e}")
#                 await manager.send_personal_message(f"Error: {str(e)}", client_id)

#     except WebSocketDisconnect:
#         manager.disconnect(client_id)
#     except Exception as e:
#         logger.error(f"WebSocket error for client {client_id}: {e}")
#         manager.disconnect(client_id)
#         # Optionally attempt to close websocket if not already closed
#         try:
#             await websocket.close(code=1011) # Internal Error
#         except RuntimeError:
#             pass # Already closed

# Placeholder imports for placeholder code above
# import asyncio
# import uuid

# TODO: Import services later
# from app.services.chat_service import ChatService 
# TODO: Inject ChatService dependency later
# chat_service: ChatService = Depends(get_chat_service) 