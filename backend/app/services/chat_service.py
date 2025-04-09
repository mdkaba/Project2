# backend/app/services/chat_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Dict, Any, List

from app.repositories.chat_history_repository import ChatHistoryRepository
from app.services.ollama_service import OllamaService
from app.core.logger import logger
from app.core.config import settings
# We'll use LangChain components here
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from app.services.vector_store_service import VectorStoreService
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from app.services.agent_service import AgentService
from app.agents.base import BaseAgent

class ChatService:
    """
    Service responsible for handling the core chat logic, including
    history management, agent routing (future), RAG (future), and LLM interaction.
    """
    def __init__(self, db_session: AsyncSession, ollama_service: OllamaService):
        """
        Initializes the ChatService.

        Args:
            db_session: The SQLAlchemy AsyncSession.
            ollama_service: An instance of the OllamaService.
            # TODO: Inject other services/components like AgentService, VectorStoreService later
        """
        self.db_session = db_session
        self.ollama_service = ollama_service
        self.history_repo = ChatHistoryRepository(db_session)
        # Initialize VectorStoreService (could also be injected)
        self.vector_store_service = VectorStoreService()
        # Initialize AgentService
        self.agent_service = AgentService()
        # TODO: Initialize KnowledgeService (or make clients accessible)

    def _format_docs(self, docs: List[Document]) -> str:
        """Helper function to format retrieved documents into a string for the prompt."""
        return "\n\n".join(f"Source {i+1}:\n{doc.page_content}" for i, doc in enumerate(docs))

    async def process_user_message(self, query: str, conversation_id_str: Optional[str]) -> Dict[str, Any]:
        """
        Processes a user's message, manages history, interacts with LLM,
        and returns the response.

        Args:
            query: The user's input message.
            conversation_id_str: The string ID of the ongoing conversation (or None for new).

        Returns:
            A dictionary containing the AI's response and the conversation ID.
            Example: {'response': '...', 'conversation_id': '...', 'agent_name': '...'}
        """
        logger.info(f"Processing query for conversation '{conversation_id_str}': '{query}'")

        # 1. Get or Create Conversation
        conversation = await self.history_repo.get_or_create_conversation(conversation_id_str)
        conv_id = conversation.id # Use the integer ID internally

        # 2. Add User Message to History
        await self.history_repo.add_message(conv_id, "user", query)

        # 3. Retrieve Recent History (formatted for LangChain)
        history_list: List[Dict[str, str]] = await self.history_repo.get_conversation_history(conv_id)

        # 4. Select Agent using AgentService
        selected_agent: BaseAgent = await self.agent_service.select_agent(query, history_list)
        selected_agent_name = selected_agent.get_name()

        # 5. Perform RAG (Context Retrieval) - Potentially agent-specific later
        context_docs: List[Document] = [] # Ensure initialization with type hint
        # Only Admissions agent uses RAG for now in this setup
        if selected_agent_name == "AdmissionsAgent":
            logger.debug(f"Retrieving context documents via RAG for {selected_agent_name}")
            retriever = self.vector_store_service.get_retriever(k=3)
            # TODO: Verify async support for retriever
            context_docs = retriever.get_relevant_documents(query)
            logger.debug(f"Retrieved {len(context_docs)} documents for RAG.")
        # formatted_context = self._format_docs(context_docs) # Formatting now done within agent process

        # 6. Process Query using Selected Agent
        # The agent's process method now handles prompt creation, tool use (if any), and LLM call
        ai_response = await selected_agent.process(
            query=query,
            history=history_list,
            context_docs=context_docs # Pass RAG context only if relevant for the agent
        )

        # 7. Add AI Response to History
        await self.history_repo.add_message(conv_id, "ai", ai_response)

        # 8. Return Result
        result = {
            "response": ai_response,
            "conversation_id": str(conv_id),
            "agent_name": selected_agent_name,
            # Optionally format/include context_docs if needed for frontend display
            "context_docs": [{"source": doc.metadata.get("source", "Unknown"), "content": doc.page_content[:100] + "..."} for doc in context_docs] if context_docs else None
        }
        logger.info(f"Processed message using {selected_agent_name}, response generated for conversation {conv_id}.")
        return result 