import requests

def chat_with_model(prompt, model="HuggingFaceH4/zephyr-7b-beta"):
    url = "http://localhost:11434/api/generate"
    response = requests.post(url, json={
        "model": model,
        "prompt": prompt,
        "stream": False
    })
    return response.json().get("response", "No response.")
