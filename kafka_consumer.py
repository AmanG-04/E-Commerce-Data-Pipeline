from kafka import KafkaConsumer
import json
from pymongo import MongoClient

# Add connection timeout and retry settings
consumer = KafkaConsumer(
    'ecommerce_orders',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    group_id='ecommerce_group',
    auto_offset_reset='earliest',  # Start from beginning
    enable_auto_commit=True,
    api_version=(0, 10, 1),        # Specify API version
)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['ecommerce_db']
collection = db['orders']

print("Consumer started, waiting for messages...")

try:
    for message in consumer:
        order = message.value
        collection.insert_one(order)
        print(f"Consumed and stored order: {order}")
except Exception as e:
    print(f"Error: {e}")
finally:
    consumer.close()
