# Enums and Pattern Matching

Enums (enumerations) allow you to define a type by listing its possible variants. While a struct groups related fields together, an enum says "this value is one of these possible things." Combined with pattern matching via `match`, enums enable expressive and safe handling of multiple states.

## Why Enums?

In smart contract development, you frequently encounter situations where a value can be one of several distinct types:

- A transaction result is either a success or a failure.
- A game character's state is idle, moving, attacking, or defeated.
- A proposal's status is pending, approved, or rejected.

Enums make these states explicit and let the compiler verify that you handle every possible case.

## What You'll Learn

1. **[Defining Enums](defining.md)** - How to declare enums with and without data
2. **[The `match` Control Flow Construct](pattern_matching.md)** - How to branch on enum variants
