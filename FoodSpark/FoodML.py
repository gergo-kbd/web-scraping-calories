from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml import pipeline

label_indexer = StringIndexer(inputCol="foodCategory",outputCol= "label")

nutrient_cols =[col for col in df_final.columns if col not in["fdcId", "description", "foodCategory"]]

assembler = VectorAssembler(inputCols=nutrient_cols, outputCol="features")

#pipeline
pipeline = pipeline(stages =[label_indexer, assembler])

df_rdy = pipeline.fit(df_final).transform(df_final)
df_rdy.select("label", "features").show(truncate=False)