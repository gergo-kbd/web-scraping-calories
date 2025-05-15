from pyspark.sql import SparkSession
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
    UsdaFoodjson = query.search_food("egg", page_size=1, data_type=["Survey (FNDDS)","Foundation"])
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


data = spark.read.format('json').option('multiline', 'true').load("usda_hit.json")

data.printSchema()
data.show()


'''
Usda_rdd = spark.sparkContext.parallelize(UsdaFoodjson)
Usda_df = spark.createDataFrame(Usda_rdd)

Usda_df.printSchema()
Usda_df.show()
'''




