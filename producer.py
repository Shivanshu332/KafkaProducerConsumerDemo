import logging
from logging.handlers import RotatingFileHandler
from kafka import KafkaProducer
import time, json, os

topic = os.getenv("KAFKA_TOPIC", "test-topic")
bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
interval = float(os.getenv("MESSAGE_INTERVAL", "0.1"))
log_dir = os.getenv("LOG_DIR", "/logs")

os.makedirs(log_dir, exist_ok=True)
handler = RotatingFileHandler(
    os.path.join(log_dir, "producer.log"),
    maxBytes=1024*1024, 
    backupCount=5
)
logging.basicConfig(handlers=[handler], level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger()

producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

counter = 0
while True:
    msg = {"message_number": counter, "content": f"Message {counter}"}
    producer.send(topic, msg)
    logger.info(f"Sent: {msg}")
    counter += 1
    time.sleep(interval)