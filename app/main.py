from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.chat.router import router as chat_router

app = FastAPI(title="Multi-Agent Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api")