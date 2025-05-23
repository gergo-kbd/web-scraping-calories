import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from OpenFoodApi.OpenFoodQuery import *
from usdaQuery.usda_food_query import *

backend_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(backend_dir)
api_key_path = os.path.join(project_root, "api_key.txt")

try:
    with open(api_key_path, "r") as file:
        API_KEY = file.read().strip()
except FileNotFoundError:
    print("APIKEY cannot be found.")
except Exception as e:
    print("ERROR occured during file read.")

query = UsdaFoodQuery(api_key=API_KEY)

try:
    UsdaFoodjson = query.search_food("egg", page_size=2, data_type=["Survey (FNDDS)","Foundation"])
except NoResultsFound as e:
    print(e)
except Exception as e:
    print("ERROR", e)

foods_data = UsdaFoodjson.get('foods')

food_df = pd.DataFrame(foods_data)

print(food_df['foodNutrients'].head())

#print(food_df['foodNutrients'].iloc[0])

for index, row in food_df.iterrows():
    for nutrient in row['foodNutrients']:
        if nutrient['nutrientName'] == 'Protein':
            print(f"{row['description']}: {nutrient['value']} {nutrient['unitName']}")

food_df.plot

plt.show()

#plt.savefig(sys.stdout.buffer)
#sys.stdout.flush()


