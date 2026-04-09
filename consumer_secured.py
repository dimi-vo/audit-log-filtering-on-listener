"""Consumer B — reads messages from the foobar topic via the secured AUDIT listener (port 9094, SASL/PLAIN)."""

from confluent_kafka import Consumer, KafkaException

BROKER = "localhost:9094"
TOPIC = "foobar"


def main():
    consumer = Consumer(
        {
            "bootstrap.servers": BROKER,
            "group.id": "consumer-secured-group",
            "client.id": "consumer-secured",
            "auto.offset.reset": "earliest",
            "security.protocol": "SASL_PLAINTEXT",
            "sasl.mechanism": "PLAIN",
            "sasl.username": "randomClient",
            "sasl.password": "the_clients_secret_i_guess",
        }
    )

    consumer.subscribe([TOPIC])
    print(f"Consuming from {TOPIC} via AUDIT listener ({BROKER}) ...")

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
