# Writing Unit Tests

Unit tests in Move are functions annotated with `#[test]`. They live inside your modules and have access to all private functions, making it easy to test internal logic.

## Basic Test

```move
module my_addr::math {
    fun double(x: u64): u64 {
        x * 2
    }

    #[test]
    fun test_double() {
        assert!(double(0) == 0);
        assert!(double(5) == 10);
        assert!(double(100) == 200);
    }
}
```

## Test Annotations

### `#[test]`

Marks a function as a test. The function will be executed when you run `aptos move test`.

```move
#[test]
fun test_basic() {
    assert!(1 + 1 == 2);
}
```

### `#[test]` with Signers

You can create test signers by specifying them in the annotation:

```move
#[test(alice = @0x1, bob = @0x2)]
fun test_with_accounts(alice: &signer, bob: &signer) {
    let alice_addr = std::signer::address_of(alice);
    let bob_addr = std::signer::address_of(bob);
    assert!(alice_addr != bob_addr);
}
```

### `#[expected_failure]`

Tests that should abort can be marked with `#[expected_failure]`:

```move
/// Division by zero should abort
const E_DIVIDE_BY_ZERO: u64 = 1;

fun safe_divide(a: u64, b: u64): u64 {
    assert!(b != 0, E_DIVIDE_BY_ZERO);
    a / b
}

#[test]
#[expected_failure(abort_code = E_DIVIDE_BY_ZERO)]
fun test_divide_by_zero() {
    safe_divide(10, 0);
}
```

You can also specify the location of the abort:

```move
#[test]
#[expected_failure(abort_code = E_DIVIDE_BY_ZERO, location = my_addr::math)]
fun test_divide_by_zero_with_location() {
    safe_divide(10, 0);
}
```

### `#[test_only]`

Marks a function, import, or constant as available only during testing. Test-only code is excluded from production compilation.

```move
#[test_only]
use aptos_framework::account::create_account_for_test;

#[test_only]
fun setup_test_env(account: &signer) {
    create_account_for_test(std::signer::address_of(account));
}
```

## Testing Resources and Global State

When testing functions that interact with global storage, you typically need to set up accounts:

```move
module my_addr::counter {
    use std::signer;

    struct Counter has key {
        value: u64,
    }

    public entry fun create(account: &signer) {
        move_to(account, Counter { value: 0 });
    }

    public entry fun increment(account: &signer) acquires Counter {
        let addr = signer::address_of(account);
        let counter = &mut Counter[addr];
        counter.value = counter.value + 1;
    }

    #[view]
    public fun get_value(addr: address): u64 acquires Counter {
        Counter[addr].value
    }

    #[test(account = @0x1)]
    fun test_counter(account: &signer) acquires Counter {
        let addr = signer::address_of(account);

        create(account);
        assert!(get_value(addr) == 0);

        increment(account);
        assert!(get_value(addr) == 1);

        increment(account);
        assert!(get_value(addr) == 2);
    }

    #[test(account = @0x1)]
    #[expected_failure]
    fun test_increment_without_create(account: &signer) acquires Counter {
        increment(account); // Should fail: no Counter exists
    }
}
```

## Assertions

Move provides the `assert!` macro for testing conditions:

```move
#[test]
fun test_assertions() {
    // Basic equality
    assert!(1 + 1 == 2);

    // With error code (useful for debugging)
    assert!(1 + 1 == 2, 0);

    // Boolean conditions
    assert!(true);
    assert!(!false);

    // Comparison
    assert!(10 > 5);
    assert!(5 < 10);
}
```

## Testing Best Practices

1. **Test the happy path**: Verify that correct inputs produce correct outputs.
2. **Test error cases**: Use `#[expected_failure]` to verify that invalid inputs are properly rejected.
3. **Test edge cases**: Check boundary conditions (zero values, maximum values, empty collections).
4. **Use descriptive test names**: Name tests after what they verify (e.g., `test_transfer_insufficient_balance`).
5. **Set up and tear down**: Use `#[test_only]` helper functions for common setup.
6. **Keep tests focused**: Each test should verify one specific behavior.
