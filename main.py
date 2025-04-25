from OpenFoodApi.OpenFoodQuery import *
from OpenFoodApi.models import *
import json
import requests
from usdaQuery.usda_food_query import *
from usdaQuery.models import *

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

    #############################################################################################################

    query = UsdaFoodQuery(api_key=API_KEY)
    try:
        banana_query = query.search_food("banana, raw", page_size = 3, data_type=["Survey (FNDDS)","Foundation"])
    except NoResultsFound as e:
        print(e)
    except Exception as e:
        print("Error:", e)

    #print(banana_query)

    for food in banana_query.get('foods', []):  
        print(food.get('description', 'Description not found'))
        print(f"{food.get('description', 'Description not found')} (ID: {food.get('fdcId', 'ID not found')})")

    banana_food_item = FoodItem.from_dict(banana_query['foods'])

    for item in banana_food_item:
        print(f"\nFood name: {item.description}")
        print("nutrients:")
        for nutrient_name, nutrient in item.nutrients.items():
            print(f"  {nutrient.name}: {nutrient.amount} {nutrient.unit}")
    '''
    parsed_banana_info = FoodItem.from_dict(banana_query)
    print(parsed_banana_info.description)
    print(parsed_banana_info.fdc_id)
    print(parsed_banana_info.data_type)
    print(parsed_banana_info.nutrients['Protein'].amount)

'''