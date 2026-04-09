"""Producer A — sends messages to the broker's unsecured PLAIN listener (port 29092)."""

import time
from confluent_kafka import Producer

BROKER = "localhost:29092"
TOPIC = "foobar"


def delivery_report(err, msg):
    if err:
        print(f"Delivery failed: {err}")
    else:
        print(f"Delivered to {msg.topic()} [{msg.partition()}] @ offset {msg.offset()}")


def main():
    producer = Producer({"bootstrap.servers": BROKER, "client.id": "producer-plain"})

    print(f"Producing to {TOPIC} via PLAIN listener ({BROKER}) ...")
    try:
        i = 0
        while True:
            value = f"plain-message-{i}"
            producer.produce(TOPIC, value=value, callback=delivery_report)
            producer.poll(0)
            i += 1
            time.sleep(2)
    except KeyboardInterrupt:
        pass
    finally:
        producer.flush()
        print("Producer stopped.")


if __name__ == "__main__":
    main()
