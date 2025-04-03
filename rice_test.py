import requests
import json

api_key = "" # Ide ird be az API kulcsodat
search_term = "rice"
api_url = f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={api_key}&query={search_term}"

response = requests.get(api_url)

'''if response.status_code == 200:
    data = response.json()
    # Itt feldolgozhatod az adatokat
    for food in data['foods']:
        print(food['description'])
        # Itt kinyerheted a tápértékadatokat
else:
    print(f"Hiba történt: {response.status_code}")'''

print("ITT VALASSZAD EL!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

search_term = "rice"
api_url = f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={api_key}&query={search_term}"

response = requests.get(api_url)


if response.status_code == 200:
    data = response.json()
    foods = data.get('foods', [])  # Ellenőrizzük, hogy a 'foods' kulcs létezik-e

    if foods:
        for i in range(min(6, len(foods))):  # Legfeljebb az első 6 találatig iterálunk
            food = foods[i]
            food_class = food.get('foodClass')
            print(f"Találat {i + 1}: foodClass = {food_class}")
    else:
        print("Nincsenek találatok.")
else:
    print(f"Hiba történt: {response.status_code}")


fields = "description"  # Csak ezeket a mezőket kérdezzük le


api_url = f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={api_key}&query={search_term}&fields={fields}"

response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()
    with open("response.json", "w") as f:
        json.dump(data, f, indent=4) #JSON formázott fájlba írás
    print("A válasz a response.json fájlba lett mentve.")
else:
    print(f"Hiba történt: {response.status_code}")


if response.status_code == 200:
    data = response.json()
    if data['foods']:
        for food in data['foods']:
            print(f"Leírás: {food.get('description')}")
            print(f"Food Class: {food.get('foodClass')}")
            # egyéb adatok kinyerése
    else:
        print("Nincsenek találatok.")
else:
    print(f"Hiba történt: {response.status_code}")