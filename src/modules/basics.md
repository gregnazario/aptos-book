# Module Basics

A module is the fundamental organizational unit in Move. It groups related types, functions, and constants together and is published at a specific blockchain address.

## Defining a Module

```move
module my_addr::greeting {
    use std::string::String;

    /// A greeting resource
    struct Greeting has key {
        message: String,
    }

    /// Store a greeting
    public entry fun set_greeting(account: &signer, msg: String) {
        move_to(account, Greeting { message: msg });
    }

    /// Read a greeting
    #[view]
    public fun get_greeting(addr: address): String acquires Greeting {
        Greeting[addr].message
    }
}
```

The module declaration has two parts:
- **`my_addr`** is a named address that is resolved at compile time.
- **`greeting`** is the module name, which must be unique within the address.

## Module Contents

A module can contain:

### Constants

```move
module my_addr::config {
    /// Maximum allowed value
    const MAX_VALUE: u64 = 1000;

    /// Error: value exceeds maximum
    const E_VALUE_TOO_HIGH: u64 = 1;
}
```

### Structs and Enums

```move
module my_addr::types {
    struct Point has copy, drop, store {
        x: u64,
        y: u64,
    }

    enum Direction has copy, drop {
        North,
        South,
        East,
        West,
    }
}
```

### Functions

```move
module my_addr::math {
    public fun add(a: u64, b: u64): u64 {
        a + b
    }

    fun internal_helper(x: u64): u64 {
        x * 2
    }
}
```

## Named Addresses

Named addresses are placeholders that are resolved at compile or deploy time. They are defined in the `Move.toml` file:

```toml
[addresses]
my_addr = "_"  # Will be filled at deploy time
```

Or set explicitly:

```toml
[addresses]
my_addr = "0x1234abcd"
```

When deploying with the Aptos CLI, you provide the address mapping:

```sh
aptos move publish --named-addresses my_addr=default
```

## Module Naming Conventions

- Module names use **snake_case**: `my_module`, `token_factory`.
- Struct and enum names use **PascalCase**: `UserProfile`, `OrderType`.
- Function names use **snake_case**: `create_account`, `get_balance`.
- Constants use **UPPER_SNAKE_CASE**: `MAX_SUPPLY`, `E_NOT_FOUND`.
- Error constants begin with **`E_`** or **`E`**: `E_INSUFFICIENT_BALANCE`.

## One Module Per Purpose

A best practice is to keep each module focused on a single responsibility:

```
sources/
├── token.move        # Token struct and logic
├── marketplace.move  # Marketplace for trading tokens
├── governance.move   # Voting and proposals
└── config.move       # Shared configuration
```

This makes your code easier to read, test, and upgrade.
