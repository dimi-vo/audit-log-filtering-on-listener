"""Producer B — sends messages to the broker's secured AUDIT listener (port 9094, SASL/PLAIN)."""

import time
from confluent_kafka import Producer

BROKER = "localhost:9094"
TOPIC = "foobar"


def delivery_report(err, msg):
    if err:
        print(f"Delivery failed: {err}")
    else:
        print(f"Delivered to {msg.topic()} [{msg.partition()}] @ offset {msg.offset()}")


def main():
    producer = Producer(
        {
            "bootstrap.servers": BROKER,
            "client.id": "producer-secured",
            "security.protocol": "SASL_PLAINTEXT",
            "sasl.mechanism": "PLAIN",
            "sasl.username": "randomClient",
            "sasl.password": "the_clients_secret_i_guess",
        }
    )

    print(f"Producing to {TOPIC} via AUDIT listener ({BROKER}) ...")
    try:
        i = 0
        while True:
            value = f"secured-message-{i}"
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
