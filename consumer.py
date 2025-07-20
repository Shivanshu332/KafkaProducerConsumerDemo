from kafka import KafkaConsumer
import json
import os

topic = os.getenv("KAFKA_TOPIC", "test-topic")
bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

consumer = KafkaConsumer(
    topic,
    bootstrap_servers=bootstrap_servers,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

for msg in consumer:
    print(f"Received: {msg.value}")
