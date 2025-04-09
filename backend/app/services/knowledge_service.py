# backend/app/services/knowledge_service.py
from typing import List, Dict, Any, Optional
import asyncio # Import asyncio

from app.knowledge.wikipedia_client import WikipediaClient
from app.knowledge.arxiv_client import ArxivClient
from app.knowledge.github_client import GitHubClient
from app.knowledge.web_search_client import WebSearchClient
from app.knowledge.concordia.web_scraper import ConcordiaWebScraper
from app.core.logger import logger

# Initialize clients (consider making these injectable dependencies later)
wikipedia_client = WikipediaClient()
arxiv_client = ArxivClient()
github_client = GitHubClient()
web_search_client = WebSearchClient()
concordia_scraper = ConcordiaWebScraper()

class KnowledgeService:
    """
    Service layer for accessing external knowledge sources.
    Uses various clients (Wikipedia, ArXiv, GitHub, Web Search, Scrapers).
    Ensures synchronous client calls are run in a separate thread.
    """
    def __init__(self):
        # Clients are initialized outside for simplicity now
        # In a larger app, consider dependency injection
        logger.info("KnowledgeService initialized.")

    async def get_wikipedia_summary(self, topic: str, sentences: int = 3) -> Optional[str]:
        """Fetches Wikipedia summary asynchronously using thread pool."""
        logger.debug(f"Running wikipedia_client.get_summary for '{topic}' in thread pool.")
        try:
            # Run the synchronous function in a separate thread
            summary = await asyncio.to_thread(
                wikipedia_client.get_summary, topic, sentences
            )
            return summary
        except Exception as e:
            logger.exception(f"Error running wikipedia_client.get_summary in thread: {e}")
            return None

    async def search_arxiv(self, query: str, max_results: int = 3) -> List[Dict[str, Any]]:
        """Searches ArXiv. Assuming arxiv library handles its own async/blocking appropriately for now."""
        # TODO: Deep-dive into `arxiv` library's async behavior if issues arise.
        return arxiv_client.search_papers(query, max_results)

    async def search_github_repos(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Searches GitHub repositories asynchronously using thread pool."""
        logger.debug(f"Running github_client.search_repositories for '{query}' in thread pool.")
        try:
            repos = await asyncio.to_thread(
                github_client.search_repositories, query, max_results
            )
            return repos
        except Exception as e:
            logger.exception(f"Error running github_client.search_repositories in thread: {e}")
            return []

    async def search_github_code(self, query: str, max_results: int = 5, language: Optional[str] = None) -> List[Dict[str, Any]]:
        """Searches GitHub code asynchronously using thread pool."""
        logger.debug(f"Running github_client.search_code for '{query}' in thread pool.")
        try:
            code_files = await asyncio.to_thread(
                github_client.search_code, query, max_results, language
            )
            return code_files
        except Exception as e:
            logger.exception(f"Error running github_client.search_code in thread: {e}")
            return []

    async def search_web(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """Performs web search using the async WebSearchClient."""
        return await web_search_client.search(query, max_results)

    async def get_concordia_scraped_data(self) -> List[Dict[str, Any]]:
        """Fetches Concordia data using the scraper. Assumes scraper.scrape_pages is sync and runs it in thread pool."""
        # Even though the update script runs this synchronously, if the service
        # might be called from elsewhere, make it non-blocking.
        logger.debug(f"Running concordia_scraper.scrape_pages in thread pool.")
        try:
            scraped_data = await asyncio.to_thread(concordia_scraper.scrape_pages)
            return scraped_data
        except Exception as e:
            logger.exception(f"Error running concordia_scraper.scrape_pages in thread: {e}")
            return []

# Optional: Singleton instance
# knowledge_service = KnowledgeService() 