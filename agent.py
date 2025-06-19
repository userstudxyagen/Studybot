import os
import requests

API_KEY = os.getenv("OPENROUTER_API_KEY")


def ask_deepseek(prompt, model="deepseek-chat"):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "https://huggingface.co",
        "Content-Type": "application/json",
    }
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Du bist ein KI-Studienassistent."},
            {"role": "user", "content": prompt}
        ]
    }
    res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    return res.json()["choices"][0]["message"]["content"]
