from kafka import KafkaConsumer
import pymongo

# Connect to MongoDB
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["ecommerce_db"]
collection = db["orders"]

# Create Kafka Consumer
consumer = KafkaConsumer(
    'ecommerce_orders',
    bootstrap_servers='10.12.46.224:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='ecommerce_group'
)

# Read messages and store in MongoDB
print("📥 Listening for messages...")
for msg in consumer:
    message = msg.value.decode("utf-8")
    print(f"✅ Received: {message}")  # Debugging line
    collection.insert_one({"order": message})
