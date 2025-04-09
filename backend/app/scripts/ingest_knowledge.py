# backend/app/scripts/ingest_knowledge.py
import asyncio
import sys
import os
from typing import List, Dict, Any, Tuple

# Add backend directory to Python path to allow imports from app
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.knowledge.concordia.web_scraper import ConcordiaWebScraper
from app.services.vector_store_service import VectorStoreService
from app.core.logger import logger

# Optional: Text Splitting (Recommended for large documents)
from langchain.text_splitter import RecursiveCharacterTextSplitter

async def run_ingestion():
    """
    Scrapes Concordia data and adds it to the vector store.
    """
    logger.info("Starting knowledge ingestion process...")

    # --- 1. Scrape Data ---
    scraper = ConcordiaWebScraper()
    # scraped_pages: List[Dict[str, Any]] where dict has 'source' and 'content'
    scraped_pages = await scraper.scrape_pages()

    if not scraped_pages:
        logger.error("No data scraped from Concordia website. Ingestion aborted.")
        return

    logger.info(f"Successfully scraped {len(scraped_pages)} pages.")

    # --- 2. Process and Chunk Data ---
    documents_to_add: List[Tuple[str, Dict[str, Any]]] = []
    # Initialize text splitter (tune parameters as needed)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, # Max characters per chunk
        chunk_overlap=150, # Overlap between chunks
        length_function=len,
        add_start_index=True, # Add start index metadata
    )

    for page in scraped_pages:
        source_url = page.get('source', 'Unknown Source')
        content = page.get('content', '')

        if not content:
            logger.warning(f"Skipping empty content from source: {source_url}")
            continue

        logger.debug(f"Splitting content from: {source_url}")
        # Split the scraped content into chunks
        chunks = text_splitter.split_text(content)
        logger.debug(f"Created {len(chunks)} chunks.")

        for i, chunk in enumerate(chunks):
            metadata = {
                "source": source_url,
                "chunk_index": i,
                # Add other metadata if available/relevant
            }
            # Append tuple (chunk_text, metadata)
            documents_to_add.append((chunk, metadata))

    if not documents_to_add:
        logger.error("No processable document chunks found after splitting. Ingestion aborted.")
        return

    logger.info(f"Processed scraped data into {len(documents_to_add)} document chunks.")

    # --- 3. Initialize Vector Store Service ---
    # This will load existing index if available
    vector_store_service = VectorStoreService()

    # --- 4. Add Documents to Vector Store ---
    logger.info("Adding processed documents to the vector store...")
    # This method handles creating or adding to the index and saving
    vector_store_service.add_documents(documents_to_add)

    logger.info("Knowledge ingestion process finished successfully.")


if __name__ == "__main__":
    # Setup to run the async function
    try:
        asyncio.run(run_ingestion())
    except Exception as e:
         logger.exception(f"Knowledge ingestion script failed: {e}")
         sys.exit(1) 