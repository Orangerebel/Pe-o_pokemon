import requests
import os 

# --- KONFIGURÁCIA ---
TOKEN = "8630548470:AAEVaJUo4FnYuoM78BNQsi7989ozJfzU3EA"
ID = "7831610863"
DB_FILE = "history.txt"

# VŠETKY WEBY, KTORÉ SLEDUJEME:
WEBY = [
    "https://www.xzone.sk/sberatelske-hry-pokemon-tcg?sort=date_desc",
    "https://www.ihrysko.sk/vyhladavanie?search=pokemon&s=6",
    "https://www.dracik.sk/vyhladavanie/?search=pokemon",
    "https://www.brloh.sk/vyhladavanie?q=pokemon",
    "https://www.sparkys.sk/zberatelske-karty-pokemon/",
    "https://www.vesely-drak.sk/produkty/pokemon-edice/",
    "https://www.gengar.cz/sk/pokemon-tcg"
]

# TVOJE ŠPECIÁLNE PRODUKTY (Sniper mode):
PRODUKTY = [
    "booster box", "booster bundle", "upc", "ultra premium collection", 
    "etb", "elite trainer box", "collection", "premium collection", "spc"
]

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
    headers = {"User-Agent": "Mozilla/5.0"}
    history = load_history()
    new_finds = []

    for url in WEBY:
        try:
            res = requests.get(url, headers=headers, timeout=25)
            obsah = res.text.lower()
            
            # Hľadáme tvoje produkty
            najdene = [p for p in PRODUKTY if p in obsah]
            je_skladom = any(d in obsah for d in DOSTUPNOST)
            
            if najdene and je_skladom:
                # Vytvoríme unikátny kľúč (napr. "dracik-etb")
                found_key = f"{url}-{najdene[0]}"
                
                if found_key not in history:
                    new_finds.append((url, najdene[0].upper()))
                    history.add(found_key)
        except:
            continue

    if new_finds:
        for url, item in new_finds:
            msg = f"✨ NOVINKA DETEKOVANÁ: {item}\nLink: {url}"
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": ID, "text": msg})
        save_history(history)

if __name__ == "__main__":
    check_all()
