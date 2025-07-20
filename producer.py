from kafka import KafkaProducer
import time
import json
import os

topic = os.getenv("KAFKA_TOPIC", "test-topic")
bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
interval = float(os.getenv("MESSAGE_INTERVAL", "0.1"))  # seconds

producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

counter = 0
while True:
    message = {"message_number": counter, "content": f"Message {counter}"}
    producer.send(topic, message)
    print(f"Sent: {message}")
    counter += 1
    time.sleep(interval)
