# backend/management/update_knowledge_base.py
import sys
import os
import asyncio
import logging

# Ensure the backend directory is in the Python path
# Go up one level from management dir to get 'backend' dir
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, backend_dir)

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document

from app.core.embeddings import SentenceTransformerEmbeddings
from app.knowledge.concordia.web_scraper import ConcordiaWebScraper
from app.core.config import settings
from app.core.logger import logger

load_dotenv()

def update_knowledge_base():
    logger.info("Starting knowledge base update process...")

    # --- 1. Scrape Data ---
    logger.info("Initializing Concordia Web Scraper...")
    scraper = ConcordiaWebScraper()
    # Run scrape_pages synchronously as this is a standalone script
    # If KnowledgeService was used here, it would handle the threading
    try:
        scraped_docs_raw = scraper.scrape_pages()
    except Exception as e:
        logger.exception(f"Error during Concordia scraping: {e}")
        scraped_docs_raw = []

    if not scraped_docs_raw:
        logger.warning("No documents were scraped. Aborting update.")
        return

    logger.info(f"Successfully scraped {len(scraped_docs_raw)} pages.")

    # Convert raw scraped data into LangChain Document objects
    documents = [
        Document(page_content=doc['content'], metadata={'source': doc['source']})
        for doc in scraped_docs_raw if doc.get('content') # Ensure content exists
    ]

    if not documents:
        logger.warning("Scraped data contained no processable content. Aborting update.")
        return

    logger.info(f"Converted {len(documents)} scraped items into LangChain Documents.")

    # --- 2. Split Documents ---
    logger.info("Initializing text splitter...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    split_docs = text_splitter.split_documents(documents)
    logger.info(f"Split documents into {len(split_docs)} chunks.")

    # --- 3. Initialize Embeddings ---
    logger.info("Initializing embeddings model...")
    try:
        embeddings = SentenceTransformerEmbeddings()
    except Exception as e:
        logger.exception(f"Failed to initialize embeddings model: {e}")
        return

    # --- 4. Load or Create Vector Store ---
    vector_store_path = settings.VECTOR_STORE_PATH
    vector_store_index_file = os.path.join(vector_store_path, "index.faiss")
    vector_store_pkl_file = os.path.join(vector_store_path, "index.pkl")

    vector_store = None
    if os.path.exists(vector_store_index_file) and os.path.exists(vector_store_pkl_file):
        logger.info(f"Loading existing vector store from: {vector_store_path}")
        try:
            vector_store = FAISS.load_local(
                folder_path=vector_store_path,
                embeddings=embeddings,
                allow_dangerous_deserialization=True
            )
            logger.info("Existing vector store loaded successfully.")
            logger.info(f"Adding {len(split_docs)} new document chunks to the vector store...")
            vector_store.add_documents(split_docs)

        except Exception as e:
            logger.exception(f"Error loading/adding to existing vector store: {e}. Will create a new one.")
            vector_store = None

    # --- 5. Create Vector Store if not loaded ---
    if vector_store is None:
        logger.info("Creating new vector store...")
        if not split_docs:
             logger.error("No document chunks to add to the new vector store. Aborting.")
             return
        try:
            vector_store = FAISS.from_documents(split_docs, embeddings)
            logger.info("New vector store created successfully.")
        except Exception as e:
            logger.exception(f"Failed to create new vector store from documents: {e}")
            return

    # --- 6. Save Vector Store ---
    logger.info(f"Saving vector store to: {vector_store_path}")
    os.makedirs(vector_store_path, exist_ok=True)
    try:
        vector_store.save_local(folder_path=vector_store_path)
        logger.info("Vector store saved successfully.")
    except Exception as e:
        logger.exception(f"Failed to save vector store: {e}")

    logger.info("Knowledge base update process finished.")

if __name__ == "__main__":
    # Setup basic logging if running as script
    log_level_str = os.getenv('LOG_LEVEL', 'INFO').upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    logging.basicConfig(level=log_level, format='%(asctime)s | %(levelname)-8s | %(name)-25s:%(lineno)-4d | %(message)s')

    update_knowledge_base() 