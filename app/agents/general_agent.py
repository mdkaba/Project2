from app.ollama.ollama_llm import get_ollama_llm
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

def get_general_agent():
    llm = get_ollama_llm()
    memory = ConversationBufferMemory()
    return ConversationChain(llm=llm, memory=memory)