import requests

from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise ValueError("❌ API-Key konnte nicht geladen werden")

def ask_deepseek(prompt, model="deepseek-r1-0528"):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Du bist ein KI-Studienassistent."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=20)
        res.raise_for_status()
        result = res.json()

        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        else:
            return f"❌ Unerwartetes Antwortformat: {result}"

    except requests.exceptions.RequestException as e:
        return f"❌ Netzwerkfehler: {e}"
    except Exception as e:
        return f"❌ Allgemeiner Fehler: {e}"
