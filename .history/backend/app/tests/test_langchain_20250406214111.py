from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

def test_langchain():
    try:
        # Initialize Ollama with streaming
        llm = Ollama(
            model="mistral",
            callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
        )
        
        # Test generation
        print("\nTesting LangChain with Ollama...")
        response = llm("Explain what is artificial intelligence in one sentence.")
        print("\n✓ LangChain + Ollama integration is working!")
    except Exception as e:
        print("\n✗ Error testing LangChain:", e)

if __name__ == "__main__":
    test_langchain() 