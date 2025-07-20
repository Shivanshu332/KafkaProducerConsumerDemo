FROM python:3.10-slim

RUN pip install kafka-python

WORKDIR /app
COPY producer.py consumer.py ./

ENTRYPOINT ["python"]
CMD ["producer.py"]