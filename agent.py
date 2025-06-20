import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("HF_TOKEN")
if not API_TOKEN:
    raise ValueError("API-Token konnte nicht geladen werden")

MODEL_ID = "mistralai/Mixtral-8x7B-Instruct-v0.1"

def ask_model(prompt):
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "inputs": prompt,
        # Falls gewünscht, kannst du hier Parameter ergänzen, z.B. max_length
    }

    url = f"https://api-inference.huggingface.co/models/{MODEL_ID}"

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    output = response.json()

    if isinstance(output, list) and "generated_text" in output[0]:
        return output[0]["generated_text"]
    else:
        return f"Unerwartetes Antwortformat: {output}"

# Beispiel-Aufruf
if __name__ == "__main__":
    frage = "Was ist die Hauptstadt von Frankreich?"
    antwort = ask_model(frage)
    print(antwort)
