"""Consumer — reads audit-log messages from the allowed-topic-produce audit topic and prints them."""

import json
from confluent_kafka import Consumer, KafkaException

BROKER = "localhost:29092"
TOPIC = "confluent-audit-log-events-default-allowed"

LISTENER_ICONS = {
    "PLAIN": "🔓",
    "AUDIT": "🔐",
}


def format_event(event: dict) -> str:
    data = event.get("data", {})
    listener = data.get("requestMetadata", {}).get("request_listener_name", "UNKNOWN")
    icon = LISTENER_ICONS.get(listener, "❓")

    client_id = data.get("request", {}).get("client_id", "n/a")
    principal = data.get("authenticationInfo", {}).get("principal", "n/a")
    timestamp = event.get("time", "n/a")
    subject = event.get("subject", "n/a")
    method = data.get("methodName", "n/a")

    return (
        f"{icon} [{listener}]  client_id={client_id}  principal={principal}\n"
        f"   🕐 {timestamp}\n"
        f"   📌 {subject}\n"
        f"   📋 {method}"
    )


def main():
    consumer = Consumer(
        {
            "bootstrap.servers": BROKER,
            "group.id": "audit-log-consumer",
            "client.id": "consumer-audit",
            "auto.offset.reset": "earliest",
        }
    )

    consumer.subscribe([TOPIC])
    print(f"Consuming from {TOPIC} ...\n")

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())

            value = msg.value().decode("utf-8")
            try:
                event = json.loads(value)
                print(format_event(event))
            except json.JSONDecodeError:
                print(value)
            print()
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
        print("Consumer stopped.")


if __name__ == "__main__":
    main()
