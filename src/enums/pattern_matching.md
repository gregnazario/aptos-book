# The `match` Control Flow Construct

The `match` expression lets you compare a value against a series of patterns and execute code based on which pattern matches. It is the primary way to work with enums in Move.

## Basic Match

```move
module my_addr::matcher {
    enum Coin has copy, drop {
        Penny,
        Nickel,
        Dime,
        Quarter,
    }

    fun value_in_cents(coin: Coin): u64 {
        match (coin) {
            Coin::Penny => 1,
            Coin::Nickel => 5,
            Coin::Dime => 10,
            Coin::Quarter => 25,
        }
    }
}
```

## Matching with Data

When a variant carries data, you can bind the data to variables in the pattern:

```move
enum Shape has copy, drop {
    Circle { radius: u64 },
    Rectangle { width: u64, height: u64 },
}

fun area(shape: Shape): u64 {
    match (shape) {
        Shape::Circle { radius } => {
            // Approximate: 3 * r^2
            3 * radius * radius
        },
        Shape::Rectangle { width, height } => {
            width * height
        },
    }
}
```

## Matching Positional Variants

```move
enum Result has copy, drop {
    Ok(u64),
    Err(u64),
}

fun unwrap_or_default(result: Result): u64 {
    match (result) {
        Result::Ok(value) => value,
        Result::Err(_) => 0,
    }
}
```

## Exhaustiveness

The Move compiler requires that `match` expressions are **exhaustive** -- every possible variant must be handled. This prevents bugs where a case is accidentally forgotten.

```move
// This would NOT compile -- missing Coin::Quarter:
// fun broken(coin: Coin): u64 {
//     match (coin) {
//         Coin::Penny => 1,
//         Coin::Nickel => 5,
//         Coin::Dime => 10,
//     }
// }
```

## Multi-Line Match Arms

Match arms can contain multiple statements within braces:

```move
fun describe(shape: Shape): vector<u8> {
    match (shape) {
        Shape::Circle { radius } => {
            if (radius > 100) {
                b"large circle"
            } else {
                b"small circle"
            }
        },
        Shape::Rectangle { width, height } => {
            if (width == height) {
                b"square"
            } else {
                b"rectangle"
            }
        },
    }
}
```

## Match and References

You can match on references to avoid consuming the value:

```move
fun is_circle(shape: &Shape): bool {
    match (shape) {
        Shape::Circle { .. } => true,
        _ => false,
    }
}
```

## Practical Example: State Machine

Enums and match are ideal for implementing state machines in smart contracts:

```move
module my_addr::auction {
    use std::signer;

    enum AuctionState has copy, drop, store {
        Open { highest_bid: u64, highest_bidder: address },
        Closed,
        Settled { winner: address, amount: u64 },
    }

    struct Auction has key {
        state: AuctionState,
        seller: address,
    }

    public fun process_bid(auction: &mut Auction, bidder: address, amount: u64) {
        auction.state = match (auction.state) {
            AuctionState::Open { highest_bid, highest_bidder } => {
                if (amount > highest_bid) {
                    AuctionState::Open {
                        highest_bid: amount,
                        highest_bidder: bidder,
                    }
                } else {
                    AuctionState::Open { highest_bid, highest_bidder }
                }
            },
            AuctionState::Closed => abort 1,  // Cannot bid on closed auction
            AuctionState::Settled { .. } => abort 2,  // Already settled
        };
    }
}
```

## Best Practices

1. **Always handle all variants**: The compiler enforces this, which prevents missing-case bugs.
2. **Use `_` for unused bindings**: If you don't need a value, use `_` to ignore it.
3. **Keep match arms simple**: If a match arm is complex, extract the logic into a separate function.
4. **Use enums for state machines**: The combination of enums and match naturally models state transitions.
