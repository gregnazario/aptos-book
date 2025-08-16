# Error Handling

Errors on Aptos are fairly simple.  Whenever the code aborts, an error message will be returned to the user.  The error message is statically defined by the doc comment above it.  All error codes are u64.  By convention, errors start with E. For example:

```move
/// Uh oh
const E_UH_OH_BAD: u64 = 1;

fun do_something() {
    abort E_UH_OH_BAD
}
```

In this case, the error message when calling `do_something()` wil be `Uh oh`.

More appropriately, errors are usually thrown by asserts.  An example here below shows if you want to ensure a value is less than 10.

```move

/// It's too high!
const E_TOO_HIGH: u64 = 128;

fun check(val: u64) {
    assert!(val < 10, E_TOO_HIGH)
}
```

Additionally, in tests the error code can be omitted for the assertion.
