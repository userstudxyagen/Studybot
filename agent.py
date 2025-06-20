import os
import json
import requests

API_URL = "https://router.huggingface.co/featherless-ai/v1/chat/completions"
HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise EnvironmentError("❌ Environment variable HF_TOKEN is not set.")

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload, stream=True)

    if response.status_code != 200:
        raise RuntimeError(f"❌ Request failed with status {response.status_code}: {response.text}")

    for line in response.iter_lines():
        if line:
            if line.strip() == b"data: [DONE]":
                break
            if line.startswith(b"data:"):
                data = json.loads(line.decode("utf-8").replace("data: ", ""))
                yield data

if __name__ == "__main__":
    chunks = query({
        "model": "HuggingFaceH4/zephyr-7b-beta",
        "messages": [
            {
                "role": "user",
                "content": "What is the capital of France?"
            }
        ],
        "stream": True
    })

    for chunk in chunks:
        delta = chunk["choices"][0].get("delta", {})
        content = delta.get("content")
        if content:
            print(content, end="", flush=True)
