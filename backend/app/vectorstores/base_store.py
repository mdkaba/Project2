from abc import ABC, abstractmethod
from typing import List, Tuple, Any, Dict

class BaseVectorStore(ABC):
    """Abstract base class for vector store implementations."""

    @abstractmethod
    def add_documents(self, documents: List[Tuple[str, Dict[str, Any]]]):
        """
        Adds documents (text and metadata) to the vector store.

        Args:
            documents: A list of tuples, where each tuple contains
                       (document_text: str, metadata: dict).
        """
        pass

    @abstractmethod
    def similarity_search(self, query: str, k: int = 4) -> List[Tuple[Any, float]]:
        """
        Performs a similarity search against the vector store.

        Args:
            query: The query string to search for.
            k: The number of similar documents to return.

        Returns:
            A list of tuples, where each tuple contains
            (document_content_or_metadata, score). The exact content depends
            on the implementation (e.g., could be the Document object or just metadata).
        """
        pass

    @abstractmethod
    def save_local(self, path: str):
        """Saves the vector store index to a local path."""
        pass

    @abstractmethod
    def load_local(self, path: str):
        """Loads the vector store index from a local path."""
        pass 