from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from app.ollama.ollama_llm import get_ollama_llm

def get_ai_agent():
    llm = get_ollama_llm()
    memory = ConversationBufferMemory()
    return ConversationChain(llm=llm, memory=memory)