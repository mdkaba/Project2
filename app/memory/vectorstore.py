import chromadb

def get_vectorstore():
    return chromadb.Client().create_collection("chat_history")