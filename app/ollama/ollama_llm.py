from langchain_community.chat_models import ChatOllama

def get_ollama_llm():
    return ChatOllama(model="mistral")