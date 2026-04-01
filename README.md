# Kafka Audit Logs Demo

Demonstrates how to use Confluent audit logs to identify which client IDs interact with the cluster through a specific listener.

The broker exposes two client-facing listeners:

| Listener | Port  | Auth        | Purpose                        |
|----------|-------|-------------|--------------------------------|
| PLAIN    | 29092 | None        | Unauthenticated (detect usage) |
| AUDIT    | 9094  | SASL/PLAIN  | Authenticated                  |

Audit log routing is configured to capture all produce/consume events on user topics into dedicated audit log topics (internal and audit topics are excluded to reduce noise).

## Setup

The audit log routing config lives in `security-event-router-config.json`. To update it:

```sh
cat security-event-router-config.json | jq -c .
```

Paste the output into `KAFKA_CONFLUENT_SECURITY_EVENT_ROUTER_CONFIG` in `compose.yaml`.

## Run the Demo

```sh
# Start the cluster
docker compose up -d

# Create a test topic
kafka-topics --bootstrap-server localhost:29092 --create --topic foobar

# Start watching the audit log for produce events
kafka-console-consumer --bootstrap-server localhost:29092 \
  --topic confluent-audit-log-events-allowed-topic-produce \
  --from-beginning

# In another terminal — produce via the PLAIN listener (no auth)
kafka-console-producer --bootstrap-server localhost:29092 --topic foobar

# In another terminal — produce via the AUDIT listener (authenticated)
kafka-console-producer --bootstrap-server localhost:9094 --topic foobar \
  --producer.config client.properties
```

## Reading the Audit Logs

Each audit log event is a JSON object. The key fields to look at:

- `data.authenticationInfo.principal` — the client identity (e.g. `User:ANONYMOUS` for unauthenticated, `User:randomClient` for authenticated)
- `data.methodName` — the operation (e.g. `kafka.Produce`)
- `data.resourceName` — the topic being accessed
- `data.serviceName` — the listener used (e.g. `crn:///kafka=.../listener=PLAIN` or `listener=AUDIT`)

Unauthenticated clients show up as `User:ANONYMOUS` — these are the ones using the PLAIN listener without SASL credentials.
