FROM python:3.11-slim

WORKDIR /app

COPY producer.py .

RUN pip install kafka-python prometheus_client

EXPOSE 8000  

CMD ["python", "producer.py"]
