from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader

def test_vectorstore():
    print("Initializing embeddings...")
    
    # Create a test document
    with open("test_document.txt", "w") as f:
        f.write("This is a test document about artificial intelligence and machine learning.")
    
    # Initialize the document loader
    loader = TextLoader("test_document.txt")
    documents = loader.load()
    
    try:
        # Initialize the model
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        
        # Create a wrapper class for the model to work with LangChain
        class STEmbeddings:
            def __init__(self, model):
                self.model = model
            
            def embed_documents(self, texts):
                embeddings = self.model.encode(texts)
                return embeddings.tolist()
            
            def embed_query(self, text):
                embedding = self.model.encode([text])[0]
                return embedding.tolist()
        
        embeddings = STEmbeddings(model)
        
        # Create the vector store
        vectorstore = FAISS.from_documents(documents, embeddings)
        
        # Test similarity search
        results = vectorstore.similarity_search("What is AI?", k=1)
        print("✓ Vector store test successful!")
        print(f"Found {len(results)} similar documents")
        print(f"Most similar document: {results[0].page_content}")
        
    except Exception as e:
        print(f"✗ Error testing vector store: {str(e)}")
    
    # Clean up test file
    import os
    if os.path.exists("test_document.txt"):
        os.remove("test_document.txt")

if __name__ == "__main__":
    test_vectorstore() 