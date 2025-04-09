from duckduckgo_search import DDGS
from typing import List, Dict, Any, Optional
from app.core.logger import logger

# Potential alternative: Tavily Search API (requires API key but often gives better results for agents)
# from tavily import TavilyClient 
# TAVILY_API_KEY = settings.TAVILY_API_KEY 

class WebSearchClient:
    """Client for performing web searches (currently using DuckDuckGo)."""
    def __init__(self):
        # Initialize DDGS - no API key needed usually
        self.ddgs = DDGS() 
        # If using Tavily:
        # if not TAVILY_API_KEY:
        #     logger.warning("TAVILY_API_KEY not found. Web search may be limited.")
        #     self.tavily_client = None
        # else:
        #     self.tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
        logger.info("WebSearchClient initialized (using DuckDuckGo).")

    async def search(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """
        Performs a web search using DuckDuckGo.

        Args:
            query: The search query string.
            max_results: The maximum number of search results to return.

        Returns:
            A list of dictionaries, each containing 'title', 'href', and 'body' (snippet).
            Returns empty list on error.
        """
        logger.debug(f"Performing web search for: '{query}' (max_results={max_results})")
        results_list = []
        try:
            # Use atext for async search. DDGS returns dictionaries directly.
            ddgs_results = await self.ddgs.atext(query, max_results=max_results)
            
            # Ensure results are in the expected format list[dict]
            if isinstance(ddgs_results, list):
                 results_list = ddgs_results[:max_results] # Ensure we don't exceed max_results
                 logger.info(f"Web search for '{query}' yielded {len(results_list)} results.")
            else:
                 logger.warning(f"DuckDuckGo search returned unexpected format: {type(ddgs_results)}")

            return results_list

            # --- If using Tavily ---
            # if not self.tavily_client:
            #     logger.error("Tavily client not initialized (missing API key?).")
            #     return []
            # response = await self.tavily_client.search(query=query, search_depth="basic", max_results=max_results)
            # # Tavily returns a dict with a 'results' key -> list[dict]
            # results_list = response.get('results', [])
            # logger.info(f"Tavily search for '{query}' yielded {len(results_list)} results.")
            # return results_list
            # -----------------------

        except Exception as e:
            logger.exception(f"Error during web search for '{query}': {e}")
            return []

# Example usage (needs an async context to run):
# async def main():
#     web_search_client = WebSearchClient()
#     results = await web_search_client.search("latest AI news", max_results=3)
#     for res in results:
#         print(f"Title: {res.get('title')}")
#         print(f"URL: {res.get('href')}")
#         print(f"Snippet: {res.get('body')}")
#         print("---")
# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main()) 