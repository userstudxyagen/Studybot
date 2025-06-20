import requests
import os
from dotenv import load_dotenv

# .env laden
load_dotenv()
API_TOKEN = os.getenv("HF_TOKEN")
if not API_TOKEN:
    raise ValueError("❌ API-Token (HF_TOKEN) konnte nicht geladen werden. Bitte in .env eintragen.")

# Modell-ID (kann auch dynamisch übergeben werden)
MODEL_ID = "HuggingFaceH4/zephyr-7b-beta"

def ask_model(prompt: str, model_id: str = MODEL_ID) -> str:
    url = f"https://api-inference.huggingface.co/models/{model_id}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 300,
            "temperature": 0.7
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)

        # Bei Fehler: Status + Inhalt anzeigen
        if response.status_code != 200:
            print("🔴 Fehler beim Aufruf des Modells:")
            print("Statuscode:", response.status_code)
            print("Antwort:", response.text)
            response.raise_for_status()

        output = response.json()

        # Erfolgreiche Antwort parsen
        if isinstance(output, list) and "generated_text" in output[0]:
            return output[0]["generated_text"]
        elif isinstance(output, dict) and "error" in output:
            return f"❌ Modellfehler: {output['error']}"
        else:
            return f"❌ Unerwartetes Antwortformat: {output}"

    except requests.exceptions.RequestException as e:
        return f"❌ Netzwerkfehler: {e}"
    except Exception as e:
        return f"❌ Allgemeiner Fehler: {e}"


# Beispielhafter Test
if __name__ == "__main__":
    frage = "Erkläre den Unterschied zwischen Listen und Tupeln in Python."
    antwort = ask_model(frage)
    print("Antwort vom Modell:\n", antwort)
