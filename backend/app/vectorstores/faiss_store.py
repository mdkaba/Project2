# backend/app/vectorstores/faiss_store.py
import os
from typing import List, Tuple, Any, Dict, Optional
import faiss # Import faiss directly if needed for specific index types
from sentence_transformers import SentenceTransformer # Use directly for embedding
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings # Import base class for type hint

from app.vectorstores.base_store import BaseVectorStore
from app.core.logger import logger
from app.core.config import settings

# Helper class to wrap SentenceTransformer for LangChain compatibility if needed,
# although FAISS.from_texts/FAISS.load_local directly accept sentence_transformers models.
# If performance is critical, directly using SentenceTransformer for embedding outside
# the LangChain FAISS wrapper might offer more control.
class SentenceTransformerEmbeddings(Embeddings):
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        # Consider loading model from config or making it configurable
        self.model = SentenceTransformer(model_name)
        logger.info(f"Initialized SentenceTransformer model: {model_name}")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embeds a list of documents."""
        logger.debug(f"Embedding {len(texts)} documents...")
        embeddings = self.model.encode(texts, convert_to_numpy=True).tolist()
        logger.debug("Finished embedding documents.")
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        """Embeds a single query."""
        logger.debug("Embedding query...")
        embedding = self.model.encode(text, convert_to_numpy=True).tolist()
        logger.debug("Finished embedding query.")
        return embedding

class FAISSVectorStore(BaseVectorStore):
    """FAISS implementation of the vector store."""

    def __init__(self, embedding_model_name: str = "all-MiniLM-L6-v2"):
        self.embedding_function = SentenceTransformerEmbeddings(model_name=embedding_model_name)
        self.index: Optional[FAISS] = None
        self.index_path = settings.VECTOR_STORE_PATH
        self.load_local(str(self.index_path)) # Attempt to load existing index on init

    def add_documents(self, documents: List[Tuple[str, Dict[str, Any]]]):
        """Adds text documents with metadata to the FAISS index."""
        if not documents:
            logger.warning("No documents provided to add.")
            return

        logger.info(f"Adding {len(documents)} documents to FAISS index...")
        # Convert tuples to LangChain Document objects
        lc_documents = [Document(page_content=text, metadata=meta) for text, meta in documents]

        if self.index is None:
            logger.info("Creating new FAISS index.")
            # Use class method from_documents to create index if it doesn't exist
            try:
                 self.index = FAISS.from_documents(
                     documents=lc_documents,
                     embedding=self.embedding_function
                 )
                 logger.info("Successfully created new FAISS index.")
            except Exception as e:
                 logger.exception(f"Error creating FAISS index: {e}")
                 raise
        else:
            logger.info("Adding documents to existing FAISS index.")
            try:
                # Extract texts and metadata for add_documents method
                texts = [doc.page_content for doc in lc_documents]
                metadatas = [doc.metadata for doc in lc_documents]
                # TODO: Check if FAISS add_documents supports async or requires sync execution
                # For simplicity, using sync add_texts here. Consider running in thread pool if blocking.
                self.index.add_texts(texts=texts, metadatas=metadatas)
                logger.info("Successfully added documents to FAISS index.")
            except Exception as e:
                logger.exception(f"Error adding documents to FAISS index: {e}")
                raise

        # Persist index after adding documents
        self.save_local(str(self.index_path))

    def similarity_search(self, query: str, k: int = 4) -> List[Tuple[Document, float]]:
        """Performs similarity search with scores."""
        if self.index is None:
            logger.error("FAISS index is not loaded or initialized.")
            return []

        logger.debug(f"Performing similarity search for query: '{query}' with k={k}")
        try:
            # Use similarity_search_with_score for better results handling
            results_with_scores = self.index.similarity_search_with_score(query, k=k)
            logger.debug(f"Found {len(results_with_scores)} similar documents.")
            # results_with_scores is List[Tuple[Document, float]]
            return results_with_scores
        except Exception as e:
            logger.exception(f"Error during similarity search: {e}")
            return []

    def save_local(self, path: str):
        """Saves the FAISS index and embeddings to a local folder."""
        if self.index:
            # Ensure path uses OS-specific separators if needed, though LangChain usually handles it
            # index_file = os.path.join(path, "index.faiss")
            logger.info(f"Saving FAISS index to path: {path}")
            try:
                # LangChain's save_local saves index and embeddings (docstore.pkl)
                self.index.save_local(folder_path=path)
                logger.info("FAISS index saved successfully.")
            except Exception as e:
                logger.exception(f"Error saving FAISS index to {path}: {e}")
        else:
            logger.warning("Attempted to save an empty or non-existent FAISS index.")

    def load_local(self, path: str):
        """Loads the FAISS index and embeddings from a local folder."""
        # index_file = os.path.join(path, "index.faiss")
        # Check if the path and essential files exist
        if os.path.isdir(path) and os.path.exists(os.path.join(path, "index.faiss")) and os.path.exists(os.path.join(path, "index.pkl")):
            logger.info(f"Loading FAISS index from path: {path}")
            try:
                # FAISS.load_local requires the embedding function
                self.index = FAISS.load_local(
                    folder_path=path,
                    embeddings=self.embedding_function,
                    # Allow dangerous deserialization if using older pickle formats (use with caution)
                    allow_dangerous_deserialization=True
                )
                logger.info("FAISS index loaded successfully.")
            except Exception as e:
                logger.exception(f"Error loading FAISS index from {path}: {e}")
                self.index = None # Ensure index is None if loading fails
        else:
            logger.warning(f"FAISS index path not found or incomplete: {path}. Index not loaded.")
            self.index = None 