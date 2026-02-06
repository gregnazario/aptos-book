# Module Imports

Move uses the `use` keyword to import modules, types, and functions from other modules. This lets you reference external code without writing out full paths every time.

## Basic Imports

### Importing a Module

```move
module my_addr::example {
    use std::string;

    fun create_greeting(): string::String {
        string::utf8(b"Hello, Aptos!")
    }
}
```

### Importing a Specific Type

```move
module my_addr::example {
    use std::string::String;

    fun create_greeting(): String {
        std::string::utf8(b"Hello, Aptos!")
    }
}
```

### Importing Both Module and Type

Use `Self` to import the module itself alongside specific types:

```move
module my_addr::example {
    use std::string::{Self, String};

    fun create_greeting(): String {
        string::utf8(b"Hello, Aptos!")
    }
}
```

This is the most common pattern -- it gives you access to both the `String` type directly and the module's functions via `string::`.

## Multiple Imports

### From the Same Module

```move
use std::vector::{Self, empty, push_back, length};
```

### From Different Modules

```move
use std::string::{Self, String};
use std::signer;
use std::vector;
use aptos_framework::event;
use aptos_framework::account;
```

## Standard Library Addresses

Aptos has three standard library addresses:

| Address | Name | Description |
|---|---|---|
| `std` (0x1) | Move Standard Library | Basic types, vectors, strings, options |
| `aptos_std` (0x1) | Aptos Standard Library | Extended utilities, crypto, data structures |
| `aptos_framework` (0x1) | Aptos Framework | Accounts, coins, objects, governance |

Common imports:

```move
// From Move Stdlib
use std::string::{Self, String};
use std::vector;
use std::option::{Self, Option};
use std::signer;
use std::error;

// From Aptos Stdlib
use aptos_std::table::{Self, Table};
use aptos_std::smart_table::{Self, SmartTable};

// From Aptos Framework
use aptos_framework::event;
use aptos_framework::object::{Self, Object};
use aptos_framework::fungible_asset::{Self, FungibleAsset};
use aptos_framework::primary_fungible_store;
```

## Aliasing Imports

You can rename imports with `as`:

```move
use std::string::String as Str;
use aptos_framework::fungible_asset as fa;
```

## Where to Place Imports

Imports are placed at the top of the module body, before any definitions:

```move
module my_addr::example {
    // Imports first
    use std::string::{Self, String};
    use std::signer;
    use aptos_framework::event;

    // Then constants, structs, and functions
    const E_NOT_FOUND: u64 = 1;

    struct MyStruct has key {
        name: String,
    }

    public fun my_function() { }
}
```

## Test-Only Imports

Use `#[test_only]` to import modules that are only needed in tests:

```move
#[test_only]
use std::debug::print;

#[test_only]
use aptos_framework::account::create_account_for_test;
```

## Best Practices

1. **Import what you use**: Don't import modules you don't reference.
2. **Use `Self` pattern**: Import both the module and its key types with `use module::{Self, Type}`.
3. **Group imports logically**: Group std, aptos_std, aptos_framework, and your own modules.
4. **Prefer specific imports**: Import specific types rather than using full paths throughout.
