from langchain_ollama import OllamaLLM
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

def test_langchain():
    try:
        # Initialize Ollama
        llm = OllamaLLM(
            model="mistral",
            callbacks=[StreamingStdOutCallbackHandler()]
        )
        
        # Test generation
        print("\nTesting LangChain with Ollama...")
        response = llm("Explain what is artificial intelligence in one sentence.")
        print("\n✓ LangChain + Ollama integration is working!")
    except Exception as e:
        print("\n✗ Error testing LangChain:", e)

if __name__ == "__main__":
    test_langchain() 