# Indexing Events

Once events are emitted on-chain, they need to be consumed by off-chain services. This is done through **indexing** -- the process of reading events from the blockchain and storing them in a queryable database.

## How Events Are Stored

When a transaction emits events, they are included in the transaction output and stored on the blockchain. Each event contains:

- The event type (the fully qualified struct name)
- The event data (the serialized struct fields)
- The sequence number (order within the transaction)

## Querying Events

### Using the Aptos REST API

You can query events through the Aptos Node API:

```
GET /v1/accounts/{address}/events/{event_handle}/{field_name}
```

For module events (the modern `#[event]` style), you can query by event type:

```
GET /v1/events?event_type={module_address}::{module_name}::{EventStructName}
```

### Using the Aptos Indexer

The Aptos Indexer provides a GraphQL API for more complex event queries:

```graphql
query GetTransferEvents {
  events(
    where: {
      type: { _eq: "0x1::coin::WithdrawEvent" }
    }
    order_by: { transaction_version: desc }
    limit: 10
  ) {
    type
    data
    transaction_version
    event_index
  }
}
```

### Using the TypeScript SDK

The Aptos TypeScript SDK provides methods for querying events:

```typescript
import { Aptos, AptosConfig, Network } from "@aptos-labs/ts-sdk";

const config = new AptosConfig({ network: Network.MAINNET });
const aptos = new Aptos(config);

const events = await aptos.getModuleEventsByEventType({
  eventType: "0x1::coin::WithdrawEvent",
});
```

## Building an Indexer

For production applications, you typically run a custom indexer that:

1. **Streams** transactions from an Aptos fullnode.
2. **Filters** for events relevant to your application.
3. **Processes** the event data and stores it in a database.
4. **Serves** the indexed data through an API.

The Aptos Indexer framework provides tools for building custom processors:

- **Transaction Stream Service**: Streams raw transaction data.
- **Custom Processors**: Parse and index specific event types.
- **PostgreSQL Storage**: Store indexed data for querying.

## Best Practices

1. **Design events for indexing**: Include all data that off-chain services will need.
2. **Use consistent event naming**: Make event types easy to filter and query.
3. **Index critical events**: Ensure all important state changes are indexed.
4. **Handle reorgs**: Your indexer should handle chain reorganizations gracefully.
5. **Monitor indexer health**: Set up alerts for indexing lag or failures.
