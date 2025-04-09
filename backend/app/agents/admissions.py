from typing import Dict, Any, List, Optional
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.documents import Document

from app.agents.base import BaseAgent
from app.services.ollama_service import OllamaService
from app.core.logger import logger

# Initialize services needed
ollama_service = OllamaService()

class AdmissionsAgent(BaseAgent):
    """Agent specialized in Concordia Computer Science admissions."""

    def get_name(self) -> str:
        return "AdmissionsAgent"

    async def should_handle(self, query: str, history: list[Dict[str, str]]) -> float:
        """
        Determines if this agent should handle the query.
        Higher confidence for admission-related keywords.
        """
        keywords = ["admission", "admit", "apply", "application", "requirement", "prerequisite", "gpa", "r-score", "cegep", "deadline", "tuition", "computer science", "bcompsc"]
        query_lower = query.lower()
        score = 0.1
        if "concordia" in query_lower or any(keyword in query_lower for keyword in keywords):
            score += 0.8
            logger.debug(f"{self.get_name()} handling score boosted by keywords.")
        # TODO: Improve using embeddings against representative admissions queries
        return min(score, 1.0)

    async def process(self, query: str, history: list[Dict[str, str]], context_docs: list[Document] = None) -> str:
        """Processes an admissions query using retrieved context documents."""
        logger.info(f"{self.get_name()} processing query: '{query}'")

        # Context documents (containing scraped info) are passed in by ChatService
        formatted_context = "\n\n".join([f"Source {i+1} ({doc.metadata.get('source', 'Unknown')}):\n{doc.page_content}" for i, doc in enumerate(context_docs or [])])

        if not formatted_context:
             logger.warning("AdmissionsAgent received no context documents for RAG.")
             # Provide a clearer message if context is missing
             return "I currently lack the specific documents needed to answer that question about Concordia admissions. Please try rephrasing or asking a different question."


        # --- Prepare New Prompt ---
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"""You are the {self.get_name()}, a specialized AI assistant providing information about **undergraduate Computer Science (BCompSc - General Program)** admissions at Concordia University.

Your task is to answer the user's query based **strictly and solely** on the information contained within the provided 'Context Documents' below. These documents are extracts from the official Concordia University website. Do not use any external knowledge or make assumptions beyond what is stated in the context.

**Instructions:**

1.  **Focus:** Your answers must pertain *only* to the BCompSc - General Program admissions.
2.  **Synthesize for General Queries:** If the user asks a general question like \"What are the admission requirements?"", carefully review all provided context documents. Extract the key requirements (e.g., minimum R-score overall, minimum Math R-score, required CEGEP/High School courses like Calculus/Linear Algebra/Physics, English proficiency standards, application deadlines if mentioned) specifically mentioned for the BCompSc General Program. Present these requirements clearly, preferably as a bulleted list.
3.  **Specific Queries:** Answer specific questions directly using the relevant information found in the context.
4.  **Missing Information:** If the provided context documents do not contain the specific information needed to answer the user's question about the BCompSc General Program, clearly state that the information is not available in the documents you have access to. Do not attempt to guess or provide information from outside the context.
5.  **Tone:** Be helpful, accurate, and polite.

Context Documents:
-------------------
{formatted_context}
-------------------"""),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{query}"),
        ])

        inputs = {
            "query": query,
            "history": history
            # Context is injected into system prompt
        }

        # --- Call LLM ---
        response = await ollama_service.generate_response(prompt, inputs)
        return response 