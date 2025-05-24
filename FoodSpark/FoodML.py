from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, size, col
import json
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml import pipeline

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

#df_final.show(5)

label_indexer = StringIndexer(inputCol="foodCategory",outputCol= "label")

nutrient_cols =[col for col in df_final.columns if col not in["fdcId", "description", "foodCategory"]]

assembler = VectorAssembler(inputCols=nutrient_cols, outputCol="features")

#pipeline
pipeline = pipeline(stages =[label_indexer, assembler])

df_rdy = pipeline.fit(df_final).transform(df_final)
df_rdy.select("label", "features").show(truncate=False)