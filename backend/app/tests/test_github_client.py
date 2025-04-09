# backend/app/tests/test_github_client.py
import sys
import os
import json # To pretty-print results

# Ensure the backend directory is in the Python path
# Go up two levels from tests dir to get 'backend' dir
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, backend_dir)

from dotenv import load_dotenv
from app.knowledge.github_client import GitHubClient
# Use standard logging for tests
import logging

load_dotenv()

def run_github_tests():
    logging.info("--- Starting GitHub Client Test ---")

    # --- Initialize Client ---
    try:
        logging.info("Initializing GitHubClient...")
        client = GitHubClient()
        if not client.client: # Check if initialization failed
             logging.error("GitHub client could not be initialized (check token/logs). Aborting test.")
             return
        logging.info("GitHubClient initialized successfully.")
    except Exception as e:
        logging.exception(f"Failed to initialize GitHubClient: {e}")
        return

    # --- Test Repository Search ---
    repo_query = "langchain-ai/langchain"
    logging.info(f"--- Testing Repository Search for query: '{repo_query}' ---")
    try:
        repos = client.search_repositories(query=repo_query, max_results=3)
        if repos:
            logging.info(f"Found {len(repos)} repositories:")
            # Pretty print the first result
            print(json.dumps(repos[0], indent=2))
            # Print just names of others
            for i, repo in enumerate(repos[1:], 1):
                 print(f"  Repo {i+1}: {repo.get('name')}")
        else:
            logging.info("No repositories found for this query.")
    except Exception as e:
        logging.exception(f"Error during repository search test: {e}")

    # --- Test Code Search (Optional) ---
    code_query = "ollama fastapi integration example"
    language = "python"
    logging.info(f"--- Testing Code Search for query: '{code_query}' (language: {language}) ---")
    try:
        code_files = client.search_code(query=code_query, max_results=3, language=language)
        if code_files:
            logging.info(f"Found {len(code_files)} code files:")
            # Print file details
            for i, file_info in enumerate(code_files, 1):
                 print(f"  File {i}: {file_info.get('repository')}/{file_info.get('path')} ({file_info.get('file_url')})")
        else:
            logging.info("No code files found for this query.")
    except Exception as e:
        logging.exception(f"Error during code search test: {e}")

    logging.info("--- GitHub Client Test Finished ---")

if __name__ == "__main__":
    # Setup basic logging for script execution
    log_level_str = os.getenv('LOG_LEVEL', 'INFO').upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    logging.basicConfig(level=log_level, format='%(asctime)s | %(levelname)-8s | %(name)-25s:%(lineno)-4d | %(message)s')

    run_github_tests() 