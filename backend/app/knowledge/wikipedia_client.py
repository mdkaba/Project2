# backend/app/knowledge/wikipedia_client.py
import wikipediaapi
from typing import Optional, List
from app.core.logger import logger

class WikipediaClient:
    """Client for interacting with the Wikipedia API."""
    def __init__(self, user_agent="COMP474Chatbot/1.0 (Concordia University)"):
        # Setting a proper user agent is good practice
        self.wiki_wiki = wikipediaapi.Wikipedia(
            language='en',
            user_agent=user_agent
        )
        logger.info("WikipediaClient initialized.")

    def get_summary(self, topic: str, sentences: int = 3) -> Optional[str]:
        """
        Fetches a summary of a Wikipedia page.

        Args:
            topic: The topic or page title to search for.
            sentences: The desired number of sentences for the summary.

        Returns:
            The summary string, or None if the page doesn't exist or summary fails.
        """
        logger.debug(f"Fetching Wikipedia summary for: {topic}")
        page = self.wiki_wiki.page(topic)

        if not page.exists():
            logger.warning(f"Wikipedia page '{topic}' does not exist.")
            return None
        try:
            # wikipediaapi library handles fetching summary; sentences param might not be exact
            # We can truncate later if needed
            summary = page.summary # Fetch full summary first
            # Simple sentence splitting and joining - adjust as needed
            split_summary = summary.split('. ')
            truncated_summary = '. '.join(split_summary[:sentences]) + ('.' if len(split_summary) > sentences else '')

            logger.debug(f"Successfully fetched summary for '{topic}'.")
            return truncated_summary
        except Exception as e:
            logger.exception(f"Error fetching Wikipedia summary for '{topic}': {e}")
            return None

    def search_pages(self, query: str, limit: int = 5) -> List[str]:
        """
        Searches for Wikipedia page titles matching the query.

        Args:
            query: The search query.
            limit: The maximum number of page titles to return.

        Returns:
            A list of matching page titles.
        """
        logger.debug(f"Searching Wikipedia for pages matching: {query}")
        try:
            # Use page method which implicitly searches if exact match fails
            page = self.wiki_wiki.page(query)
            if page.exists():
                 # If exact match, return just that for now? Or search anyway?
                 # Let's return search results for consistency.
                 pass # Fall through to search

            # wikipediaapi doesn't have a direct search method, workaround using generator
            # This approach is less direct than using the `wikipedia` library's search
            # Consider switching library if direct search is crucial
            logger.warning("WikipediaClient search is basic; consider 'wikipedia' library for better search.")
            # Placeholder: Return the query itself if page exists, else empty
            return [page.title] if page.exists() else []

        except Exception as e:
            logger.exception(f"Error searching Wikipedia for '{query}': {e}")
            return []

# Example usage:
# wiki_client = WikipediaClient()
# summary = wiki_client.get_summary("Artificial intelligence")
# print(summary)
# results = wiki_client.search_pages("Machine Learning")
# print(results) 