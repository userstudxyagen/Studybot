import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("HUGGINGFACE_API_TOKEN")
if not API_KEY:
    raise ValueError("❌ API-Key konnte nicht geladen werden")

MODEL_ID = "google/flan-t5-large"  # or your chosen model

def ask_deepseek(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "inputs": prompt,
        # Optional: you can add parameters here, e.g. max_length, temperature, etc.
        # "parameters": {"max_new_tokens": 150}
    }

    try:
        url = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
        res = requests.post(url, headers=headers, json=data, timeout=20)
        res.raise_for_status()
        result = res.json()

        # Hugging Face models usually return a list of dicts with 'generated_text'
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]
        else:
            return f"❌ Unerwartetes Antwortformat: {result}"

    except requests.exceptions.RequestException as e:
        return f"❌ Netzwerkfehler: {e}"
    except Exception as e:
        return f"❌ Allgemeiner Fehler: {e}"
