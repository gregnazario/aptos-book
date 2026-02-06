# Aptos Standard Library (AptosStdlib)

The Aptos Standard Library (`aptos_std`) extends the Move Standard Library with data structures and utilities specific to the Aptos blockchain. It is deployed at address `0x1`.

Source: [aptos-framework/aptos-stdlib](https://github.com/aptos-labs/aptos-framework/tree/main/aptos-move/framework/aptos-stdlib)

## Key Modules

### Data Structures

#### `aptos_std::smart_table`

A scalable hash table designed for large datasets. Entries are stored in separate storage slots for parallelism.

```move
use aptos_std::smart_table::{Self, SmartTable};

let table = smart_table::new<address, u64>();
smart_table::add(&mut table, @0x1, 100);
let value = smart_table::borrow(&table, @0x1);
```

#### `aptos_std::smart_vector`

A vector that automatically splits into a table when it grows beyond a threshold.

```move
use aptos_std::smart_vector::{Self, SmartVector};

let sv = smart_vector::new<u64>();
smart_vector::push_back(&mut sv, 42);
```

#### `aptos_std::simple_map`

A simple key-value map backed by a vector. Best for small collections.

```move
use aptos_std::simple_map::{Self, SimpleMap};

let map = simple_map::new<String, u64>();
simple_map::add(&mut map, key, value);
```

#### `aptos_std::table`

A hash-based key-value store where each entry occupies its own storage slot.

```move
use aptos_std::table::{Self, Table};

let t = table::new<address, u64>();
table::add(&mut t, @0x1, 100);
```

### Cryptography

#### `aptos_std::ed25519`

Ed25519 signature verification.

#### `aptos_std::multi_ed25519`

Multi-signature Ed25519 verification.

#### `aptos_std::secp256k1`

Secp256k1 elliptic curve operations (compatible with Ethereum keys).

### Utilities

#### `aptos_std::type_info`

Get runtime type information for generic types.

```move
use aptos_std::type_info;

fun get_type_name<T>(): String {
    type_info::type_name<T>()
}
```

#### `aptos_std::math64` / `aptos_std::math128`

Common math operations like `min`, `max`, `pow`, and `sqrt`.

```move
use aptos_std::math64;

let max_val = math64::max(10, 20); // 20
let min_val = math64::min(10, 20); // 10
```

#### `aptos_std::comparator`

Generic comparison utilities for ordering values.

#### `aptos_std::string_utils`

Extended string formatting and manipulation.

```move
use aptos_std::string_utils;

let formatted = string_utils::to_string(&42u64);
```

## Summary

| Module | Purpose |
|---|---|
| `smart_table` | Scalable hash table |
| `smart_vector` | Auto-scaling vector |
| `simple_map` | Small key-value map |
| `table` | Large key-value store |
| `ed25519` | Ed25519 signatures |
| `type_info` | Runtime type info |
| `math64/128` | Math utilities |
| `string_utils` | String formatting |
| `comparator` | Value comparison |
