from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAgent(ABC):
    """Abstract base class for all agents."""

    @abstractmethod
    def get_name(self) -> str:
        """Returns the unique name of the agent."""
        pass

    @abstractmethod
    async def process(self, query: str, history: list[Dict[str, str]], context_docs: list[Any] = None) -> str:
        """Processes the user query and returns the agent's response.

        Args:
            query: The user's current query.
            history: A list of past conversation turns (e.g., [{'role': 'user', 'content': '...'}, {'role': 'assistant', 'content': '...'}]).
            context_docs: Optional list of relevant documents retrieved via RAG.

        Returns:
            The agent's response as a string.
        """
        pass

    @abstractmethod
    async def should_handle(self, query: str, history: list[Dict[str, str]]) -> float:
        """Determines the confidence score (0.0 to 1.0) of this agent handling the query.

        Args:
            query: The user's current query.
            history: The conversation history.

        Returns:
            A float score between 0.0 (definitely not) and 1.0 (definitely should).
        """
        pass 