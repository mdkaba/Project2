# backend/app/repositories/chat_history_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload # Keep for potential future use with relationships
from typing import List, Optional, Dict
import uuid

from app.models.chat_history import Conversation, Message
from app.core.logger import logger

class ChatHistoryRepository:
    """
    Repository class for handling database operations related to
    conversations and messages.
    """
    def __init__(self, db_session: AsyncSession):
        """
        Initializes the repository with an async database session.

        Args:
            db_session: The SQLAlchemy AsyncSession to use for database operations.
        """
        self.db: AsyncSession = db_session

    async def create_conversation(self, title: Optional[str] = None) -> Conversation:
        """
        Creates a new conversation entry in the database.

        Args:
            title: An optional title for the conversation.

        Returns:
            The newly created Conversation object.
        """
        try:
            new_conversation = Conversation(title=title)
            self.db.add(new_conversation)
            await self.db.flush() # Flush to get the ID before commit
            await self.db.refresh(new_conversation)
            logger.info(f"Created new conversation with ID: {new_conversation.id}")
            return new_conversation
        except Exception as e:
            logger.exception(f"Error creating conversation: {e}")
            # Depending on desired behavior, you might re-raise or return None
            raise

    async def add_message(self, conversation_id: int, sender_type: str, content: str) -> Message:
        """
        Adds a message to an existing conversation.

        Args:
            conversation_id: The ID of the conversation to add the message to.
            sender_type: The type of sender ('user' or 'ai').
            content: The text content of the message.

        Returns:
            The newly created Message object.
        """
        try:
            new_message = Message(
                conversation_id=conversation_id,
                sender_type=sender_type,
                content=content
            )
            self.db.add(new_message)
            await self.db.flush() # Flush to get the ID before commit
            await self.db.refresh(new_message)
            logger.debug(f"Added message to conversation {conversation_id}")
            return new_message
        except Exception as e:
            logger.exception(f"Error adding message to conversation {conversation_id}: {e}")
            raise

    async def get_conversation_history(self, conversation_id: int, limit: int = 10) -> List[Dict[str, str]]:
        """
        Retrieves the most recent messages for a given conversation,
        formatted for LangChain memory input.

        Args:
            conversation_id: The ID of the conversation.
            limit: The maximum number of messages to retrieve.

        Returns:
            A list of dictionaries, each representing a message
            with 'role' and 'content' keys, in chronological order.
        """
        try:
            stmt = (
                select(Message)
                .where(Message.conversation_id == conversation_id)
                .order_by(Message.timestamp.desc())
                .limit(limit)
            )
            result = await self.db.execute(stmt)
            messages = result.scalars().all()

            # Format history for LangChain (needs role/content)
            # Reverse messages to get chronological order for prompt
            history = [
                # Use 'assistant' role for AI messages to match common conventions
                {"role": msg.sender_type if msg.sender_type == 'user' else 'assistant', "content": msg.content}
                for msg in reversed(messages)
            ]
            logger.debug(f"Retrieved {len(history)} messages for conversation {conversation_id}")
            return history
        except Exception as e:
            logger.exception(f"Error retrieving history for conversation {conversation_id}: {e}")
            return [] # Return empty list on error

    async def get_or_create_conversation(self, conversation_id_str: Optional[str]) -> Conversation:
        """
        Gets an existing conversation by its string ID or creates a
        new one if the ID is None, invalid, or not found.

        Args:
            conversation_id_str: The conversation ID as a string (or None).

        Returns:
            The existing or newly created Conversation object.
        """
        conversation: Optional[Conversation] = None

        if conversation_id_str:
            try:
                # Attempt to convert the string ID to an integer
                conv_int_id = int(conversation_id_str)
                conversation = await self.get_conversation(conv_int_id)

                if conversation:
                    logger.debug(f"Found existing conversation: {conversation_id_str}")
                    return conversation
                else:
                    # ID was valid integer but not found in DB
                    logger.warning(f"Conversation ID {conversation_id_str} not found, creating new.")
            except ValueError:
                 # ID was not a valid integer format
                 logger.warning(f"Invalid conversation ID format: '{conversation_id_str}'. Creating new.")
            except Exception as e:
                # Catch other potential DB errors during fetch
                logger.exception(f"Error fetching conversation {conversation_id_str}: {e}. Creating new.")

        # If conversation_id_str was None, invalid, not found, or error occurred:
        logger.info("Creating a new conversation.")
        return await self.create_conversation() # Ensure creation error is handled/logged inside

    async def get_conversation(self, conversation_id: int) -> Optional[Conversation]:
         """
         Gets a conversation by its integer ID.

         Args:
             conversation_id: The integer ID of the conversation.

         Returns:
             The Conversation object if found, otherwise None.
         """
         try:
             stmt = select(Conversation).where(Conversation.id == conversation_id)
             result = await self.db.execute(stmt)
             return result.scalar_one_or_none()
         except Exception as e:
             logger.exception(f"Error getting conversation {conversation_id}: {e}")
             return None 