# Glossary

This glossary defines key terms used throughout the Aptos documentation.

---

## Abort Code
A numeric identifier indicating why a program terminated abnormally. In Move, it signals specific error conditions.

## Aptos CLI
The command-line interface for the Aptos blockchain. It is used for compiling, testing, deploying, and interacting with Move packages.

## Attributes
Special annotations in Move code, like `#[test]` or `#[view]`, that provide metadata to the compiler or runtime, modifying the behavior of the annotated code.

## BCS (Binary Canonical Serialization)
The deterministic serialization format used in Aptos. BCS ensures that data structures always serialize to the same byte representation, which is crucial for blockchain consensus.

## Custom Error Type
A user-defined struct that provides detailed context for an error, offering a more informative alternative to simple abort codes.

## Entry Function
A public function in a Move module, marked with the `entry` keyword, that can be directly invoked in a transaction.

## Enum
A type that can hold one of several defined variants. Enums are useful for representing states or options in a type-safe way.

## Error Propagation
The process where an error (abort) in one function causes its calling functions to also abort, passing the error up the call stack.

## Error Range
A designated range of abort codes for a specific module to prevent conflicts and organize error handling.

## Error Testing
The practice of writing tests to verify that functions fail as expected under error conditions, often using the `#[expected_failure]` attribute.

## Event
A mechanism for Move contracts to emit data that can be indexed and queried by off-chain services, signaling that something of interest has occurred.

## Expected Failure
A test attribute (`#[expected_failure]`) that asserts a test case should fail with a specific abort code, enabling robust error-handling tests.

## Legacy Shortened Address
A condensed form of an Aptos address where leading zeros are omitted. These are automatically padded with zeros for compatibility.

## Little-endian
A byte-ordering scheme where the least significant byte is stored first. Aptos uses little-endian byte order for BCS serialization.

## Module
A single file containing Move code (`.move`), which acts as a fundamental unit of code organization and encapsulation within a package.

## Named Address
An alias for a specific account address used in Move source code. The actual address is substituted during compilation, making code more portable.

## Package
A deployable unit of Move code that can contain one or more modules. It is published to the Aptos blockchain as a single entity.

## Publish
The act of deploying a Move package to the Aptos blockchain, making its code and resources available on-chain.

## Resource
A special struct with the `key` ability that represents data stored in an account's global storage. Resources have ownership semantics and cannot be copied or discarded.

## Storage Slot
A location in the blockchain's global state, identified by a 32-byte address, where data (like accounts or objects) can be stored.

## Struct
A composite data type that groups related values into a single, named structure. Its behavior is defined by its abilities (`copy`, `drop`, `store`, `key`).

## Tuple
A fixed-size, ordered collection of values that can have different types.

## ULEB128 (Unsigned Little-Endian Base-128)
A variable-length encoding for unsigned integers used in BCS, primarily for representing the length of sequences efficiently.

## View Function
A read-only function marked with the `#[view]` attribute. It can be called to query blockchain state without submitting a transaction and incurring gas fees for state changes.