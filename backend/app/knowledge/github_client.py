from github import Github, GithubException, RateLimitExceededException
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.core.logger import logger

class GitHubClient:
    """Client for interacting with the GitHub API."""
    def __init__(self):
        self.github_token = settings.GITHUB_PAT
        self.client: Optional[Github] = None

        if not self.github_token:
            logger.warning("GITHUB_PAT not found in environment variables. GitHubClient will have limited functionality (rate limits).")
            # Initialize without token for limited public access
            self.client = Github()
        else:
            try:
                self.client = Github(self.github_token)
                # Test connection by getting authenticated user (optional)
                user = self.client.get_user()
                logger.info(f"GitHubClient initialized and authenticated as: {user.login}")
            except RateLimitExceededException:
                 logger.error("GitHub API rate limit exceeded during initialization. Check token usage.")
                 # Decide how to handle - maybe still initialize unauthenticated?
                 self.client = Github() # Fallback to unauthenticated
            except GithubException as e:
                logger.exception(f"Failed to initialize GitHub client with token: {e.status} {e.data}")
                self.client = Github() # Fallback to unauthenticated
            except Exception as e:
                 logger.exception(f"An unexpected error occurred during GitHub client initialization: {e}")
                 self.client = None # Indicate failure

    def _extract_keywords_from_query(self, query: str) -> str:
        """Simple heuristic to extract likely keywords from a natural language query."""
        query_lower = query.lower()
        # Remove common action phrases used for triggering
        action_phrases_to_remove = [
            "search github for repositories related to",
            "search github for repositories",
            "search github for",
            "find github repository for",
            "find github repositories for",
            "find github",
            "show github repositories for",
            "show github repository",
            "look for github repository",
            "look for github repositories",
            "search repositories for",
            "search repository for",
            "find repositories for",
            "find repository for",
            "repositories related to",
            "repository related to",
            # Add more variations as needed
        ]
        # Sort by length descending to remove longer phrases first
        action_phrases_to_remove.sort(key=len, reverse=True)

        extracted_term = query_lower
        for phrase in action_phrases_to_remove:
            if phrase in extracted_term:
                extracted_term = extracted_term.replace(phrase, "").strip()
                break # Assume first match is good enough for this simple heuristic

        # Remove common leading/trailing words if needed (e.g., 'about', 'implementations')
        # This part can be expanded
        extracted_term = extracted_term.replace("about", "").strip()

        # If empty after stripping, fallback to original query? Or handle error?
        if not extracted_term:
            logger.warning(f"Could not extract keyword from query: '{query}'. Using original.")
            return query # Fallback to original query if extraction fails

        logger.debug(f"Extracted search term '{extracted_term}' from query '{query}'")
        return extracted_term

    def search_repositories(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Searches for repositories on GitHub, extracting keywords first."""
        if not self.client:
             logger.error("GitHub client not initialized.")
             return []

        # Extract keywords before searching
        search_term = self._extract_keywords_from_query(query)

        logger.debug(f"Searching GitHub repositories for extracted term: '{search_term}' (original query: '{query}')")
        results_list = []
        try:
            # Search repositories using the extracted term
            repositories = self.client.search_repositories(query=search_term, sort="stars", order="desc")
            count = 0
            for repo in repositories:
                if count >= max_results:
                    break
                repo_details = {
                    "name": repo.full_name,
                    "url": repo.html_url,
                    "description": repo.description,
                    "stars": repo.stargazers_count,
                    "language": repo.language,
                    "last_updated": repo.updated_at.strftime('%Y-%m-%d')
                }
                results_list.append(repo_details)
                logger.debug(f"Found GitHub repo: {repo.full_name}")
                count += 1

            logger.info(f"GitHub repository search for term '{search_term}' yielded {len(results_list)} results.")
            return results_list

        except RateLimitExceededException:
             logger.warning(f"GitHub API rate limit exceeded during repository search for '{search_term}'.")
             return results_list # Return potentially partial results
        except GithubException as e:
            logger.exception(f"GitHub API error during repository search for '{search_term}': {e.status} {e.data}")
            return []
        except Exception as e:
            logger.exception(f"Unexpected error during GitHub repository search for '{search_term}': {e}")
            return []

    def search_code(self, query: str, max_results: int = 5, language: Optional[str] = None) -> List[Dict[str, Any]]:
        """Searches for code snippets on GitHub."""
        if not self.client:
             logger.error("GitHub client not initialized.")
             return []

        logger.debug(f"Searching GitHub code for: '{query}' (language: {language})")
        qualifiers = {}
        if language:
            qualifiers["language"] = language

        results_list = []
        try:
            code_results = self.client.search_code(query=query, qualifiers=qualifiers, sort="indexed", order="desc") # or sort='best-match'
            count = 0
            for code_file in code_results:
                 if count >= max_results:
                     break
                 # Getting content might require another API call per file - be careful with rate limits!
                 # For snippets, maybe just return file info initially.
                 try:
                     # Limit snippet size for preview
                     # content_snippet = code_file.decoded_content.decode('utf-8', errors='ignore')[:500]
                     file_details = {
                         "file_url": code_file.html_url,
                         "repository": code_file.repository.full_name,
                         "path": code_file.path,
                         # "snippet": content_snippet + "..." if len(code_file.decoded_content) > 500 else content_snippet
                     }
                     results_list.append(file_details)
                     logger.debug(f"Found GitHub code file: {code_file.repository.full_name}/{code_file.path}")
                     count += 1
                 except GithubException as e_file:
                      logger.warning(f"Could not access file content for {code_file.html_url}: {e_file.status}")
                 except Exception as e_decode:
                     logger.warning(f"Could not decode content for {code_file.html_url}: {e_decode}")


            logger.info(f"GitHub code search for '{query}' yielded {len(results_list)} results.")
            return results_list

        except RateLimitExceededException:
             logger.warning("GitHub API rate limit exceeded during code search.")
             return results_list # Return potentially partial results
        except GithubException as e:
            logger.exception(f"GitHub API error during code search for '{query}': {e.status} {e.data}")
            return []
        except Exception as e:
            logger.exception(f"Unexpected error during GitHub code search for '{query}': {e}")
            return []

# Example usage:
# github_client = GitHubClient()
# repos = github_client.search_repositories("langchain fastapi", max_results=3)
# for repo in repos: print(repo)
# code = github_client.search_code("uvicorn.run", language="python", max_results=2)
# for c in code: print(c) 