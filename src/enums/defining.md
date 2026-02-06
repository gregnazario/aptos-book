# Defining Enums

Enums in Move allow you to define a type that can be one of several variants. Each variant can optionally carry data.

## Basic Enum

The simplest enum is a set of named variants with no associated data:

```move
module my_addr::status {
    enum Status has copy, drop {
        Active,
        Inactive,
        Suspended,
    }
}
```

## Enums with Data

Variants can carry data, similar to structs:

```move
module my_addr::shapes {
    enum Shape has copy, drop {
        Circle { radius: u64 },
        Rectangle { width: u64, height: u64 },
        Triangle { base: u64, height: u64 },
    }
}
```

Each variant can have different fields, making enums far more flexible than simple constants.

## Enums with Positional Fields

Variants can also carry unnamed (positional) data:

```move
module my_addr::result {
    use std::string::String;

    enum Result has copy, drop {
        Ok(u64),
        Err(String),
    }
}
```

## Abilities on Enums

Like structs, enums can have abilities. The rules are the same: an enum can only have an ability if all data in all variants supports that ability.

```move
/// Copyable, droppable enum
enum Color has copy, drop, store {
    Red,
    Green,
    Blue,
    Custom { r: u8, g: u8, b: u8 },
}
```

## Creating Enum Values

You create an enum value by specifying the variant:

```move
fun create_examples() {
    let active = Status::Active;
    let circle = Shape::Circle { radius: 10 };
    let ok = Result::Ok(42);
}
```

## Enum Use Cases in Smart Contracts

### Proposal Status

```move
module my_addr::governance {
    enum ProposalStatus has copy, drop, store {
        Pending,
        Active { votes_for: u64, votes_against: u64 },
        Approved,
        Rejected,
        Executed,
    }

    struct Proposal has key {
        description: vector<u8>,
        status: ProposalStatus,
    }
}
```

### Order Types

```move
module my_addr::exchange {
    enum OrderType has copy, drop, store {
        Market,
        Limit { price: u64 },
        StopLoss { trigger_price: u64 },
    }
}
```

## Best Practices

1. **Use enums for mutually exclusive states**: If a value can only be one of several options, use an enum.
2. **Prefer enums over integer constants**: Enums are type-safe and self-documenting.
3. **Attach data to variants**: If a variant needs additional context, embed it directly rather than using separate fields.
4. **Add abilities thoughtfully**: Only add abilities that all variants can support.
