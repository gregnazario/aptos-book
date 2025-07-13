# Functions

Functions are the building blocks of Move programs. They allow you to encapsulate logic, reuse code, and create modular, maintainable programs. Move provides several types of functions with different visibility levels and purposes.

## Function Types and Visibility

### Public Functions

Public functions can be called from outside the module.

```move
module my_module::functions {
    /// Public functions can be called from outside the module.
    public fun add(x: u64, y: u64): u64 {
        x + y
    }

    /// Public functions can also be entry functions.
    public entry fun public_entry(account: &signer, value: u64) {
        let addr = signer::address_of(account);
        // Process the transaction
    }
}
```

### Private Functions

Private functions can only be called from within the same module. Functions are private by default.

```move
module my_module::private_functions {
    /// Private functions can only be called from within the module.
    fun multiply(x: u64, y: u64): u64 {
        x * y
    }

    /// Public function that uses private function
    public fun calculate_area(width: u64, height: u64): u64 {
        multiply(width, height)  // Call private function
    }

    /// Private helper function
    fun validate_input(value: u64): bool {
        value > 0 && value < 1000
    }

    public fun process_data(input: u64): u64 {
        if (validate_input(input)) {  // Call private function
            input * 2
        } else {
            0
        }
    }
}
```

### Friend Functions

Friend functions can be called from other modules that declare this module as a friend.

```move
module my_module::friend_example {
    /// Friend functions can be called from other modules that declare this module as a friend.
    friend fun sum_vector(vec: vector<u64>): u64 {
        let sum = 0u64;
        let i = 0;
        let len = vector::length(&vec);
        
        while (i < len) {
            sum = sum + *vector::borrow(&vec, i);
            i = i + 1;
        };
        
        sum
    }

    /// Alternative syntax for friend functions
    public(friend) fun do_something_friend(x: u64): u64 {
        x + 1
    }
}

/// Module that declares my_module::friend_example as a friend
module my_module::friend_caller {
    friend my_module::friend_example;

    public fun call_friend_function(): u64 {
        let numbers = vector[1, 2, 3, 4, 5];
        my_module::friend_example::sum_vector(numbers)
    }
}
```

### Package Functions

Package functions can be called from within the package but not from outside.

```move
module my_module::package_functions {
    /// Package functions can be called from within the package, but not from outside.
    package fun square(x: u64): u64 {
        x * x
    }

    /// Alternative syntax for package functions
    public(package) fun cube(x: u64): u64 {
        x * x * x
    }

    /// Public function that uses package function
    public fun calculate_power(base: u64, power: u8): u64 {
        if (power == 2) {
            square(base)  // Call package function
        } else if (power == 3) {
            cube(base)    // Call package function
        } else {
            base
        }
    }
}
```

## Entry Functions

Entry functions are special functions that can be called as standalone transactions from outside the module.

```move
module my_module::entry_functions {
    use std::signer;

    /// Entry functions can be called as standalone transactions.
    entry fun create_account(account: &signer) {
        let addr = signer::address_of(account);
        // Initialize account data
    }

    /// Entry functions can also be public, friend, or package.
    public entry fun transfer_funds(
        from: &signer,
        to: address,
        amount: u64
    ) {
        let from_addr = signer::address_of(from);
        // Transfer logic here
    }

    /// Entry functions with multiple parameters
    entry fun update_profile(
        account: &signer,
        name: String,
        age: u8
    ) {
        let addr = signer::address_of(account);
        // Update profile logic
    }

    /// Entry functions can return values (though they're typically void)
    entry fun calculate_and_return(x: u64, y: u64): u64 {
        x + y
    }
}
```

### Entry Function Best Practices

```move
module my_module::entry_best_practices {
    use std::signer;
    use std::error;

    const EINSUFFICIENT_FUNDS: u64 = 1;
    const EINVALID_AMOUNT: u64 = 2;

    /// Good: Entry function with proper validation
    entry fun safe_transfer(
        from: &signer,
        to: address,
        amount: u64
    ) {
        // Validate input
        assert!(amount > 0, error::invalid_argument(EINVALID_AMOUNT));
        assert!(to != @0x0, error::invalid_argument(3));
        
        let from_addr = signer::address_of(from);
        
        // Check balance (simplified)
        // let balance = get_balance(from_addr);
        // assert!(balance >= amount, error::invalid_state(EINSUFFICIENT_FUNDS));
        
        // Perform transfer
        // transfer_funds(from_addr, to, amount);
    }

    /// Good: Entry function with clear parameter names
    entry fun create_user_profile(
        account: &signer,
        user_name: String,
        user_age: u8,
        user_email: String
    ) {
        let user_address = signer::address_of(account);
        
        // Validate input
        assert!(user_age >= 13, error::invalid_argument(4));
        assert!(string::length(&user_name) > 0, error::invalid_argument(5));
        
        // Create profile
        // create_profile(user_address, user_name, user_age, user_email);
    }
}
```

