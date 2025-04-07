from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
import os

def test_vectorstore():
    try:
        # Initialize embeddings
        print("\nInitializing embeddings...")
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2"
        )
        
        # Create test document
        test_content = "This is a test document for vector store. It contains information about Concordia University's computer science program."
        test_file = "test_doc.txt"
        
        with open(test_file, "w") as f:
            f.write(test_content)
        
        # Load document
        print("Loading test document...")
        loader = TextLoader(test_file)
        documents = loader.load()
        
        # Create vector store
        print("Creating vector store...")
        vectorstore = FAISS.from_documents(documents, embeddings)
        
        # Test search
        print("Testing similarity search...")
        results = vectorstore.similarity_search("computer science program")
        print("\n✓ Vector store test successful!")
        print("Search results:", results[0].page_content if results else "No results")
        
        # Cleanup
        os.remove(test_file)
    except Exception as e:
        print("\n✗ Error testing vector store:", e)

if __name__ == "__main__":
    test_vectorstore() 