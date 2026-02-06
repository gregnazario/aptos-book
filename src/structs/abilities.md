# Structs and Abilities

Abilities are the mechanism Move uses to control what operations can be performed on a type. Every struct must explicitly declare which abilities it has. This chapter explores each ability in detail.

## The Four Abilities

| Ability | What it allows |
|---|---|
| `copy` | The value can be duplicated |
| `drop` | The value can be implicitly destroyed when it goes out of scope |
| `store` | The value can be stored inside another struct in global storage |
| `key` | The value can be stored directly in global storage as a top-level resource |

## `copy` -- Duplicating Values

The `copy` ability allows a value to be duplicated. Without it, assigning a value to a new variable moves it, making the original invalid.

```move
struct Point has copy, drop {
    x: u64,
    y: u64,
}

fun copy_example() {
    let p1 = Point { x: 10, y: 20 };
    let p2 = p1;  // p1 is copied, both p1 and p2 are valid
    let sum = p1.x + p2.x; // Works because Point has copy
}
```

> A struct can only have `copy` if all of its fields also have `copy`.

## `drop` -- Implicit Destruction

The `drop` ability allows a value to be automatically destroyed when it goes out of scope. Without `drop`, every value must be explicitly consumed.

```move
struct TempData has drop {
    value: u64,
}

fun drop_example() {
    let data = TempData { value: 42 };
    // data is implicitly dropped at end of scope -- no error
}
```

Without `drop`, the compiler would require you to destructure or move the value:

```move
struct ImportantData {
    value: u64,
}

fun no_drop_example() {
    let data = ImportantData { value: 42 };
    let ImportantData { value: _ } = data; // Must explicitly destroy
}
```

## `store` -- Nested Storage

The `store` ability allows a value to be stored as a field inside another struct that is in global storage. Without `store`, a type cannot appear inside a resource.

```move
struct Metadata has store, copy, drop {
    name: vector<u8>,
    version: u64,
}

struct Contract has key {
    metadata: Metadata, // Metadata needs `store` to be here
    owner: address,
}
```

## `key` -- Top-Level Storage

The `key` ability allows a struct to be stored directly in global storage under an address. This is what makes a struct a "resource" in the traditional Move sense.

```move
struct Balance has key {
    amount: u64,
}

fun store_balance(account: &signer, amount: u64) {
    move_to(account, Balance { amount });
}
```

> A struct with `key` implicitly requires all its fields to have `store`.

## Common Ability Combinations

### Pure Data (Value Type)

```move
/// Freely copyable and droppable -- behaves like a primitive
struct Config has copy, drop, store {
    max_supply: u64,
    is_active: bool,
}
```

### Storable Asset (Resource)

```move
/// Stored in global storage, cannot be copied or implicitly dropped
struct Token has key, store {
    id: u64,
    value: u64,
}
```

### Temporary Object

```move
/// Can be dropped but not copied or stored
struct Receipt has drop {
    amount: u64,
    timestamp: u64,
}
```

### Hot Potato (No Abilities)

A struct with no abilities at all is called a "hot potato." It must be consumed by some specific function, which is useful for enforcing certain patterns.

```move
/// Must be consumed -- cannot be copied, dropped, or stored
struct FlashLoanReceipt {
    amount: u64,
    fee: u64,
}
```

## Ability Constraints on Fields

A struct's abilities are constrained by its fields:

- A struct can have `copy` only if **all** fields have `copy`.
- A struct can have `drop` only if **all** fields have `drop`.
- A struct can have `store` only if **all** fields have `store`.
- A struct can have `key` only if **all** fields have `store`.

```move
// This would NOT compile because String does not have copy:
// struct BadExample has copy, drop {
//     name: String,  // String does not have copy
// }
```

## Best Practices

1. **Start with minimal abilities**: Only add what you need.
2. **Use `key` for top-level resources**: Structs stored under an address need `key`.
3. **Omit `copy` for assets**: Digital assets should not be copyable.
4. **Omit `drop` for assets that must be tracked**: Prevent accidental loss by omitting `drop`.
5. **Use hot potato pattern for receipts**: When you need to ensure a value is consumed by a specific function.
