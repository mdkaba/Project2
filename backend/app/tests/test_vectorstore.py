from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
import numpy as np
import os
import sys

# Adjust path to import from app.core
# Go up two levels from test dir to get 'backend' dir
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, backend_dir) # Add backend directory to sys.path

from app.core.embeddings import SentenceTransformerEmbeddings

def test_vectorstore():
    print("Initializing embeddings...")
    
    # Create a test document
    test_doc_path = "test_document.txt"
    with open(test_doc_path, "w") as f:
        f.write("This is a test document about artificial intelligence and machine learning.")
    
    # Initialize the document loader
    loader = TextLoader(test_doc_path)
    documents = loader.load()
    
    try:
        # Initialize the embeddings model from the core module
        embeddings = SentenceTransformerEmbeddings()
        
        # Create the vector store
        # FAISS.from_documents handles text splitting and embedding implicitly
        # if documents are provided directly.
        vectorstore = FAISS.from_documents(documents, embeddings)
        
        # Test similarity search
        results = vectorstore.similarity_search("What is AI?", k=1)
        print("\u2713 Vector store test successful!")
        print(f"Found {len(results)} similar documents")
        if results:
            print(f"Most similar document: {results[0].page_content}")
        else:
            print("No similar documents found.")
        
    except Exception as e:
        print(f"\u2717 Error testing vector store: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up test file
        if os.path.exists(test_doc_path):
            os.remove(test_doc_path)

if __name__ == "__main__":
    test_vectorstore() 