from langchain_community.embeddings import OpenAIEmbeddings
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
    
    # Initialize embeddings
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key="dummy-key"  # This is just for testing
    )
    
    try:
        # Create the vector store
        vectorstore = FAISS.from_documents(documents, embeddings)
        
        # Test similarity search
        results = vectorstore.similarity_search("What is AI?", k=1)
        print("✓ Vector store test successful!")
        print(f"Found {len(results)} similar documents")
        
    except Exception as e:
        print(f"✗ Error testing vector store: {str(e)}")
    
    # Clean up test file
    import os
    if os.path.exists("test_document.txt"):
        os.remove("test_document.txt")

if __name__ == "__main__":
    test_vectorstore() 