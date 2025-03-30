from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg

spark = SparkSession.builder.appName("KafkaMongoDBPipeline").config("spark.mongodb.input.uri", "mongodb://localhost:27017/ecommerce_db.orders").config("spark.mongodb.output.uri", "mongodb://localhost:27017/ecommerce_db.orders").getOrCreate()

df = spark.read.format("mongo").load()
df.createOrReplaceTempView("orders")

avg_price = spark.sql("SELECT product, avg(price) as avg_price FROM orders GROUP BY product")
avg_price.show()