## View Functions

View functions are read-only functions that can be called without a transaction. They are marked with the `#[view]` attribute.

```move
module my_module::view_functions {
    use std::signer;

    struct UserProfile has key, store {
        name: String,
        age: u8,
        email: String,
    }

    /// View function - can be called without a transaction
    #[view]
    public fun get_user_name(user_addr: address): String {
        assert!(exists<UserProfile>(user_addr), 0);
        borrow_global<UserProfile>(user_addr).name
    }

    /// View function that returns multiple values
    #[view]
    public fun get_user_profile(user_addr: address): (String, u8, String) {
        assert!(exists<UserProfile>(user_addr), 0);
        let profile = borrow_global<UserProfile>(user_addr);
        (profile.name, profile.age, profile.email)
    }

    /// View function with complex logic
    #[view]
    public fun is_user_adult(user_addr: address): bool {
        if (!exists<UserProfile>(user_addr)) {
            return false
        };
        
        let profile = borrow_global<UserProfile>(user_addr);
        profile.age >= 18
    }

    /// View function that doesn't access global storage
    #[view]
    public fun calculate_discount(price: u64, discount_percent: u8): u64 {
        let discount = (price * (discount_percent as u64)) / 100;
        price - discount
    }
}
```

### View Function Best Practices

```move
module my_module::view_best_practices {
    /// Good: View function with proper error handling
    #[view]
    public fun get_user_balance(user_addr: address): u64 {
        if (!exists<UserBalance>(user_addr)) {
            return 0
        };
        
        borrow_global<UserBalance>(user_addr).amount
    }

    /// Good: View function that validates input
    #[view]
    public fun calculate_compound_interest(
        principal: u64,
        rate: u64,
        time: u64
    ): u64 {
        // Validate input parameters
        assert!(principal > 0, 0);
        assert!(rate <= 100, 0);  // Rate as percentage
        assert!(time > 0, 0);
        
        // Calculate compound interest
        let rate_decimal = rate / 100;
        let amount = principal * ((1 + rate_decimal) ^ time);
        amount - principal
    }
}
```

## Test-Only Functions

Test-only functions are only available during testing and are marked with the `#[test_only]` attribute.

```move
module my_module::test_functions {
    use std::signer;

    /// Test-only functions are only available during testing.
    #[test_only]
    fun create_test_user(account: &signer, name: String): address {
        let addr = signer::address_of(account);
        // Create test user profile
        // move_to(account, UserProfile { name, age: 25, email: string::utf8(b"test@example.com") });
        addr
    }

    /// Test-only functions can be public
    #[test_only]
    public fun setup_test_environment(): vector<u64> {
        vector[1, 2, 3, 4, 5]
    }

    /// Test function that tests other functions
    #[test_only]
    public fun test_add_function() {
        let result = add(2, 3);
        assert!(result == 5, 0);
    }

    /// Test function with test account
    #[test(account = @0x1)]
    public fun test_with_account(account: signer) {
        let addr = signer::address_of(&account);
        // Test logic here
    }

    /// Private function used by tests
    fun add(x: u64, y: u64): u64 {
        x + y
    }
}
```

### Test Function Best Practices

```move
module my_module::test_best_practices {
    use std::signer;
    use std::error;

    const EINVALID_INPUT: u64 = 1;

    /// Good: Comprehensive test function
    #[test_only]
    public fun test_validation_function() {
        // Test valid input
        let result1 = validate_input(50);
        assert!(result1 == true, 0);
        
        // Test invalid input
        let result2 = validate_input(0);
        assert!(result2 == false, 0);
        
        let result3 = validate_input(1001);
        assert!(result3 == false, 0);
    }

    /// Good: Test function with multiple test cases
    #[test_only]
    public fun test_calculation_function() {
        // Test case 1: Normal calculation
        let result1 = calculate_discount(100, 10);
        assert!(result1 == 90, 0);
        
        // Test case 2: No discount
        let result2 = calculate_discount(100, 0);
        assert!(result2 == 100, 0);
        
        // Test case 3: Full discount
        let result3 = calculate_discount(100, 100);
        assert!(result3 == 0, 0);
    }

    /// Good: Test function with test account
    #[test(account = @0x1)]
    public fun test_account_operations(account: signer) {
        let addr = signer::address_of(&account);
        
        // Test account creation
        // create_account(&account);
        // assert!(exists<UserProfile>(addr), 0);
        
        // Test account operations
        // update_profile(&account, string::utf8(b"Test User"), 25);
        // let profile = get_user_profile(addr);
        // assert!(profile.0 == string::utf8(b"Test User"), 0);
    }

    /// Helper functions for tests
    fun validate_input(value: u64): bool {
        value > 0 && value <= 1000
    }

    fun calculate_discount(price: u64, discount_percent: u8): u64 {
        let discount = (price * (discount_percent as u64)) / 100;
        price - discount
    }
}
```

