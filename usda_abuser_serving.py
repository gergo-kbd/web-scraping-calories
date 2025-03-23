import requests
import json

API_KEY = "C2hbBSIucd88eskFFJphpWYc30JmA6Tv45Rn421I"  # Itt add meg a saját API kulcsodat
BASE_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"


def check_serving_size(fdc_id):
    """Lekérdezi, hogy az USDA API milyen mennyiségre vonatkoztatja az adatokat"""
    url = f"https://api.nal.usda.gov/fdc/v1/food/{fdc_id}"
    params = {"api_key": API_KEY}
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # Ellenőrizzük, hogy van-e adagméret megadva
        serving_size = data.get("servingSize", "Nincs megadva")
        serving_unit = data.get("servingSizeUnit", "N/A")

        print(f"🍽 Adagméret: {serving_size} {serving_unit}")
        print("🔍 Teljes adatstruktúra ellenőrzéshez:")
        print(json.dumps(data, indent=4))
    
    else:
        print(f"❌ Hiba! Státuszkód: {response.status_code}")

# Próbáld ki az adott FDC ID-ra
check_serving_size(2705964)