import requests

API_KEY = ""  # place your usda key here  
BASE_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"

def get_nutrition(food_name):
    params = {"api_key": API_KEY, "query": food_name, "pageSize": 1}
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # Ellenőrizzük, hogy van-e találat
        if "foods" in data and len(data["foods"]) > 0:
            food = data["foods"][0]
            nutrients = {nutrient["nutrientName"]: nutrient["value"] for nutrient in food["foodNutrients"]}

            return {
                "food": food_name,
                "calories": nutrients.get("Energy", "N/A"),  # kcal
                "protein": nutrients.get("Protein", "N/A"),  # g
                "fat": nutrients.get("Total lipid (fat)", "N/A"),  # g
                "carbs": nutrients.get("Carbohydrate, by difference", "N/A")  # g
            }
    return None

# Teszt
food_info = get_nutrition("chicken breast")
print(food_info)