import requests
from bs4 import BeautifulSoup
import os
import sys

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

PRODUKTY = ["booster box", "booster bundle", "upc", "etb", "elite trainer box", "collection", "premium collection"]

def load_history():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return set(f.read().splitlines())
    return set()

def save_history(history):
    with open(DB_FILE, "w") as f:
        f.write("\n".join(sorted(history)))

def check_all():
    if not TOKEN or not ID:
        print("Chýba TOKEN alebo ID v Secrets!")
        sys.exit(1)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    history = load_history()
    new_finds = False

    for url in WEBY:
        try:
            print(f"Kontrolujem: {url}")
            res = requests.get(url, headers=headers, timeout=20)
            res.raise_for_status()
            soup = BeautifulSoup(res.content, "html.parser")
            
            for link in soup.find_all('a', href=True):
                text = link.get_text().lower().strip()
                href = link['href']
                
                # Filter na kľúčové slová
                if any(p in text for p in PRODUKTY):
                    # Ošetrenie URL
                    if href.startswith('/'):
                        base = url.split('/')[2]
                        href = f"https://{base}{href}"
                    
                    if href not in history:
                        # Overenie, či je to fakt produkt (odfiltrovanie menu a pod.)
                        if len(text) > 10: 
                            msg = f"🎯 NOVÝ POKÉMON DROOP: {text.upper()}\n🔗 Link: {href}"
                            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                                          json={"chat_id": ID, "text": msg})
                            history.add(href)
                            new_finds = True
                            print(f"Nájdené: {text}")
        except Exception as e:
            print(f"Chyba na {url}: {e}")
            continue

    if new_finds:
        save_history(history)
        return True
    return False

if __name__ == "__main__":
    check_all()
