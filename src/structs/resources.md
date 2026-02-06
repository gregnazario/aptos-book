# Structs and How They Become Resources

One of the most powerful concepts in Move is the idea of a **resource** -- a struct whose usage is tightly controlled by the type system to prevent duplication or accidental loss. Resources are the foundation of safe digital asset management on Aptos.

## What is a Resource?

A resource is any struct that has the `key` ability but lacks the `copy` ability. Because a resource cannot be copied, it can only exist in one place at a time, which makes it ideal for representing assets like tokens, NFTs, or game items.

```move
module my_addr::vault {
    /// A vault that holds a balance. Because it has `key` but not `copy`,
    /// it is a resource -- it cannot be duplicated.
    struct Vault has key {
        balance: u64,
    }
}
```

## Resources vs. Regular Structs

| Property | Regular Struct (`copy + drop`) | Resource (`key`, no `copy`) |
|---|---|---|
| Can be copied | Yes | No |
| Can be implicitly dropped | Yes (with `drop`) | No |
| Stored in global storage | Only with `key` | Yes |
| Ideal for | Temporary data, config | Assets, tokens, game items |

## Creating Resources

Resources are created like any other struct, but they must be explicitly stored or returned -- they cannot simply go out of scope.

```move
module my_addr::vault {
    use std::signer;

    struct Vault has key {
        balance: u64,
    }

    /// Create a vault and store it under the caller's account
    public entry fun create_vault(account: &signer, initial_balance: u64) {
        let vault = Vault { balance: initial_balance };
        move_to(account, vault);
    }
}
```

## Global Storage Operations

Move provides four built-in operations for working with resources in global storage:

### `move_to` -- Store a resource

Stores a resource under a signer's address. Each account can hold at most one instance of a given resource type.

```move
move_to(account, Vault { balance: 100 });
```

### `move_from` -- Remove a resource

Removes and returns a resource from global storage. This transfers ownership back to the caller.

```move
let vault = move_from<Vault>(addr);
```

### `borrow_global` -- Immutable reference

Borrows an immutable reference to a resource in global storage.

```move
let vault_ref = borrow_global<Vault>(addr);
let balance = vault_ref.balance;
```

### `borrow_global_mut` -- Mutable reference

Borrows a mutable reference to a resource in global storage.

```move
let vault_mut = borrow_global_mut<Vault>(addr);
vault_mut.balance = vault_mut.balance + 100;
```

> **Note:** The newer indexing syntax `Vault[addr]` is equivalent to `borrow_global<Vault>(addr)` and `&mut Vault[addr]` is equivalent to `borrow_global_mut<Vault>(addr)`.

### `exists` -- Check existence

Checks whether a resource exists at a given address.

```move
if (exists<Vault>(addr)) {
    // The vault exists
};
```

## The `acquires` Annotation

Any function that accesses global storage for a resource type must declare this with the `acquires` keyword:

```move
#[view]
public fun get_balance(addr: address): u64 acquires Vault {
    Vault[addr].balance
}

public entry fun deposit(account: &signer, amount: u64) acquires Vault {
    let addr = signer::address_of(account);
    let vault = &mut Vault[addr];
    vault.balance = vault.balance + amount;
}
```

## Destroying Resources

Because resources cannot be implicitly dropped, you must explicitly destroy them through destructuring:

```move
public entry fun close_vault(account: &signer) acquires Vault {
    let addr = signer::address_of(account);
    let Vault { balance: _ } = move_from<Vault>(addr);
}
```

## Why Resources Matter

Resources solve a fundamental problem in blockchain programming: preventing the duplication or loss of digital assets.

- **No duplication**: Because resources cannot be copied, a token cannot be "double-spent" at the language level.
- **No accidental loss**: Because resources without `drop` cannot be silently discarded, assets cannot be accidentally lost.
- **Explicit lifecycle**: Every resource must be explicitly created, stored, transferred, or destroyed.

This is what makes Move uniquely safe for financial applications compared to languages like Solidity, where asset safety relies on developer discipline rather than compiler enforcement.
