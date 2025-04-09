from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base
import datetime

class Conversation(Base):
    """Represents a single conversation session."""
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    # Optional: Add user ID if implementing user accounts later
    # user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # Optional: Add a title or summary for the conversation
    title = Column(String(255), nullable=True)

class Message(Base):
    """Represents a single message within a conversation."""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id'), nullable=False, index=True)
    sender_type = Column(String(50), nullable=False) # e.g., 'user', 'ai', 'system'
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # Optional: Add metadata like agent used, context documents, etc.
    # metadata = Column(JSON, nullable=True) 