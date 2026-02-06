# How to Write Tests

Move has a built-in unit testing framework that lets you write tests alongside your smart contract code. Tests are compiled and run by the Move compiler, giving you fast feedback without deploying to a blockchain.

## Why Test?

Smart contracts manage real assets and run in an immutable environment. Bugs can be costly and difficult to fix after deployment. Testing helps you:

- **Catch bugs early** before deployment
- **Verify correctness** of your business logic
- **Document expected behavior** through executable examples
- **Enable safe upgrades** by ensuring backward compatibility

## What You'll Learn

1. **[Writing Unit Tests](writing_unit_tests.md)** - How to define test functions and use assertions
2. **[Running Unit Tests](running_unit_tests.md)** - How to execute tests with the Aptos CLI
3. **[Coverage](coverage.md)** - How to measure test coverage
4. **[Formal Verification](formal_verification.md)** - Using the Move Prover for mathematical guarantees

## Quick Start

Here's a minimal test to give you a sense of the framework:

```move
module my_addr::math {
    public fun add(a: u64, b: u64): u64 {
        a + b
    }

    #[test]
    fun test_add() {
        assert!(add(2, 3) == 5);
        assert!(add(0, 0) == 0);
        assert!(add(100, 200) == 300);
    }
}
```

Run the test with:

```sh
aptos move test --dev
```
