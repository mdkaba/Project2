from typing import Dict, Any, List, Optional
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from app.agents.base import BaseAgent
from app.services.ollama_service import OllamaService
from app.services.knowledge_service import KnowledgeService # Uses ArXiv, GitHub
from app.core.logger import logger

# Initialize services needed
ollama_service = OllamaService()
knowledge_service = KnowledgeService()

class AIExpertAgent(BaseAgent):
    """Agent specialized in AI, ML, and related technical topics."""

    def get_name(self) -> str:
        return "AIExpertAgent"

    async def should_handle(self, query: str, history: list[Dict[str, str]]) -> float:
        """
        Determines if this agent should handle the query.
        Higher confidence for AI/ML terms, papers, code, technical questions.
        """
        keywords = ["ai", "artificial intelligence", "machine learning", "deep learning", "neural network", "transformer", "llm", "paper", "arxiv", "github", "code", "algorithm", "pytorch", "tensorflow"]
        query_lower = query.lower()
        score = 0.1
        if any(keyword in query_lower for keyword in keywords):
            score += 0.8
            logger.debug(f"{self.get_name()} handling score boosted by keywords.")
        # TODO: Improve using embeddings against representative AI queries
        return min(score, 1.0)

    async def process(self, query: str, history: list[Dict[str, str]], context_docs: list[Any] = None) -> str:
        """Processes an AI/ML query, potentially using ArXiv/GitHub."""
        logger.info(f"{self.get_name()} processing query: '{query}'")

        # --- Tool Use ---
        tool_results_str = ""
        # Simple logic: If query asks for papers or code, use tools
        if "paper" in query.lower() or "arxiv" in query.lower():
            logger.debug("AIExpertAgent searching ArXiv...")
            papers = await knowledge_service.search_arxiv(query, max_results=2)
            if papers:
                tool_results_str += "\n\nRelevant ArXiv Papers Found:\n" + "\n---\n".join([
                    f"Title: {p.get('title', 'N/A')}\nAuthors: {', '.join(p.get('authors',[]))}\nURL: {p.get('pdf_url', 'N/A')}\nSummary: {p.get('summary', 'N/A')[:200]}..."
                    for p in papers
                ])
                logger.debug("Added ArXiv results to context.")

        # Refined logic: Trigger GitHub search on more specific action phrases
        query_lower = query.lower()
        github_action_phrases = [
            "find github", "search github", "show github", "look for github",
            "find repository", "find repositories", "search repository", "search repositories",
            "show repository", "show repositories", "look for repository", "look for repositories"
        ]
        trigger_github_search = any(phrase in query_lower for phrase in github_action_phrases)

        if trigger_github_search:
             logger.debug("AIExpertAgent searching GitHub Repos based on action phrase...")
             # Note: This call is currently blocking
             repos = await knowledge_service.search_github_repos(query, max_results=2)
             if repos:
                  tool_results_str += "\n\nRelevant GitHub Repositories Found:\n" + "\n---\n".join([
                     f"Name: {r.get('name', 'N/A')}\nURL: {r.get('url', 'N/A')}\nDescription: {r.get('description', 'N/A')}\nStars: {r.get('stars', 'N/A')}"
                     for r in repos
                  ])
                  logger.debug("Added GitHub repo results to context.")
        elif "code" in query_lower or "implementation" in query_lower:
             # Optional: Consider adding GitHub code search trigger here if desired later
             # For now, only trigger repo search on specific phrases
             logger.debug(f"Query mentioned '{query_lower}' but didn't match specific GitHub action phrases; skipping GitHub repo search.")


        # --- Prepare Prompt ---
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"""You are the {self.get_name()}, specializing in AI, Machine Learning, and related technical topics.
Answer the user's question clearly and concisely based on the conversation history and any provided tool results (ArXiv papers, GitHub repos).
Explain technical concepts accurately.

Tool Results:
{tool_results_str}"""),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{query}"),
        ])

        inputs = {
            "query": query,
            "history": history
            # Tool results injected into system prompt
        }

        # --- Call LLM ---
        response = await ollama_service.generate_response(prompt, inputs)
        return response 