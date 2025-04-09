# backend/app/knowledge/arxiv_client.py
import arxiv
from typing import List, Dict, Any, Optional
from app.core.logger import logger

class ArxivClient:
    """Client for interacting with the ArXiv API."""
    def __init__(self):
        # The arxiv library doesn't require explicit initialization beyond import
        self.client = arxiv.Client(
             page_size=5, # Fetch 5 results per page
             delay_seconds=3.0, # Be polite to the API
             num_retries=3
        )
        logger.info("ArxivClient initialized.")

    def search_papers(self, query: str, max_results: int = 3) -> List[Dict[str, Any]]:
        """
        Searches for papers on ArXiv.

        Args:
            query: The search query (e.g., title, author, abstract keywords).
            max_results: The maximum number of papers to return.

        Returns:
            A list of dictionaries, each containing details of a paper.
            Returns empty list on error.
        """
        logger.debug(f"Searching ArXiv for query: '{query}' (max_results={max_results})")
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance # Or SubmittedDate
        )

        results_list = []
        try:
            results_generator = self.client.results(search)
            for result in results_generator:
                paper_details = {
                    "entry_id": result.entry_id,
                    "title": result.title,
                    "authors": [str(author) for author in result.authors],
                    "summary": result.summary,
                    "published": result.published.strftime('%Y-%m-%d'), # Format date
                    "pdf_url": result.pdf_url,
                    "primary_category": result.primary_category,
                    "categories": result.categories
                }
                results_list.append(paper_details)
                logger.debug(f"Found ArXiv paper: {result.title}")

            logger.info(f"ArXiv search for '{query}' yielded {len(results_list)} results.")
            return results_list
        except Exception as e:
            logger.exception(f"Error searching ArXiv for query '{query}': {e}")
            return [] # Return empty list on error

# Example usage:
# arxiv_client = ArxivClient()
# papers = arxiv_client.search_papers("large language models", max_results=2)
# for paper in papers:
#     print(f"Title: {paper['title']}")
#     print(f"Authors: {', '.join(paper['authors'])}")
#     print(f"URL: {paper['pdf_url']}")
#     print(f"Summary: {paper['summary'][:200]}...")
#     print("-" * 10) 