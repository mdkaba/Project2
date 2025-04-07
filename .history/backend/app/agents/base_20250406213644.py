from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.embeddings = HuggingFaceEmbeddings()
        self.vector_store: Optional[FAISS] = None
        
    @abstractmethod
    async def process(self, query: str, context: Dict[str, Any]) -> str:
        """Process a query and return a response"""
        pass
        
    @abstractmethod
    async def should_handle(self, query: str) -> float:
        """Return confidence score (0-1) for handling this query"""
        pass
    
    def _get_relevant_context(self, query: str) -> str:
        """Get relevant context from vector store if available"""
        if self.vector_store:
            docs = self.vector_store.similarity_search(query, k=3)
            return "\n".join(doc.page_content for doc in docs)
        return ""
    
    def add_to_memory(self, query: str, response: str):
        """Add interaction to memory"""
        self.memory.save_context(
            {"input": query},
            {"output": response}
        ) 