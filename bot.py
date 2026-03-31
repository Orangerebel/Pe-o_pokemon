import requests

# --- KONFIGURÁCIA ---
TOKEN = "8630548470:AAEVaJUo4FnYuoM78BNQsi7989ozJfzU3EA"
ID = "7831610863"

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
    "etb", "elite trainer box", "collection", "premium collection",
    "spc", "super premium collection"
]

# Musí tam byť aj potvrdenie, že sa to dá kúpiť (nie len vypredaný archív):
DOSTUPNOST = ["do košíka", "skladom", "kúpiť", "vložiť do košíka", "koupit", "skladem"]

def check_all():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    for url in WEBY:
        try:
            res = requests.get(url, headers=headers, timeout=25)
            obsah = res.text.lower()
            
            # Logika: Ak je tam nejaký tvoj produkt A ZÁROVEŇ sa dá kúpiť
            naskladnene = [p for p in PRODUKTY if p in obsah]
            je_skladom = any(d in obsah for d in DOSTUPNOST)
            
            if naskladnene and je_skladom:
                najdene_veci = ", ".join(naskladnene).upper()
                msg = f"🎯 SNIPER ALERT: {najdene_veci}!\nKukaj tu: {url}"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                              json={"chat_id": ID, "text": msg})
                print(f"Zásah na: {url} ({najdene_veci})")
            else:
                print(f"Na {url} nič z tvojho výberu.")
                
        except Exception as e:
            print(f"Chyba pri {url}: {e}")

if __name__ == "__main__":
    check_all()
