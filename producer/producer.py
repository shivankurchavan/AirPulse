from kafka import KafkaProducer
from prometheus_client import start_http_server, Counter, Gauge
import time
import json
import random
import threading

# Define Prometheus metrics
produced_messages = Counter('producer_messages_total', 'Total messages produced')
failed_messages = Counter('producer_messages_failed', 'Failed messages to Kafka')
messages_per_second = Gauge('producer_messages_per_second', 'Messages sent per second')

# Start Prometheus metrics server
start_http_server(8000)  # Metrics available at :8000/metrics

producer = KafkaProducer(
    bootstrap_servers='broker:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_messages():
    """Send messages at a random rate between 50 and 1000 per second."""
    while True:
        # Select a random rate between 150 and 500 messages per second
        rate_per_second = random.randint(150, 500)
        interval = 1.0 / rate_per_second
        # Run for 10 seconds before changing the rate
        rate_change_time = time.time() + 5
        while time.time() < rate_change_time:
            start_time = time.time()
            for _ in range(rate_per_second):
                try:
                    msg = {
                        'event': 'test',
                        'timestamp': time.time(),
                        'value': random.uniform(0, 100)
                    }
                    producer.send('transactions', msg)
                    produced_messages.inc()
                    print(f"Produced: {msg}")
                except Exception as e:
                    failed_messages.inc()
                    print(f"Failed to send message: {e}")
                time.sleep(interval)
            # Update messages per second metric
            messages_per_second.set(rate_per_second)
            print(f"Set messages_per_second to {rate_per_second}")  # Debug print
            # Sleep to maintain approximate rate
            elapsed = time.time() - start_time
            if elapsed < 1:
                time.sleep(1 - elapsed)

# Start producer in a separate thread
producer_thread = threading.Thread(target=send_messages)
producer_thread.daemon = True
producer_thread.start()

# Keep the main thread running
try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    print("Shutting down producer")