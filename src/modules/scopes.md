# Function Scopes

Move provides several visibility levels for functions that control where they can be called from. Choosing the right scope is important for security and API design.

## Visibility Levels

### Private (default)

Functions with no visibility modifier are private. They can only be called from within the same module.

```move
module my_addr::example {
    /// Only callable within this module
    fun internal_calculation(x: u64): u64 {
        x * 2
    }

    public fun public_function(): u64 {
        internal_calculation(21) // OK -- same module
    }
}
```

### Public

`public` functions can be called from any module.

```move
module my_addr::math {
    /// Callable from anywhere
    public fun add(a: u64, b: u64): u64 {
        a + b
    }
}
```

### Public Entry

`entry` functions can be called as standalone transactions from outside the blockchain (e.g., from a wallet or SDK). They can be combined with `public` to also be callable from other modules.

```move
module my_addr::token {
    /// Callable as a transaction AND from other modules
    public entry fun transfer(from: &signer, to: address, amount: u64) {
        // ...
    }

    /// Callable as a transaction ONLY (not from other modules)
    entry fun admin_action(admin: &signer) {
        // ...
    }
}
```

### Public(friend)

`public(friend)` functions are callable only from modules that are declared as friends.

```move
module my_addr::core {
    friend my_addr::helper;

    /// Only callable from my_addr::helper
    public(friend) fun internal_mint(amount: u64) {
        // ...
    }
}

module my_addr::helper {
    use my_addr::core;

    public fun do_mint(amount: u64) {
        core::internal_mint(amount); // OK -- declared as friend
    }
}
```

### Public(package)

`public(package)` functions are callable from any module within the same package but not from external packages.

```move
module my_addr::internal_api {
    /// Callable from any module in this package
    public(package) fun package_only_function(): u64 {
        42
    }
}
```

## View Functions

The `#[view]` attribute marks a function as callable by external read queries without submitting a transaction. View functions should not modify state.

```move
#[view]
public fun get_balance(addr: address): u64 acquires Balance {
    Balance[addr].amount
}
```

## Summary Table

| Modifier | Same Module | Same Package | Friend Module | Any Module | Transaction |
|---|---|---|---|---|---|
| *(private)* | Yes | No | No | No | No |
| `public` | Yes | Yes | Yes | Yes | No |
| `entry` | Yes | No | No | No | Yes |
| `public entry` | Yes | Yes | Yes | Yes | Yes |
| `public(friend)` | Yes | No | Yes | No | No |
| `public(package)` | Yes | Yes | No | No | No |

## Best Practices

1. **Start private**: Make functions private by default and only increase visibility as needed.
2. **Use `entry` for user-facing actions**: Any function a user calls directly should be `entry`.
3. **Use `public` for reusable library functions**: Functions other modules need to call.
4. **Use `public(package)` for internal APIs**: Shared logic within your package that shouldn't be exposed externally.
5. **Use `#[view]` for read operations**: Mark all pure read functions with `#[view]`.
6. **Limit `friend` usage**: Use sparingly -- `public(package)` is usually a better choice.
