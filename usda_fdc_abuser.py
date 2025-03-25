import requests
import json

API_KEY = "C2hbBSIucd88eskFFJphpWYc30JmA6Tv45Rn421I"  # here you add your own API key
BASE_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"

def get_food_id(query):
    """Query the first result's FDC id from USDA API """
    params = {
        "api_key": API_KEY,
        "query": query,
        "pageSize": 1,  # only need the first result
        "dataType": ["Foundation", "Survey (FNDDS)"]
    }
    
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("foods"):
            first_food = data["foods"][0]
            return first_food.get("fdcId")
    return None

# Try it for chicken breast
fdc_id = get_food_id("Chicken breast")
print(f"🔎 FDC ID: {fdc_id}")

def get_food_nutrients(fdc_id):
    """Query nutrition data to the corresponding FDC id """
    if not fdc_id:
        print("❌ No FDC ID, cant get nutrition data.")
        return None

    url = f"https://api.nal.usda.gov/fdc/v1/food/{fdc_id}"
    params = {"api_key": API_KEY}
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # tweaked to json format
        nutrients = {n["nutrient"]["name"]: n["amount"] for n in data.get("foodNutrients", [])}

        return {
            "calories": nutrients.get("Energy", "N/A"),
            "protein": nutrients.get("Protein", "N/A"),
            "fat": nutrients.get("Total lipid (fat)", "N/A"),
            "carbs": nutrients.get("Carbohydrate, by difference", "N/A")
        }
    else:
        print(f"❌ Error! Status: {response.status_code}")
        return None

# print the data behind the fdc id
nutrients = get_food_nutrients(fdc_id)
print(nutrients)

