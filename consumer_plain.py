"""Consumer A — reads messages from the foobar topic via the unsecured PLAIN listener (port 29092)."""

from confluent_kafka import Consumer, KafkaException

BROKER = "localhost:29092"
TOPIC = "foobar"


def main():
    consumer = Consumer(
        {
            "bootstrap.servers": BROKER,
            "group.id": "consumer-plain-group",
            "client.id": "consumer-plain",
            "auto.offset.reset": "earliest",
        }
    )

    consumer.subscribe([TOPIC])
    print(f"Consuming from {TOPIC} via PLAIN listener ({BROKER}) ...")

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            print(msg.value().decode("utf-8"))
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
        print("Consumer stopped.")


if __name__ == "__main__":
    main()
