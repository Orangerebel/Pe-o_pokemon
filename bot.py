import requests
from bs4 import BeautifulSoup
import os
# --- KONFIGURÁCIA ---
TOKEN = "8630548470:AAEVaJUo4FnYuoM78BNQsi7989ozJfzU3EA"
ID = "7831610863"
DB_FILE = "history.txt"

WEBY = [
    "https://www.xzone.sk/sberatelske-hry-pokemon-tcg?sort=date_desc",
    "https://www.ihrysko.sk/vyhladavanie?search=pokemon&s=6",
    "https://www.dracik.sk/vyhladavanie/?search=pokemon",
    "https://www.brloh.sk/vyhladavanie?q=pokemon",
    "https://www.sparkys.sk/zberatelske-karty-pokemon/",
    "https://www.vesely-drak.sk/produkty/pokemon-edice/",
    "https://www.gengar.cz/sk/pokemon-tcg"
]

PRODUKTY = ["booster box", "booster bundle", "upc", "etb", "elite trainer box", "collection", "premium collection", "spc"]
DOSTUPNOST = ["do košíka", "skladom", "kúpiť", "vložiť do košíka", "koupit", "skladem"]

def load_history():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return set(f.read().splitlines())
    return set()

def save_history(history):
    with open(DB_FILE, "w") as f:
        f.write("\n".join(history))

def check_all():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    history = load_history()
    new_finds = False

    for url in WEBY:
        try:
            res = requests.get(url, headers=headers, timeout=25)
            soup = BeautifulSoup(res.content, "html.parser")
            
            # Prejdeme všetky odkazy na stránke
            for link in soup.find_all('a', href=True):
                text = link.get_text().lower()
                href = link['href']
                
                # Ak odkaz obsahuje tvoj produkt
                if any(p in text for p in PRODUKTY):
                    # Skontrolujeme, či je v okolí tlačidlo na kúpu (zjednodušene cez text stránky)
                    full_content = res.text.lower()
                    if any(d in full_content for d in DOSTUPNOST):
                        
                        # Opravíme relatívne linky (napr. /produkt na https://web.sk/produkt)
                        if href.startswith('/'):
                            base = url.split('/')[2]
                            href = f"https://{base}{href}"
                        
                        if href not in history:
                            msg = f"🎯 NOVÝ BOOSTER TY JEBO: {text.strip().upper()}\n🔗 Link: {href}"
                            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": ID, "text": msg})
                            history.add(href)
                            new_finds = True
        except:
            continue

    if new_finds:
        save_history(history)

if __name__ == "__main__":
    check_all()
