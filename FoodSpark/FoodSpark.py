from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, size
import json
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
    UsdaFoodjson = query.search_food("banana", page_size=5, data_type=["Survey (FNDDS)","Foundation"])
except NoResultsFound as e:
    print(e)
except Exception as e:
    print("ERROR", e)

file_path = "usda_hit.json"
try:
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(UsdaFoodjson, f, ensure_ascii=False, indent=4)
except IOError as e:
    print(f"error occured during saving json: {e}")


spark = SparkSession.builder.appName("FoodSpark").getOrCreate()

df_json = spark.read.format('json').option('multiline', 'true').load("usda_hit.json")

#df_json.select(size("foods").alias("num_foods")).show()

df_foods = df_json.select(explode("foods").alias("food"))

#df_foods.select("food.fdcId", "food.description").show(truncate=False)

df_nutrients_flat = df_foods.select(
    "food.fdcId",
    "food.description",
    explode("food.foodNutrients").alias("nutrient")
)

df_nutrients_flat.show(150)


#df_nutrients_flat.write.csv("nutrients.csv", header=True)
'''
df_nutrients_flat.write.csv("nutrients.csv", header=True)

df_nutrients_flat.write.parquet("nutrients.parquet")

df_nutrients_flat.createOrReplaceTempView("nutrients")
spark.sql("SELECT * FROM nutrients WHERE nutrientName = 'Protein'").show()
'''




