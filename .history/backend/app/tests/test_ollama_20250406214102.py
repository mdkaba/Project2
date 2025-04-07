import requests

def test_ollama():
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": "Say hello!"
            }
        )
        if response.status_code == 200:
            print("✓ Ollama is working correctly!")
            print("Response:", response.json().get("response", ""))
        else:
            print("✗ Error: Unexpected status code:", response.status_code)
    except Exception as e:
        print("✗ Error connecting to Ollama:", e)

if __name__ == "__main__":
    test_ollama() 