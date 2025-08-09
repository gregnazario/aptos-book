# Example Program Using Enums

```move
module examples::orders {
    enum OrderStatus has copy, drop {
        Open,
        Filled { qty: u64 },
        Cancelled,
    }

    public fun process(status: OrderStatus): u64 {
        match status {
            OrderStatus::Open => 0,
            OrderStatus::Filled { qty } => qty,
            OrderStatus::Cancelled => 0,
        }
    }
}
```

Adding a new variant to `OrderStatus` later will cause the `match` in `process` to stop compiling until the new case is handled, making this pattern helpful for safely upgrading modules.
