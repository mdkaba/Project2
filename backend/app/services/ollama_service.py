from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.core.config import settings
from app.core.logger import logger

class OllamaService:
    def __init__(self):
        try:
            logger.info(f"Initializing Ollama LLM with base URL: {settings.OLLAMA_API_BASE_URL} and model: {settings.OLLAMA_MODEL_NAME}")
            self.llm = OllamaLLM(
                base_url=str(settings.OLLAMA_API_BASE_URL),
                model=settings.OLLAMA_MODEL_NAME
                # Add other parameters like temperature, top_k if needed
                # temperature=0.7
            )
            logger.info("Ollama LLM initialized successfully.")
            # Simple test invoke
            # logger.debug(f"Testing Ollama LLM connection: {self.llm.invoke('Why is the sky blue?')[:50]}...")
        except Exception as e:
            logger.exception(f"Failed to initialize Ollama LLM: {e}")
            # Depending on requirements, you might want to raise the exception
            # or handle it gracefully (e.g., set self.llm = None and check later)
            raise

    async def generate_response(self, prompt: ChatPromptTemplate, inputs: dict) -> str:
        """Generates a response using the configured LLM and prompt.

        Args:
            prompt: The ChatPromptTemplate to use.
            inputs: A dictionary containing values for the prompt template variables.

        Returns:
            The generated response string.
        """
        if not self.llm:
            logger.error("Ollama LLM is not available.")
            return "Error: The language model is not available."

        try:
            # Simple chain: prompt -> llm -> output parser
            chain = prompt | self.llm | StrOutputParser()
            logger.debug(f"Invoking LLM chain with inputs: {list(inputs.keys())}")
            # Use ainvoke for asynchronous execution
            response = await chain.ainvoke(inputs)
            logger.debug(f"Received LLM response.")
            return response
        except Exception as e:
            logger.exception(f"Error during LLM chain invocation: {e}")
            return f"Error generating response: {str(e)}"

# Singleton instance (optional, can use FastAPI dependency injection instead)
# ollama_service = OllamaService() 