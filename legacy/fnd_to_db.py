import pandas as pd
import sqlite3
import json

# Specify the name of your JSON file
file_path = 'usda_pretty.json'

try:
    # Read the JSON data from the file
    with open(file_path, 'r') as f:
        json_data = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
    exit()
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from the file '{file_path}'. Please ensure it's valid JSON.")
    exit()

print(json_data.keys())
#print(json.dumps(json_data, indent=4, sort_keys=True))  # Formatted print

# Normalize
df_foods = pd.json_normalize(json_data, record_path='FoundationFoods', errors='ignore')
df_nutrients = pd.json_normalize(json_data, record_path=['FoundationFoods', 'foodNutrients'], meta=['description'], errors='ignore')
df_portions = pd.json_normalize(json_data, record_path=['FoundationFoods', 'foodPortions'], meta=['description'], errors='ignore')

print(df_foods.info())

conn = sqlite3.connect('foundation_foods.db') 

# A df_foods DataFrame oszlopainak konvertálása és törlése
for col in df_foods.columns:
    if col in ['description', 'publicationDate', 'foodCategory.description']:
        try:
            df_foods[col] = df_foods[col].astype(str)
        except:
            print(f"Nem sikerült konvertálni a {col} oszlopot a df_foods DataFrame-ben.")
    elif col in ['foodNutrients', 'foodAttributes', 'nutrientConversionFactors', 'foodPortions', 'inputFoods']:
        df_foods = df_foods.drop(columns=[col])

#'foods', 'foodNutrients', 'foodPortions' write to sql table
table_name_foods = 'foods_table'
df_foods.to_sql(table_name_foods, conn, if_exists='replace', index=False)

table_name_nutrients = 'food_nutrients_table'
df_nutrients.to_sql(table_name_nutrients, conn, if_exists='replace', index=False)

table_name_portions = 'food_portions_table'
df_portions.to_sql(table_name_portions, conn, if_exists='replace', index=False)

conn.close()

print(f"'{file_path}' Success json -> sql table creation '{table_name_foods}' '{table_name_nutrients}' '{table_name_portions}' tables have been created -> foundation_food.db .")