import requests

def chat_with_deepseek(prompt, model="deepseek-coder"):
    url = "http://localhost:11434/api/generate"
    response = requests.post(url, json={
        "model": model,
        "prompt": prompt,
        "stream": False
    })
    return response.json().get("response", "No response.")