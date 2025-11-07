# E-Commerce Real-Time Data Pipeline

This project demonstrates a real-time data pipeline for e-commerce order processing and analytics using Kafka, MongoDB, Spark, and Streamlit.

## Architecture

```
Kafka Producer → Kafka Topic → Kafka Consumer → MongoDB → Spark Analytics → Streamlit Dashboard
```

## Features

- **Simulates e-commerce orders** using a Kafka producer.
- **Streams orders in real-time** via Kafka.
- **Stores orders in MongoDB** using a Kafka consumer.
- **Performs analytics** (e.g., average price per product) using Spark.
- **Visualizes data and analytics** in a live Streamlit dashboard.

## Prerequisites

- Docker & Docker Compose
- Python 3.x

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/E-Commerce-Data-Pipeline.git
cd E-Commerce-Data-Pipeline
```

### 2. Start the services

```bash
docker-compose up -d
```

This will start Kafka, Zookeeper, MongoDB, and Spark (if configured).

### 3. Run the Kafka Producer

```bash
python kafka_producer.py
```

### 4. Run the Kafka Consumer

```bash
python kafka_consumer.py
```

### 5. Run Spark Analytics

```bash
docker exec -it spark spark-submit --packages org.mongodb.spark:mongo-spark-connector_2.12:10.1.1 /home/jovyan/app/pyspark_processing.py
```

### 6. Launch the Streamlit Dashboard

```bash
streamlit run streamlit_dashboard.py
```

Visit [http://localhost:8501](http://localhost:8501) to view the dashboard.

## Data Persistence

MongoDB data is stored inside the Docker container by default.  
To persist data on your host, add a volume to the `mongodb` service in `docker-compose.yml`:

```yaml
volumes:
  - ./mongo-data:/data/db
```

## Customization

- Modify `kafka_producer.py` to change the order simulation logic.
- Add more analytics in `pyspark_processing.py`.
- Enhance the dashboard in `streamlit_dashboard.py`.

## Use Cases

- Real-time order tracking and analytics for e-commerce.
- Scalable architecture for streaming, storage, and analytics.
- Template for IoT, finance, or any event-driven application.

## Troubleshooting

- If MongoDB data disappears after container removal, add a volume as described above.
- For Spark + MongoDB integration, use the `--packages` option to auto-download dependencies.
