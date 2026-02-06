# Running Unit Tests

The Aptos CLI provides commands for running tests, filtering which tests to run, and controlling output verbosity.

## Basic Test Execution

Run all tests in your package:

```sh
aptos move test
```

If your package uses named addresses with `"_"`, use the `--dev` flag to fill them automatically:

```sh
aptos move test --dev
```

Or provide them explicitly:

```sh
aptos move test --named-addresses my_addr=0x1
```

## Filtering Tests

### Run Tests Matching a Name

```sh
aptos move test --filter test_transfer
```

This runs all tests whose names contain `test_transfer`.

### Run Tests in a Specific Module

```sh
aptos move test --filter my_module
```

## Test Output

### Successful Output

```
Running Move unit tests
[ PASS    ] 0x1::counter::test_counter
[ PASS    ] 0x1::counter::test_increment
Test result: OK. Total tests: 2; passed: 2; failed: 0
```

### Failed Output

```
Running Move unit tests
[ FAIL    ] 0x1::counter::test_bad_assertion
  Error: assertion failed
Test result: FAILED. Total tests: 1; passed: 0; failed: 1
```

## Verbose Output

For more detailed output including gas usage:

```sh
aptos move test --dev -v
```

## Debugging with Print

You can print values during tests using `std::debug::print`:

```move
#[test_only]
use std::debug::print;

#[test]
fun test_with_debug() {
    let value = 42;
    print(&value);  // Prints during test execution
    assert!(value == 42);
}
```

Run with verbose output to see the printed values:

```sh
aptos move test --dev -v
```

## Test Gas Limits

By default, tests have a gas budget. If a test exceeds this limit, it will fail. You can increase the limit:

```sh
aptos move test --dev --gas-limit 100000
```

## Common Issues

### "Unresolved named address"

Provide the missing address with `--named-addresses` or use `--dev`.

### "Test exceeded gas limit"

Your test is doing too much computation. Either optimize the test or increase the gas limit.

### Flaky tests

Move tests are deterministic -- if a test passes once, it should always pass. If you see inconsistent results, check for uninitialized state or timing-dependent logic.
