from sentence_transformers import SentenceTransformer
from langchain_core.embeddings import Embeddings
from typing import List

class SentenceTransformerEmbeddings(Embeddings):
    """LangChain compatible embeddings wrapper for Sentence Transformers."""
    def __init__(self, model_name: str = 'sentence-transformers/all-MiniLM-L6-v2'):
        # Initialize the Sentence Transformer model
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents."""
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()

    def embed_query(self, text: str) -> List[float]:
        """Embed a single query."""
        embedding = self.model.encode([text], convert_to_numpy=True)[0]
        return embedding.tolist()

    # Optional: If you need direct call compatibility, though embed_documents/embed_query are standard
    # def __call__(self, text):
    #     if isinstance(text, str):
    #         return self.embed_query(text)
    #     return self.embed_documents(text) 