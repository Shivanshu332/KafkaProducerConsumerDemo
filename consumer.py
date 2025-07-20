import logging
from logging.handlers import RotatingFileHandler
from kafka import KafkaConsumer
import json, os, time

topic = os.getenv("KAFKA_TOPIC", "test-topic")
bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
log_dir = os.getenv("LOG_DIR", "/logs")

os.makedirs(log_dir, exist_ok=True)
handler = RotatingFileHandler(
    os.path.join(log_dir, "consumer.log"),
    maxBytes=1024*1024,
    backupCount=5
)
logging.basicConfig(handlers=[handler], level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger()

consumer = KafkaConsumer(
    topic,
    bootstrap_servers=bootstrap_servers,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    key_deserializer=lambda k: k.decode(),
    value_deserializer=lambda v: json.loads(v.decode())
)

while True:
    for rec in consumer.poll(timeout_ms=1000).values():
        for msg in rec:
            logger.info(f"Received: {msg.key} -> {msg.value}")
    time.sleep(0.1)