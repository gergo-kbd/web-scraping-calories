'''
from usdaQuery.usda_food_query import *

with open("api_key.txt", "r") as file:
        API_KEY = file.read().strip()

if __name__ == "__main__":
    query = UsdaFoodQuery(api_key=API_KEY)

    try:
        foods = query.search_food("banana")
        for food in foods:
            #print(food["description"])
            print(f"{food['description']} (ID: {food['fdcId']})")

    except NoResultsFound as e:
        print("⚠️ No hit:", e)

    except Exception as e:
        print("💥 Error:", e)

        '''


from OpenFoodApi.OpenFoodQuery import OpenFoodQuery
import json
import requests

def get_search_result_count(search_term):
    url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={search_term}&search_simple=1&action=process&json=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("count", 0)  # Visszaadja a találatok számát
    else:
        return f"Hiba: {response.status_code}"


if __name__ == "__main__":
    
    api_client = OpenFoodQuery(language="en")
    
    # Példa: Termék keresése vonalkód alapján
    print("Példa: Termék keresése vonalkód alapján...")
    barcode = "737628064502"  # Helyettesítsd egy valós vonalkóddal
    product = api_client.get_product(barcode)
    if product:
        print(json.dumps(product, indent=2))  # Szép nyomtatás JSON formátumban
    else:
        print(f"Nem található termék ezzel a vonalkóddal: {barcode}")

    # Példa: Keresés terméknév alapján
    print("\nPélda: Keresés terméknév alapján...")
    search_term = "chocolate"  # Helyettesítsd a saját keresőkifejezéseddel
    results = api_client.search_products(search_term)
    if results.get("products"):
        for product in results["products"][:5]:  # Csak az első 5 találatot mutatjuk
            print(f"Név: {product.get('product_name')}")
            print(f"Márka: {product.get('brands')}")
            print(f"Kiszerelés: {product.get('quantity')}")
            print(f"Kép: {product.get('image_front_small_url')}")
            print("-" * 20)
    else:
        print(f"Nincs találat a következő keresőkifejezésre: {search_term}")
    
    search_term = "chocolate"
    result_count = get_search_result_count(search_term)
    print(f"Találatok száma: {result_count}")
    

'''
from OpenFoodApi.OpenFoodQuery import OpenFoodQuery
import json
import requests
import logging

if __name__ == "__main__":
    off_api = OpenFoodQuery(language="en")

    try:
        search_results = off_api.search_products(
            search_term="chocolate",
            sort_by="popularity",
            tagtype_0="allergens",
            tag_contains_0="en:milk"
        )
        print("--- Nyers API válasz ---")
        print(json.dumps(search_results, indent=4))

        print("\n--- Bővített keresési eredmények (csokoládé, tejallergiamentes, népszerűség szerint rendezve) ---")
        for product in search_results.get("products", []):
            print(f"  - {product.get('product_name', 'N/A')} ({product.get('brands', 'N/A')})")

    except OpenFoodFactsAPIError as e:
        logging.error(f"Hiba a keresés során (OpenFoodFactsAPIError): {e}")
        print(f"Hiba történt (OpenFoodFactsAPIError): {e}")
    except Exception as e:
        logging.error(f"Hiba a keresés során: {e}")
        print(f"Hiba történt: {e}")

'''