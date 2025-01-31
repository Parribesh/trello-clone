from kafka import KafkaProducer
import json

# KafkaProducer setup
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8'),
    # Ensures that the message is acknowledged by all replicas (strongest guarantee)
    acks='all',
    retries=5,   # Retry up to 5 times in case of errors
    batch_size=16384,  # Adjust batch size based on your message load
    linger_ms=10  # Delay before sending a batch (in milliseconds)
)

# Function to send messages


def send_message(topic, message):
    producer.send(topic, value=message)
    # Optional: You can wait for confirmation that the message was sent
    producer.flush()


if __name__ == "__main__":
    # Example usage
    task_update = {"project_id": "1234",
                   "task": "Complete", "stage": "In Progress"}
    send_message("task-stage-changes", task_update)
