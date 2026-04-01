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

# Kľúčové slová - iba produkty, ktoré ťa reálne zaujímajú
PRODUKTY = ["booster box", "booster bundle", "upc", "etb", "elite trainer box", "collection"]

def load_history():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return set(f.read().splitlines())
    return set()

def save_history(history):
    with open(DB_FILE, "w") as f:
        f.write("\n".join(sorted(history)))

def check_all():
    history = load_history()
    new_items_found = [] # Tu si budeme ukladať len tie, čo ešte nepoznáme
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    for url in WEBY:
        try:
            res = requests.get(url, headers=headers, timeout=15)
            if res.status_code != 200: continue
            
            soup = BeautifulSoup(res.content, "html.parser")
            
            for link in soup.find_all('a', href=True):
                href = link['href']
                text = link.get_text().lower().strip()

                # Oprava relatívnej cesty
                if href.startswith('/'):
                    base = url.split('/')[2]
                    href = f"https://{base}{href}"

                # LOGIKA: Musí obsahovať kľúčové slovo A nesmie byť v histórii
                if any(p in text for p in PRODUKTY):
                    if href not in history:
                        # Ak sme sem došli, našli sme SKUTOČNE novú vec
                        new_items_found.append((text.upper(), href))
                        history.add(href) # Pridáme hneď do pamäte, aby sme o tom druhýkrát nepísali
        except:
            continue

    # ODOSIELANIE: Iba ak zoznam nových vecí nie je prázdny
    if new_items_found:
        for name, link in new_items_found:
            msg = f"🔥 NOVINKA: {name}\n🔗 {link}"
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": ID, "text": msg})
        
        # Uložíme aktualizovanú históriu späť do súboru na GitHub
        save_history(history)
        print(f"Nájdených {len(new_items_found)} nových produktov. Správy odoslané.")
    else:
        print("Nič nové sa nenašlo. Telegram zostáva ticho.")

if __name__ == "__main__":
    check_all()
