import requests
from bs4 import BeautifulSoup # type: ignore

def scrape_text_from_url(url):
    try:
        html = requests.get(url, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")
        return " ".join(p.get_text() for p in soup.find_all("p"))[:4000]
    except Exception as e:
        return f"Fehler: {e}"