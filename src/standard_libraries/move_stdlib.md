# Move Standard Library (MoveStdlib)

The Move Standard Library (`std`) provides the foundational types and utilities used across all Move programs. It is deployed at address `0x1`.

Source: [aptos-framework/move-stdlib](https://github.com/aptos-labs/aptos-framework/tree/main/aptos-move/framework/move-stdlib)

## Key Modules

### `std::string`

UTF-8 encoded strings.

```move
use std::string::{Self, String};

let greeting: String = string::utf8(b"Hello, Aptos!");
let length = string::length(&greeting);
let is_empty = string::is_empty(&greeting);
```

### `std::vector`

Dynamic arrays (see [Collections > Vectors](../collections/vectors.md) for details).

```move
use std::vector;

let v = vector[1, 2, 3];
let len = v.length();
```

### `std::option`

Optional values -- a value that may or may not be present.

```move
use std::option::{Self, Option};

let some_val: Option<u64> = option::some(42);
let none_val: Option<u64> = option::none();
let val = option::extract(&mut some_val); // 42
```

### `std::signer`

Functions for working with transaction signers.

```move
use std::signer;

fun get_addr(account: &signer): address {
    signer::address_of(account)
}
```

### `std::error`

Standard error categories for structured error reporting.

```move
use std::error;

const E_NOT_FOUND: u64 = 1;

fun example() {
    abort error::not_found(E_NOT_FOUND)
}
```

Error categories include: `not_found`, `already_exists`, `permission_denied`, `invalid_argument`, `invalid_state`, `out_of_range`, `resource_exhausted`, and `internal`.

### `std::bcs`

Binary Canonical Serialization (see [BCS chapter](../bcs/intro.md)).

```move
use std::bcs;

let bytes = bcs::to_bytes(&42u64);
```

### `std::hash`

Cryptographic hash functions.

```move
use std::hash;

let data = b"hello";
let hash = hash::sha3_256(data);
```

### `std::debug`

Debugging utilities (test-only).

```move
#[test_only]
use std::debug;

#[test]
fun test_debug() {
    debug::print(&42);
}
```

### `std::fixed_point32` / `std::fixed_point64`

Fixed-point arithmetic for precise financial calculations.

```move
use std::fixed_point32::{Self, FixedPoint32};

let half = fixed_point32::create_from_rational(1, 2);
let result = fixed_point32::multiply_u64(100, half); // 50
```

## Summary

| Module | Purpose |
|---|---|
| `std::string` | UTF-8 strings |
| `std::vector` | Dynamic arrays |
| `std::option` | Optional values |
| `std::signer` | Transaction signer utilities |
| `std::error` | Structured error codes |
| `std::bcs` | Serialization |
| `std::hash` | Cryptographic hashing |
| `std::debug` | Test-time debugging |
| `std::fixed_point32/64` | Fixed-point math |
