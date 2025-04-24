from OpenFoodApi.OpenFoodQuery import *
from OpenFoodApi.models import *
import json
import requests
from usdaQuery.usda_food_query import *

with open("api_key.txt", "r") as file:
        API_KEY = file.read().strip()

if __name__ == "__main__":
    
    api_client = OpenFoodQuery()

    
    barcode_peanut_noodle_kit = "737628064502"  
    barcode_apenta="5998821515771"

    try:
        food_data_peanut_noodle_kit = api_client.get_product(barcode_peanut_noodle_kit)
        food_apenta = api_client.get_product(barcode_apenta)
    except ProductNotFoundError:
        print("no such barcode")
    except OpenFoodFactsAPIError as e:
        print(f"API error: {e}")

    #print(food_data_peanut_noodle_kit.get('nutriments', {}))
    #print(food_data_peanut_noodle_kit)
    #print(food_apenta.get('nutriments', {}))

    peanut_noodle_kit_info = ProductInfo.from_json(food_data_peanut_noodle_kit)
    apenta_info = ProductInfo.from_json(food_apenta)

    print(peanut_noodle_kit_info)
    print(apenta_info)

    query = UsdaFoodQuery(api_key=API_KEY)
    try:
        foods = query.search_food("banana")
        for food in foods:
            print(food["description"])
            #print(food)
            print(f"{food['description']} (ID: {food['fdcId']})")

    except NoResultsFound as e:
        print("No hit:", e)
    except Exception as e:
        print("Error:", e)
    