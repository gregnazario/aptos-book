# Event Emission

Events are the primary mechanism for making contract state changes observable to off-chain services like indexers, wallets, and dApps. Well-designed events make your contract easy to integrate with.

## The Event Pattern

### Define the Event

Events are structs with the `#[event]` attribute and the `drop` and `store` abilities:

```move
module my_addr::marketplace {
    use aptos_framework::event;

    #[event]
    struct ItemListed has drop, store {
        seller: address,
        item_id: u64,
        price: u64,
    }

    #[event]
    struct ItemSold has drop, store {
        seller: address,
        buyer: address,
        item_id: u64,
        price: u64,
    }
}
```

### Emit the Event

Use `event::emit` to emit events during function execution:

```move
public entry fun list_item(
    seller: &signer,
    item_id: u64,
    price: u64,
) {
    let seller_addr = signer::address_of(seller);

    // Business logic...

    event::emit(ItemListed {
        seller: seller_addr,
        item_id,
        price,
    });
}

public entry fun buy_item(
    buyer: &signer,
    seller_addr: address,
    item_id: u64,
) {
    let buyer_addr = signer::address_of(buyer);
    let price = get_item_price(seller_addr, item_id);

    // Transfer logic...

    event::emit(ItemSold {
        seller: seller_addr,
        buyer: buyer_addr,
        item_id,
        price,
    });
}
```

## What to Include in Events

Good events contain enough information for off-chain consumers to understand what happened:

- **Who**: The addresses of the parties involved.
- **What**: The specific action that occurred.
- **Details**: Relevant data like amounts, IDs, and timestamps.

```move
#[event]
struct Transfer has drop, store {
    from: address,
    to: address,
    amount: u64,
}
```

## Event Design Guidelines

1. **One event per significant action**: Emit an event for every state change that external observers might care about.
2. **Include all relevant data**: Don't force indexers to make additional API calls to reconstruct what happened.
3. **Use descriptive names**: Event struct names should clearly describe the action (e.g., `TokenMinted`, `OrderFilled`).
4. **Keep events small**: Don't include large data structures -- include IDs and references instead.
5. **Be consistent**: Use consistent naming and field ordering across all events in your module.

## Testing Events

You can verify event emission in tests:

```move
#[test(seller = @0x1)]
fun test_list_emits_event(seller: &signer) {
    list_item(seller, 1, 100);
    // The event is emitted during execution
    // Indexers will pick it up from the transaction output
}
```

## Best Practices

1. **Always emit events for entry functions**: Any user-facing action should emit an event.
2. **Don't emit events for view functions**: View functions don't change state.
3. **Use module events (not handle events)**: The `#[event]` attribute with `event::emit` is the modern approach.
4. **Document your events**: Include doc comments on event structs so consumers know what each field means.
