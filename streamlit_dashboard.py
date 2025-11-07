import streamlit as st
import pymongo
import pandas as pd
import matplotlib.pyplot as plt
from pyspark.sql import SparkSession

# Connect to MongoDB with timeout
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
db = mongo_client["ecommerce_db"]
collection = db["orders"]

# Test MongoDB connection
try:
    mongo_client.admin.command('ping')
    st.success("✅ Connected to MongoDB")
except Exception as e:
    st.error(f"❌ MongoDB connection failed: {e}")
    st.stop()

# Fetch latest data from MongoDB
data = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB's default "_id" field

# Streamlit UI
st.title("📊 E-Commerce Orders Dashboard")
st.write("### 🔍 Real-time Orders from Kafka & MongoDB")

if data:
    df = pd.DataFrame(data)
    
    # Show the data
    st.write(f"**Total Orders: {len(df)}**")
    st.dataframe(df)
    
    # Create charts based on actual columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Orders by Product")
        st.bar_chart(df["product"].value_counts())
    
    with col2:
        st.write("### Orders by User")
        st.bar_chart(df["user"].value_counts())
    
    # Show price statistics
    st.write("### Price Statistics")
    st.write(f"Average Price: ${df['price'].mean():.2f}")
    st.write(f"Min Price: ${df['price'].min():.2f}")
    st.write(f"Max Price: ${df['price'].max():.2f}")
    
    # Price histogram
    st.write("### Price Distribution")
    fig, ax = plt.subplots()
    ax.hist(df["price"], bins=20, color='skyblue', edgecolor='black')
    ax.set_xlabel("Price")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)
    
    # Spark analytics: Average price per product
    st.write("### Spark: Average Price per Product")
    spark = SparkSession.builder \
        .appName("KafkaMongoDBPipeline") \
        .config("spark.mongodb.input.uri", "mongodb://localhost:27017/ecommerce_db.orders") \
        .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.1.1") \
        .getOrCreate()
    spark_df = spark.read.format("mongo").load()
    spark_df.createOrReplaceTempView("orders")
    avg_price = spark.sql("SELECT product, avg(price) as avg_price FROM orders GROUP BY product")
    avg_price_pd = avg_price.toPandas()
    st.dataframe(avg_price_pd)
    spark.stop()

else:
    st.warning("⚠️ No data found! Make sure your producer and consumer are running.")

# Add refresh button
if st.button("🔄 Refresh Data"):
    st.rerun()
