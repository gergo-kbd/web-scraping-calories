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
         