import streamlit as st
import pymongo
import pandas as pd

# Connect to MongoDB
mongo_client = pymongo.MongoClient("mongodb://172.17.0.4:27017/")
db = mongo_client["ecommerce_db"]
collection = db["orders"]

# Fetch latest data from MongoDB
data = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB’s default "_id" field
df = pd.DataFrame(data)

# Streamlit UI
st.title("📊 E-Commerce Orders Dashboard")
st.write("### 🔍 Real-time Orders from Kafka & MongoDB")

if not df.empty:
    st.dataframe(df)
    st.bar_chart(df["order"].value_counts())
else:
    st.warning("⚠️ No data found! Run the producer to generate messages.")

# import streamlit as st
# from kafka import KafkaConsumer

# # Kafka Configuration
# KAFKA_BROKER = "10.12.46.224:9092"  # Change this if needed
# TOPIC_NAME = "ecommerce_orders"

# # Create Kafka Consumer
# consumer = KafkaConsumer(
#     TOPIC_NAME,
#     bootstrap_servers=KAFKA_BROKER,
#     auto_offset_reset="latest",  # Read new messages
#     enable_auto_commit=True,
#     group_id="streamlit_group"
# )

# # Streamlit UI
# st.title("📊 Live Kafka Orders Dashboard")
# st.write("🔄 **Streaming live orders from Kafka...**")

# # Stream messages dynamically
# messages = []
# for msg in consumer:
#     message = msg.value.decode("utf-8")
#     messages.append(message)
    
#     # Display the last 10 messages only
#     st.write("✅ **New Order:**", message)
#     if len(messages) > 10:
#         messages.pop(0)
