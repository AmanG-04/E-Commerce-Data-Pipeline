from pyspark.sql import SparkSession

# Create Spark session - it will auto-download all MongoDB dependencies
spark = SparkSession.builder \
    .appName("KafkaMongoDBPipeline") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.1.1") \
    .config("spark.mongodb.read.connection.uri", "mongodb://mongodb:27017/ecommerce_db.orders") \
    .getOrCreate()

# Read data from MongoDB
df = spark.read \
    .format("mongodb") \
    .option("database", "ecommerce_db") \
    .option("collection", "orders") \
    .load()

# Show schema and sample data
print("=== Data from MongoDB ===")
df.printSchema()
df.show()

# Perform analytics: Average price per product
print("=== Average Price per Product ===")
df.createOrReplaceTempView("orders")
avg_price = spark.sql("SELECT product, AVG(price) as avg_price FROM orders GROUP BY product ORDER BY avg_price DESC")
avg_price.show()

# Additional analytics
print("=== Total Orders per User ===")
user_orders = spark.sql("SELECT user, COUNT(*) as order_count FROM orders GROUP BY user ORDER BY order_count DESC")
user_orders.show()

# Stop Spark session
spark.stop()
