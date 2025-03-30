import requests
import json

API_KEY = ""  # place your usda key here
BASE_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"


def get_general_food_names(query, results=10):
    """Lekérdezi az USDA API-ból az általános (nem márkázott) élelmiszerek neveit."""
    params = {
        "api_key": API_KEY,
        "query": query,
        "pageSize": results,
        "dataType": ["Foundation", "Survey (FNDDS)"]  # Csak általános élelmiszerek
    }
    
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return [food.get("description", "N/A") for food in data.get("foods", [])]
    else:
        print(f"❌ Hiba! Státuszkód: {response.status_code}")
        return []

# Próbáld ki csirkére
food_list = get_general_food_names("chicken breast", 5)
print(food_list)