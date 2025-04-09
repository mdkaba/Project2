# backend/app/agents/general.py
from typing import Dict, Any, List, Optional
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from app.agents.base import BaseAgent
from app.services.ollama_service import OllamaService
from app.services.knowledge_service import KnowledgeService # Uses WebSearch, Wikipedia
from app.core.logger import logger

# Initialize services needed
ollama_service = OllamaService()
knowledge_service = KnowledgeService()

class GeneralAgent(BaseAgent):
    """Agent for handling general knowledge questions."""

    def get_name(self) -> str:
        return "GeneralAgent"

    async def should_handle(self, query: str, history: list[Dict[str, str]]) -> float:
        """
        Acts as the default agent if others don't have high confidence.
        Confidence can be slightly boosted by general knowledge keywords.
        """
        # This agent is often the fallback, so starts with a moderate score
        score = 0.5
        # Can add logic to slightly decrease score if AI or Admissions keywords are present
        if "wikipedia" in query.lower() or "search" in query.lower() or "what is" in query.lower():
            score = min(score + 0.2, 1.0) # Slightly boost for explicit requests
            logger.debug(f"{self.get_name()} handling score boosted by keywords.")

        # TODO: Reduce score if AI/Admissions keywords are strong?
        return score

    async def process(self, query: str, history: list[Dict[str, str]], context_docs: list[Any] = None) -> str:
        """Processes a general query, potentially using Web Search or Wikipedia."""
        logger.info(f"{self.get_name()} processing query: '{query}'")

        # --- Tool Use (Example: Prioritize Wikipedia Summary, then Web Search) ---
        tool_results_str = ""
        # 1. Try Wikipedia Summary
        # Note: Blocking call
        wiki_summary = await knowledge_service.get_wikipedia_summary(query, sentences=3)
        if wiki_summary:
            logger.debug("Found Wikipedia summary, using as context.")
            tool_results_str = f"Wikipedia Summary for '{query}':\n{wiki_summary}"
        else:
            # 2. If no Wiki summary, try Web Search
            logger.debug("No Wikipedia summary found, trying web search...")
            web_results = await knowledge_service.search_web(query, max_results=3)
            if web_results:
                tool_results_str = "Relevant Web Search Results:\n" + "\n---\n".join([
                    f"Title: {r.get('title', 'N/A')}\nURL: {r.get('href', 'N/A')}\nSnippet: {r.get('body', 'N/A')}"
                    for r in web_results
                ])
                logger.debug("Added web search results to context.")
            else:
                 logger.debug("No relevant tool results found for general query.")
                 tool_results_str = "No specific external information found for this query."


        # --- Prepare Prompt ---
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"""You are the {self.get_name()}, a helpful AI assistant designed to answer general knowledge questions.
Use the conversation history and the provided external information (Wikipedia summary or Web Search results) if available and relevant.
If no external information is provided or relevant, answer based on your general knowledge.
Be concise and informative.

External Information Found:
{tool_results_str}"""),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{query}"),
        ])

        inputs = {
            "query": query,
            "history": history
            # External info injected into system prompt
        }

        # --- Call LLM ---
        response = await ollama_service.generate_response(prompt, inputs)
        return response 