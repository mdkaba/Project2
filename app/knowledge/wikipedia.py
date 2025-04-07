import wikipedia

def search_wikipedia(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except Exception:
        return "No relevant Wikipedia data found."