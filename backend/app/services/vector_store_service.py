from typing import List, Optional, Dict, Any, Tuple
from langchain_core.documents import Document

from app.vectorstores.faiss_store import FAISSVectorStore
from app.vectorstores.base_store import BaseVectorStore # For type hint
from app.core.logger import logger
from app.core.config import settings

class VectorStoreService:
    """
    Service layer for managing interactions with the vector store.
    Handles initialization and provides methods for adding and searching documents.
    """
    def __init__(self):
        # Initialize the specific vector store implementation
        # Could be made configurable later if needed
        self.vector_store: BaseVectorStore = FAISSVectorStore(
            # Optionally configure embedding model from settings if needed
            # embedding_model_name=settings.EMBEDDING_MODEL_NAME
        )
        logger.info("VectorStoreService initialized.")

    def add_documents(self, documents: List[Tuple[str, Dict[str, Any]]]):
        """
        Adds documents to the configured vector store.

        Args:
            documents: List of tuples containing (text, metadata).
        """
        logger.info(f"VectorStoreService adding {len(documents)} documents.")
        try:
            self.vector_store.add_documents(documents)
        except Exception as e:
            logger.exception("VectorStoreService failed to add documents.")
            # Decide if error should be propagated or handled
            # raise e

    def search_similar_documents(self, query: str, k: int = 4) -> List[Document]:
        """
        Searches for documents similar to the query in the vector store.

        Args:
            query: The search query string.
            k: The number of documents to return.

        Returns:
            A list of LangChain Document objects found.
        """
        logger.info(f"VectorStoreService searching for documents similar to: '{query}'")
        try:
            # Similarity search returns List[Tuple[Document, float]]
            results_with_scores = self.vector_store.similarity_search(query, k=k)
            # Extract just the Document objects
            documents = [doc for doc, score in results_with_scores]
            logger.info(f"VectorStoreService found {len(documents)} similar documents.")
            return documents
        except Exception as e:
            logger.exception("VectorStoreService failed during similarity search.")
            return []

    def get_retriever(self, k: int = 4):
        """
        Returns a LangChain retriever instance for the vector store.
        Useful for integrating directly into LCEL chains.

        Args:
            k: The number of documents the retriever should fetch.

        Returns:
            A LangChain retriever object.
        """
        if self.vector_store and hasattr(self.vector_store.index, 'as_retriever'):
            logger.debug(f"Creating retriever with k={k}")
            return self.vector_store.index.as_retriever(search_kwargs={"k": k})
        else:
            logger.error("Cannot create retriever: Vector store index not initialized.")
            # Return a dummy retriever or raise an error
            class DummyRetriever:
                def get_relevant_documents(self, *args, **kwargs): return []
                async def aget_relevant_documents(self, *args, **kwargs): return []
            return DummyRetriever()

# Optional: Singleton instance for easier access or use dependency injection
# vector_store_service = VectorStoreService() 