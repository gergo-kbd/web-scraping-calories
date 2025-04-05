import requests
import json


with open("api_key.txt", "r") as file:
    api_key = file.read().strip()


search_term = "rice, raw"  # Példa keresési kifejezés
api_url = f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={api_key}&query={search_term}&dataType=Foundation"

response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()
    if data['foods']:
        for food in data['foods']:
            if food.get('dataType') == 'Foundation': # only foundation
                print(json.dumps(food, indent=4)) #Teljes food adat kiírása.
                # Itt kinyerheted a tápértékadatokat
                break #Megtaláltuk a foundatiot, nincs értelme tovább iterálni.
    else:
        print("Nincsenek találatok.")
else:
    print(f"Hiba történt: {response.status_code}")


if response.status_code == 200:
    data = response.json()
    with open("response.json", "w") as f:
        json.dump(data, f, indent=4) #JSON formázott fájlba írás
    print("A válasz a response.json fájlba lett mentve.")
else:
    print(f"Hiba történt: {response.status_code}")




