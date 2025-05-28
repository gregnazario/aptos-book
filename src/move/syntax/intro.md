# Syntax

## Literals

Move supports the following literal types:
```move
module 0x42::literals {
    // Boolean
    const boolean: bool = true;

    // -- Numbers --
    // Unsigned Integer
    const uint8: u8 = 255;
    const uint8_typed: u8 = 255u8;
    const uint16: u16 = 65535;
    const uint32: u32 = 4294967295;
    const uint64: u64 = 18446744073709551615;

    // -- Addresses --
    // Address using a hex literal
    const address: address = @0x42;
    // Address using a number
    const address_numbered: address = @1;

    // -- U8 Vectors --
    // Hex
    const hex: vector<u8> = x"0123456789abcdef";
    // ASCII String
    const chars: vector<u8> = b"Hello, World!";
    // Vector of numbers
    const numbers: vector<u8> = vector[1, 2, 3, 4, 5];
}
```

## Control flow

```move
module 0x42::control_flow {
    public fun if_example(x: u8): u8 {
        if (x < 10) {
            return x + 1;
        } else {
            return x - 1;
        }
    }

    public fun loop_example(n: u8): u8 {
        let i = 0u8;
        while (i < n) {
            i = i + 1;
        };
        return i;
    }

    public fun for_example(n: u8): u8 {
        let sum = 0u8;
        for (i in 0..n) {
            sum = sum + i;
        };
        return sum;
    }

    enum State {
        Ok
        Err,
    }

    public fun match_example(x: State): u8 {
        match (x) {
            Ok => return 0,
            Err => return 1,
        }
    }
}
```

## Functions

```move
module 0x42::functions {
    /// Public functions can be called from outside the module.
    public fun add(x: u8, y: u8): u8 {
        x + y
    }

    /// Private functions can only be called from within the module. (private by default)
    fun multiply(x: u8, y: u8): u8 {
        x * y
    }

    /// Package functions can be called from within the package, but not from outside.
    package fun square(x: u8): u8 {
        multiply(x, x)
    }

    /// Older syntax for package functions
    public(package) fun cube(x: u8): u8 {
        multiply(square(x), x)
    }

    /// Friend functions can be called from other modules that declare this module as a friend.
    friend fun sum_vector(vec: vector<u8>): u8 {
        let mut sum = 0u8;
        for (i in vec) {
        sum = add(sum, i);
        }
        sum
    }

    /// Older syntax for friend functions
    public(friend) fun do_something_friend(x: u8): u8 {
        // This function can be called by friends of this module.
        x + 1
    }

    /// Entry functions are special functions that can be called from outside the module as a standalone transaction.
    entry fun process_transaction(account: signer, amount: u64) {
        // This function can be called as a transaction.
        let addr = signer::address_of(&account);
        // Process the transaction logic here.
        // For example, transfer `amount` to `addr`.
    }

    /// Entry functions can also be public, friend, or package.  This means they can be called from outside the module 
    /// as a transaction or from within other modules.
    public entry fun example_entry(account: signer) {
        // This is an entry function that can be called as a transaction.
        let addr = signer::address_of(&account);
        // Perform some action with the account address.
    }

    #[test_only]
    /// Test functions are used for testing purposes and can be run in a test environment.
    fun test_addition() {
        let result = add(2, 3);
        assert!(result == 5, 0); // Test passes if result is 5
    }

    #[test_only]
    /// Test functions can also be public, friend, or package.
    public fun test_multiply() {
        let result = multiply(2, 3);
        assert!(result == 6, 0); // Test passes if result is 6
    }
    // TODO: Acquires
    // TODO: Entry function arguments
}
```