from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

products = ["Laptop", "Smartphone", "Headphones", "Keyboard", "Mouse"]
users = ["User1", "User2", "User3", "User4", "User5"]

while True:
    order = {
        "user": random.choice(users),
        "product": random.choice(products),
        "price": round(random.uniform(10, 1000), 2),
        "timestamp": time.time()
    }
    
    producer.send('ecommerce_orders', order)
    print(f"Produced Order: {order}")
    
    time.sleep(2)  # Simulates real-time order streaming
