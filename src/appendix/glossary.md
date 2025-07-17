# Glossary

A list of all the definitions of different terms used with the Aptos blockchain.

## Abort Code

A numeric identifier that indicates why a program terminated abnormally. Used in Move to signal error conditions and
provide information about what went wrong.

## Aptos CLI

A command line interface to the Aptos blockchain. Used for compiling, testing, verifying, and [publishing](#publish)
Move [packages](#package) to the Aptos blockchain. As well as used for quick prototyping and interaction.

## Attributes

Special annotations in Move code that provide additional information to the compiler or runtime. Examples include
`#[test]`, `#[view]`, `#[event]`, and `#[test_only]`. They modify the behavior or properties of the code they annotate.

## BCS (Binary Canonical Serialization)

A serialization format used in Aptos for encoding data in a deterministic way. BCS ensures that the same data is always
serialized to the same byte representation, which is important for blockchain operations.

## Custom Error Type

A structured error type that provides additional context about the error condition. Used in Move to create more
informative error handling mechanisms beyond simple abort codes.

## Entry Function

A function in Move that can be called directly from outside the module, such as from a transaction. Entry functions are
marked with the `entry` keyword and serve as entry points to a module's functionality.

## Enum

A type in Move that allows for representing different variants or cases. Enums allow for upgradable and different types
in a compact representation, headed by a type identifier followed by the expected type values.

## Error Propagation

The process of passing error information from lower-level functions to higher-level functions. In Move, this is
typically done by having functions abort with specific error codes that can be caught and handled by calling functions.

## Error Range

A range of abort codes reserved for a specific module or functionality. Using error ranges helps avoid conflicts between
modules and organizes error codes in a structured way.

## Error Testing

Testing that functions correctly handle error conditions and abort with appropriate codes. In Move, this is often done
using the `#[expected_failure]` attribute in tests.

## Event

A mechanism used to record changes to the blockchain in an easily indexable way. Events are emitted during transaction
execution and can be subscribed to by off-chain services to track on-chain activities.

## Expected Failure

A testing attribute (`#[expected_failure]`) used in Move to specify that a test is expected to fail with a particular
abort code. This allows for testing error conditions.

## Legacy Shortened Address

A shortened form of an Aptos address that omits leading zeros. For compatibility purposes, these addresses are extended
by filling the missing bytes with zeros.

## Little-endian

A byte order format where the least significant byte is stored at the lowest memory address. In Aptos, numbers in BCS
are stored in little-endian byte order.

## Module

Also known as a Move Module. A single unit of code for a [Move package](#package). Exists in a single file.

## Named Address

An identifier that represents an address in Move source code. Named addresses can be passed in at compile time and
determine where the contract is being deployed.

## Package

Also known as a Move Package. A single deployable unit of code [published](#publish) to the Aptos blockchain. It can
contain multiple [Move modules](#module) inside it. Deployed via the [Aptos CLI](#aptos-cli) with `aptos move publish`.

## Publish

Also known as deploy. Publishing a [Move package](#package) is deploying new code to the blockchain. Can be used with
the [Aptos CLI](#aptos-cli) running with `aptos move publish`.

## Resource

A special kind of struct in Move that represents a value that can be stored in global storage. Resources have the `key`
ability and are stored at specific addresses on the blockchain.

## Storage Slot

A location in the blockchain's state where data can be stored. In Aptos, an address is the 32-byte representation of a
storage slot, which can be used for accounts, objects, and other addressable storage.

## Struct

A composite data type in Move that groups together related values. Structs can have different abilities (copy, drop,
store, key) that determine how they can be used.

## Tuple

A fixed-size collection of values, potentially of different types. In Move, tuples are used in enum variants and
return values to group related values together.

## ULEB128 (Unsigned Little-Endian Base-128)

A variable-length integer encoding used mainly for representing sequence lengths in BCS. It is efficient at storing
small numbers and takes up more space as the number grows.

## View Function

A function in Move that can be called to read data from the blockchain without modifying qstate. View functions are
marked with the `#[view]` attribute and are useful for querying the current state.