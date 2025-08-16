# Generic Types

## Overview

Generics are similar to other languages, which allow for a function to specify implementation for multiple input types, output types or struct inner types.

Here is a simple example of a parameterized input type:

```move
/// Take a generic type `T` and use it as an input type
fun print<T>(input: &T) {
    std::debug::print(input)
}
```

Similarly can be used to define outputs:

```move
fun from_string<T>(input: &String): T {
    // Implementation
}
```

Structs and enums can also have generics in them.  Here is an example making a wrapper:

```move
struct Box<T> {
  inner: T
}
```

We can see in this example, the `Box` wraps the inner value.  This can be used similarly in Enums or in combination with other values.

> Note that if a generic is provided in a struct, it will always need to be provided.

## Type Constraints

When considering generics, it's important to remember that, it can be any type, and that some consideration has to be made for the differences.

For example, in the previous example, there were no abilities on the types.  If you try to drop those types in the function, it will fail to compile, as the input can't be dropped.  Here's an example:

```move
fun print<T>(input: T) {
  // ... This will fail with a compilation error
}
```

But, if we add the drop constraint, only inputs of type T that can be dropped will be allowed.  Which provides type safety like so:

```move
fun print<T: drop>(input: T) {
  // ... This will succeed
}
```

> Note that, multiple properties can be added with `+` like:

```move
fun print<T: copy + drop>(input: T) {
  // ... This will succeed
}
```

## Phantom Generics

The `phantom` keyword works just like in Rust.  It is only used for type checking, but not used for an underlying type.  This is useful if you want types that don't conflict, but are essentially the same.  Here's an example using `Coin`.

```move
struct Coin<phantom T> {
  amount: u64
}
```

The `phantom` keyword is used, because the `T` value is used for domain separation, that is that each type of coin is different.  But, it is not used directly in the struct's inner values.

## Tradeoffs and considerations

### Generics as Inputs

Since all types that the constraints apply to, this can be tricky to use when providing into entry functions.

For example if I have a function that takes in a generic and converts it to a single type, we will need to manage all possible types, including primitives to be passed in.

```
struct Storage {
  bytes: vector<u8>
}

entry fun store_type_as_bytes<T: copy + drop>(caller: &signer) {
  // Convert to bytes
  let bytes: vector<u8> = //...

  move_to(caller, Storage {
    bytes
  })
}
```

Callers will also have to know which input types are supported, and it would be best to have abort messages explaining that it doesn't support the type.

#### Example

A perfect example of this is the original Coin standard on Aptos.  By using a generic, the caller needs to pass in the coin types.  However, the contract will not know all possible types, and cannot store them in the contract.

### Generics as Outputs

Using a generic as an output has the same considerations as an input.  It can be tricky to properly support different types together in a clean way.
