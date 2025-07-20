# Kafka Log Rotation Test Suite (Producer & Consumer)

This project deploys a Kafka producer and consumer written in Python to Kubernetes via Helm. It includes:
- Kafka via Bitnami Helm chart
- Python apps that log to files with log rotation
- Persistent storage for logs using PVC
- Fluent Bit sidecar for log tailing/shipping

---

## 🛠️ Prerequisites

- Docker installed
- Kubernetes cluster (e.g., Minikube, kind, GKE, etc.)
- Helm 3+
- `kubectl` configured
- Docker Hub or another container registry

---

## 📦 1. Clone the Project

```bash
git clone https://github.com/your-org/kafka-log-rotation-demo.git
cd kafka-log-rotation-demo




docker build -t yourdockerhubuser/kafka-file-log:latest .
docker build -t kafkaproducerconsumer .


docker login
docker push yourdockerhubuser/kafka-file-log:latest



kubectl exec -it deployment/kafka-producer -- ls /logs
kubectl exec -it deployment/kafka-consumer -- ls /logs

helm install kafka-file-log ./kafka-file-log-chart \
  --set kafka.bootstrapServers="localhost:9092" \
  --set producer.interval=1 \
  --set image.command="{python, -c, 'import time, logging; logging.basicConfig(filename=\"/logs/test.log\", level=logging.INFO); i=0; [logging.info(f\"log {i}\") or time.sleep(1) or (i:=i+1) for _ in range(100)]'}"


kubectl logs <producer-pod> -c fluentbit
kubectl logs <consumer-pod> -c fluentbit


helm uninstall kafka
helm uninstall kafka-file-log
kubectl delete pvc kafka-file-log-pvc


The producer and consumer log every message to /logs/producer.log or /logs/consumer.log

Python's RotatingFileHandler rotates logs at 1MB with 5 backups

Fluent Bit tails all *.log* files to ensure rotated logs are shipped too