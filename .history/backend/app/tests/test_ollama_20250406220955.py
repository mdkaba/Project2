import requests
import json

def test_ollama():
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": "Say hello!",
                "stream": False  # Disable streaming for simpler response handling
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✓ Ollama is working correctly!")
            print("Response:", result.get("response", ""))
        else:
            print("✗ Error: Unexpected status code:", response.status_code)
    except Exception as e:
        print("✗ Error connecting to Ollama:", str(e))

if __name__ == "__main__":
    test_ollama() 