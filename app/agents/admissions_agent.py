from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from app.ollama.ollama_llm import get_ollama_llm

def get_admissions_agent():
    template = """You are an expert on Concordia University's Computer Science admissions.
    {question}"""
    prompt = PromptTemplate(template=template, input_variables=["question"])
    llm = get_ollama_llm()
    return LLMChain(llm=llm, prompt=prompt)