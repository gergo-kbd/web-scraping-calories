from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, size, col
import json

#Saprksession starts here
spark = SparkSession.builder.appName("FoodML").getOrCreate()

#read json
usda_fnds_json = spark.read.format('json').option('multiline', 'true').load("FoodData_Central_foundation_food_json_2025-04-24.json")

# checking the schema
#usda_fnds_json.printSchema()

df_foods = usda_fnds_json.select(explode("foods").alias("food"))

# explode nutrients
df_nutrients = df_foods.select(
    "food.fdcId",
    "food.description",
    explode("food.foodNutrients").alias("nutrient")
)

# only nutrient name and value, and dimension is needed
df_nutrients =  df_nutrients.select(
    "fdcId",
    "description",
    "foodCategory",
    col("nutrient.nutrientName").alias("nutrient_name"),
    col("nutrient.value").alias("nutrient_value"),
    col("nutrient.unitName").alias("nutrient_unit")
)

# pivot
df_nutrients_pivot = df_nutrients.groupBy("fdcId", "description", "foodCategory")\
    .pivot("nutrient_name")\
    .agg(F.first("nutrient_value"))

df_final = df_nutrients_pivot.fillna(0)

df_final.show(5)




