from app.agents.general_agent import get_general_agent
from app.agents.admissions_agent import get_admissions_agent
from app.agents.ai_agent import get_ai_agent

def route_query(query: str):
    if "admission" in query.lower() or "concordia" in query.lower():
        return get_admissions_agent().run(query)
    elif "AI" in query.lower() or "machine learning" in query.lower():
        return get_ai_agent().run(query)
    else:
        return get_general_agent().run(input=query)