## Inline Functions

Inline functions are small functions that can be inlined by the compiler for better performance.

```move
module my_module::inline_functions {
    /// Inline function - compiler may inline this for better performance
    #[inline]
    public fun max(a: u64, b: u64): u64 {
        if (a > b) a else b
    }

    /// Inline function with multiple parameters
    #[inline]
    public fun clamp(value: u64, min: u64, max: u64): u64 {
        if (value < min) {
            min
        } else if (value > max) {
            max
        } else {
            value
        }
    }

    /// Inline function used in calculations
    #[inline]
    public fun is_even(n: u64): bool {
        n % 2 == 0
    }

    /// Public function that uses inline functions
    public fun process_numbers(a: u64, b: u64, c: u64): u64 {
        let max_value = max(a, b);  // Inline function call
        let clamped = clamp(c, 0, 100);  // Inline function call
        
        if (is_even(max_value)) {  // Inline function call
            max_value + clamped
        } else {
            max_value - clamped
        }
    }
}
```

### Inline Function Best Practices

```move
module my_module::inline_best_practices {
    /// Good: Small, simple inline functions
    #[inline]
    public fun square(x: u64): u64 {
        x * x
    }

    /// Good: Inline function for frequently used operations
    #[inline]
    public fun is_positive(n: u64): bool {
        n > 0
    }

    /// Good: Inline function for type conversions
    #[inline]
    public fun u8_to_u64(value: u8): u64 {
        (value as u64)
    }

    /// Avoid: Large inline functions (compiler may ignore inline hint)
    #[inline]
    public fun complex_calculation(a: u64, b: u64, c: u64): u64 {
        let temp1 = a * b;
        let temp2 = b * c;
        let temp3 = c * a;
        let result = temp1 + temp2 + temp3;
        result / 3
    }
}
```

## Function Overloading and Generics

Move doesn't support function overloading, but you can use generics to create flexible functions.

```move
module my_module::generic_functions {
    /// Generic function that works with any type that has copy, drop abilities
    public fun identity<T>(x: T): T {
        x
    }

    /// Generic function with constraints
    public fun add_generic<T: copy + drop>(a: T, b: T): T {
        // Note: This is a simplified example
        // In practice, you'd need to implement specific logic for each type
        a
    }

    /// Generic function for vector operations
    public fun get_first<T>(vec: &vector<T>): T {
        assert!(vector::length(vec) > 0, 0);
        *vector::borrow(vec, 0)
    }

    /// Generic function with multiple type parameters
    public fun create_pair<T, U>(first: T, second: U): (T, U) {
        (first, second)
    }
}
```

## Function Abilities and Constraints

Functions can have ability constraints that determine what types they can work with.

```move
module my_module::function_abilities {
    /// Function that requires copy ability
    public fun duplicate<T: copy>(x: T): (T, T) {
        (x, x)
    }

    /// Function that requires drop ability
    public fun consume<T: drop>(x: T) {
        // x is automatically dropped at the end
    }

    /// Function that requires store ability
    public fun store_value<T: store>(x: T) {
        // x can be stored in global storage
    }

    /// Function with multiple ability constraints
    public fun process_value<T: copy + drop + store>(x: T): T {
        // x can be copied, dropped, and stored
        x
    }
}
```

## Best Practices Summary

### Function Visibility

1. **Start with private**: Make functions private by default
2. **Use public sparingly**: Only expose what's necessary
3. **Use friend for related modules**: When modules need to share functionality
4. **Use package for internal APIs**: For functions used within the package

### Entry Functions

1. **Validate input**: Always validate parameters in entry functions
2. **Use clear names**: Make function names descriptive
3. **Handle errors gracefully**: Use proper error handling
4. **Keep them simple**: Delegate complex logic to private functions

### View Functions

1. **Mark with `#[view]`**: Always mark read-only functions with `#[view]`
2. **Don't modify state**: View functions should be pure
3. **Handle missing data**: Return sensible defaults for missing data
4. **Optimize for queries**: Make view functions efficient

### Test Functions

1. **Use `#[test_only]`**: Mark test functions appropriately
2. **Test edge cases**: Include boundary condition tests
3. **Use descriptive names**: Make test names clear
4. **Test error conditions**: Include tests for error cases

### Inline Functions

1. **Keep them small**: Inline functions should be simple
2. **Use for hot paths**: Inline frequently called functions
3. **Don't overuse**: Let the compiler decide when to inline
4. **Profile first**: Measure performance before optimizing

By understanding and using these different function types effectively, you can create well-structured, maintainable, and efficient Move programs.
