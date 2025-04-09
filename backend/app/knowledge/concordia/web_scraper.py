# backend/app/knowledge/concordia/web_scraper.py
import requests
import os
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup # Import BeautifulSoup
from app.core.logger import logger

# Load environment variables from .env file
load_dotenv()

class ConcordiaWebScraper:
    """Scrapes specific Concordia pages using ScrapingBee for fetching and BeautifulSoup for parsing."""

    # Keep the updated list of URLs
    TARGET_URLS = [
        "https://www.concordia.ca/academics/undergraduate/computer-science.html",
        "https://www.concordia.ca/ginacody/computer-science-software-eng/programs/computer-science/bachelor/bcompsc-general.html",
        "https://www.concordia.ca/academics/undergraduate/calendar/current/section-71-gina-cody-school-of-engineering-and-computer-science/section-71-70-department-of-computer-science-and-software-engineering/section-71-70-2-degree-requirements-bcompsc-.html",
        "https://www.concordia.ca/admissions/undergraduate/requirements/cegep-students/r-score.html",
        "https://www.concordia.ca/admissions/undergraduate/programs.html",
        "https://www.concordia.ca/admissions/undergraduate/programs-with-additional-requirements.html",
        "https://www.concordia.ca/ginacody/programs/undergraduate.html",
        "https://www.concordia.ca/ginacody/computer-science-software-eng/programs/computer-science/bachelor.html",
        "https://www.concordia.ca/admissions/undergraduate/requirements/english-language-proficiency.html",
    ]
    TARGET_URLS = list(set(TARGET_URLS))

    def __init__(self, timeout=60):
        self.timeout = timeout
        self.api_key = os.getenv("SCRAPINGBEE_API_KEY")
        if not self.api_key:
            logger.error("SCRAPINGBEE_API_KEY not found in environment variables.")
            raise ValueError("ScrapingBee API key is missing.")
        logger.info(f"ConcordiaWebScraper initialized for {len(self.TARGET_URLS)} target URLs using ScrapingBee GET + BeautifulSoup.")

    def _extract_main_content(self, html_content: str, url: str) -> Optional[str]:
        """
        Extracts the main textual content from the HTML using BeautifulSoup.
        Uses basic selectors - may need refinement based on Concordia's site structure.
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            # Try to find a specific main content area first
            # These selectors are guesses and likely need inspection/adjustment
            main_content_area = soup.find('main') or \
                                soup.find('div', id='content') or \
                                soup.find('div', class_='content-main') or \
                                soup.find('article')

            # Fallback to body if no specific container found
            if not main_content_area:
                main_content_area = soup.body
                logger.debug(f"No specific main content tag found for {url}, using body.")

            if not main_content_area:
                 logger.warning(f"Could not find suitable content area (even body) for {url}")
                 return None

            # Remove common noise elements (use specific selectors for Concordia if known)
            selectors_to_remove = ['header', 'footer', 'nav', '.nav', '.navigation',
                                 '#sidebar', '.sidebar', 'script', 'style', 'aside', '.aside']
            for selector in selectors_to_remove:
                 # Use select for CSS selectors
                 for element in main_content_area.select(selector):
                     element.decompose() # Remove the element and its content

            # Get text from relevant tags, join paragraphs, clean whitespace
            # Consider adding other relevant tags like 'table', 'dl' if needed
            text_parts = [p.get_text(separator=' ', strip=True) for p in main_content_area.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'td', 'th', 'dd', 'dt'])]
            full_text = "\n".join(filter(None, text_parts)) # Join non-empty parts with newline

            # Basic cleaning - normalize whitespace
            full_text = ' '.join(full_text.split())

            return full_text if full_text else None

        except Exception as e:
            logger.exception(f"Error parsing HTML content from {url} with BeautifulSoup: {e}")
            return None

    def scrape_pages(self) -> List[Dict[str, Any]]:
        """
        Scrapes the target Concordia pages using ScrapingBee GET requests
        and parses the HTML content with BeautifulSoup.
        """
        scraped_data = []
        if not self.api_key:
             logger.error("Cannot scrape, ScrapingBee API key is missing.")
             return []

        for url in self.TARGET_URLS:
            logger.debug(f"Attempting to fetch URL via ScrapingBee GET: {url}")
            try:
                response = requests.get(
                    'https://app.scrapingbee.com/api/v1/',
                    params={
                        'api_key': self.api_key,
                        'url': url,
                        'render_js': 'true', # Keep JS rendering enabled
                        # Add other params like 'premium_proxy': 'true' if needed and available
                    },
                    timeout=self.timeout
                )
                response.raise_for_status() # Raise for bad status codes (4xx or 5xx)

                # Get HTML content from the response
                html_content = response.text
                if not html_content:
                    logger.warning(f"ScrapingBee GET returned empty content for: {url}")
                    continue

                # Extract content using BeautifulSoup
                logger.debug(f"Parsing HTML content for {url} with BeautifulSoup...")
                content = self._extract_main_content(html_content, url)

                if content:
                    scraped_data.append({"source": url, "content": content})
                    logger.info(f"Successfully fetched and parsed content from: {url}")
                else:
                    logger.warning(f"Could not extract main content using BeautifulSoup from: {url}")

            except requests.exceptions.RequestException as e:
                http_error_msg = f" Status: {e.response.status_code}, Response: {e.response.text[:500]}..." if e.response is not None else ""
                logger.error(f"ScrapingBee API GET error scraping {url}: {e}{http_error_msg}")
            except Exception as e:
                logger.exception(f"Unexpected error processing URL {url}: {e}")

        logger.info(f"Web scraping/parsing complete. Successfully processed {len(scraped_data)} pages.")
        return scraped_data

# Example usage remains commented out

# Example usage (needs to be run from a context where .env is loaded)
# if __name__ == "__main__":
#     scraper = ConcordiaWebScraper()
#     data = scraper.scrape_pages()
#     if data:
#         print(f"Scraped {len(data)} pages.")
#         print("--- Sample Content ---")
#         print(f"Source: {data[0]['source']}")
#         print(data[0]['content'][:1000] + "...")
#     else:
#          print("No data scraped.") 