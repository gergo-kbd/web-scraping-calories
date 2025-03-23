import requests
import json

API_KEY = "C2hbBSIucd88eskFFJphpWYc30JmA6Tv45Rn421I"  # Itt add meg a saját API kulcsodat
BASE_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"

def get_food_id(query):
    """Lekéri az első találat FDC ID-ját az USDA API-ból"""
    params = {
        "api_key": API_KEY,
        "query": query,
        "pageSize": 1,  # Csak az első találat kell
        "dataType": ["Foundation", "Survey (FNDDS)"]
    }
    
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("foods"):
            first_food = data["foods"][0]
            return first_food.get("fdcId")
    return None

# Próbáld ki csirkemellre
fdc_id = get_food_id("Chicken breast")
print(f"🔎 FDC ID: {fdc_id}")

def get_food_nutrients(fdc_id):
    """Lekérdezi az adott FDC ID-hoz tartozó makrókat"""
    if not fdc_id:
        print("❌ Nincs FDC ID, nem lehet lekérdezni a tápértékeket.")
        return None

    url = f"https://api.nal.usda.gov/fdc/v1/food/{fdc_id}"
    params = {"api_key": API_KEY}
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # Az új JSON struktúrához igazított keresés
        nutrients = {n["nutrient"]["name"]: n["amount"] for n in data.get("foodNutrients", [])}

        return {
            "calories": nutrients.get("Energy", "N/A"),
            "protein": nutrients.get("Protein", "N/A"),
            "fat": nutrients.get("Total lipid (fat)", "N/A"),
            "carbs": nutrients.get("Carbohydrate, by difference", "N/A")
        }
    else:
        print(f"❌ Hiba! Státuszkód: {response.status_code}")
        return None

# Próbáld ki az előzőleg kapott FDC ID-val
nutrients = get_food_nutrients(fdc_id)
print(nutrients)

