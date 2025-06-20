import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("HF_TOKEN")
if not API_KEY:
    raise ValueError("❌ API-Key konnte nicht geladen werden")

MODEL_ID = "mistralai/Mixtral-8x7B-Instruct-v0.1"

def ask_deepseek(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "inputs": prompt,
    }

    try:
        url = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
        res = requests.post(url, headers=headers, json=data, timeout=20)
        res.raise_for_status()
        result = res.json()

        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]
        else:
            return f"❌ Unerwartetes Antwortformat: {result}"

    except requests.exceptions.RequestException as e:
        return f"❌ Netzwerkfehler: {e}"
    except Exception as e:
        return f"❌ Allgemeiner Fehler: {e}"
