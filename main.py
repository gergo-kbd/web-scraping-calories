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

    # This is the line that's causing the issue
    banana_item = FoodItem.from_dict(banana_query)

    print("--- A banana_query['foods'] első 3 eleme  ---")
    if 'foods' in banana_query:
        for i, food in enumerate(banana_query['foods']):
            if i < 3:
                print(f"Elem {i+1}: {food.get('description')}, ID: {food.get('fdcId')}")
            else:
                break
    else:
        print("'foods' kulcs nem található a banana_query-ban")
    print("---")

    print("--- A banana_item lista hossza ---")
    print(len(banana_item))
    print("---")

    '''

    if banana_item:
        print("--- A banana_item lista első elemének típusa ---")
        print(type(banana_item[0]))
        print("--- A banana_item lista első elemének adatai ---")
        print(f"ID: {getattr(banana_item[0], 'fdc_id', 'Nincs ID')}")
        print(f"Leírás: {getattr(banana_item[0], 'description', 'Nincs leírás')}")
        print("---")
    else:
        print("--- A banana_item lista üres ---")



    parsed_banana_info = FoodItem.from_dict(banana_query)
    print(parsed_banana_info.description)
    print(parsed_banana_info.fdc_id)
    print(parsed_banana_info.data_type)
    print(parsed_banana_info.nutrients['Protein'].amount)


for item in banana_item:
        print(f"Food: {item.description} (ID: {item.fdc_id})")
    for nutrient_name, nutrient in item.nutrients.items():
        print(f"  - {nutrient_name}: {nutrient.amount} {nutrient.unit}")

    print("--- Printing each banana item with its nutrients ---")
    for item in banana_item:
        print("---")
        print(f"Food: {item.description} (ID: {item.fdc_id})")
        print("Nutrients:")
        for nutrient_name, nutrient in item.nutrients.items():
            print(f"  - {nutrient_name}: {nutrient.amount} {nutrient.unit}")
        print("---")
'''