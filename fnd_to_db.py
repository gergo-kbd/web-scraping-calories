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

# Normalize the main food data
df_foods = pd.json_normalize(json_data)

# Normalize 

df_nutrients = pd.json_normalize(json_data, record_path='FoundationFoods', meta=['id', 'description'])

df_nutrients = pd.json_normalize(json_data, record_path='foodNutrients', meta=['id', 'description'])
df_portions = pd.json_normalize(json_data, record_path='foodPortions', meta=['id', 'description'])


conn = sqlite3.connect('my_database.db') # Creates the file if it doesn't exist

table_name_foods = 'foods_table'
df_foods.to_sql(table_name_foods, conn, if_exists='replace', index=False)


table_name_nutrients = 'food_nutrients_table'
df_nutrients.to_sql(table_name_nutrients, conn, if_exists='replace', index=False)


table_name_portions = 'food_portions_table'
df_portions.to_sql(table_name_portions, conn, if_exists='replace', index=False)

# Close the connection
conn.close()

print(f"The JSON data from '{file_path}' has been successfully converted to '{table_name_foods}', '{table_name_nutrients}', and '{table_name_portions}' tables in the 'my_database.db' database.")