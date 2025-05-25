from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, size, col
import json
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml import Pipeline
from pyspark.sql import functions as F

#Saprksession starts here
spark = SparkSession.builder.appName("FoodML").getOrCreate()

#read json
usda_fnds_json = spark.read.format('json').option('multiline', 'true').load("FoodData_Central_foundation_food_json_2025-04-24.json")

# checking the schema
#usda_fnds_json.printSchema()

df_foods = usda_fnds_json.select(explode("FoundationFoods").alias("food"))

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
    col("nutrient.nutrient.name").alias("nutrient_name"),
    col("nutrient.amount").alias("nutrient_value"),
    col("nutrient.nutrient.unitName").alias("nutrient_unit")
)

# pivot
df_nutrients_pivot = df_nutrients.groupBy("fdcId", "description")\
    .pivot("nutrient_name")\
    .agg(F.first("nutrient_value"))

df_final = df_nutrients_pivot.fillna(0)

#df_final.show(5)

def sanitize_column_name(name):
    return name.replace(" ", "_") \
               .replace(",", "") \
               .replace("(", "") \
               .replace(")", "") \
               .replace(".", "") \
               .replace("/", "_") \
               .replace("-", "_")

cleaned_cols = [col(f"`{c}`").alias(sanitize_column_name(c)) for c in df_final.columns]
df_final = df_final.select(*cleaned_cols)

label_indexer = StringIndexer(inputCol="description",outputCol= "label")

nutrient_cols =[col for col in df_final.columns if col not in["fdcId", "description"]]

assembler = VectorAssembler(inputCols=nutrient_cols, outputCol="features")

#pipeline
pipeline = Pipeline(stages =[label_indexer, assembler])

df_rdy = pipeline.fit(df_final).transform(df_final)
df_rdy.select("label", "features").show(truncate=False)