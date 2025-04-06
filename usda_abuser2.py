import requests
import json

with open("api_key.txt", "r") as file:
    api_key = file.read().strip()


BASE_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"


def get_general_food_names(query, results=10):
    """Lekérdezi az USDA API-ból az általános (nem márkázott) élelmiszerek neveit."""
    params = {
        "api_key": api_key,
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
