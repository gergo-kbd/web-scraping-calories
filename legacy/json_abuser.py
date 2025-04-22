import json

# USDA JSON minta (rövidített változat)
json_adat = '''
{
    "foodClass": "Survey",
    "description": "Chicken breast, rotisserie, skin not eaten",
    "foodNutrients": [
        {
            "type": "FoodNutrient",
            "id": 34173859,
            "nutrient": {
                "id": 1003,
                "number": "203",
                "name": "Protein",
                "rank": 600,
                "unitName": "g"
            },
            "amount": 28.0
        },
        {
            "type": "FoodNutrient",
            "id": 34173860,
            "nutrient": {
                "id": 1004,
                "number": "204",
                "name": "Total lipid (fat)",
                "rank": 800,
                "unitName": "g"
            },
            "amount": 3.57
        }
    ]
}
'''
adat = json.loads(json_adat)

print(f"Étel neve: {adat['description']}")
print("\nTápanyagok:")
for nutrient in adat["foodNutrients"]:
    nev = nutrient["nutrient"]["name"]
    mennyiseg = nutrient["amount"]
    egyseg = nutrient["nutrient"]["unitName"]
    print(f"- {nev}: {mennyiseg} {egyseg}")

for nutrient in adat["foodNutrients"]:
    if nutrient["nutrient"]["name"] == "Protein":
        print(f"Protein: {nutrient['amount']} {nutrient['nutrient']['unitName']}")

nutrients_dict = {
    nutrient["nutrient"]["name"]: nutrient
    for nutrient in adat["foodNutrients"]
}

if "Protein" in nutrients_dict:
    protein = nutrients_dict["Protein"]
    print(f"Protein: {protein['amount']} {protein['nutrient']['unitName']}")