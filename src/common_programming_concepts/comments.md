# Comments

Comments are essential for documenting your Move code and making it more readable and maintainable. Move supports several types of comments that serve different purposes.

## Types of Comments

### 1. Documentation Comments (`///`)

Documentation comments use three forward slashes (`///`) and are used to generate documentation for your code. These comments describe what's directly below them.

```move
/// Writes a message to a single storage slot, all changes overwrite the previous.
/// Changes are recorded in `MessageChange` events.
module hello_blockchain::message {
    /// A resource for a single storage slot, holding a message.
    struct MessageHolder has key {
        message: String,
    }

    /// Event representing a change in a message, records the old and new messages, and who wrote it.
    #[event]
    struct MessageChange has drop, store {
        account: address,
        from_message: String,
        to_message: String,
    }

    /// The address does not contain a MessageHolder
    const ENO_MESSAGE: u64 = 0;

    /// Reads the message from storage slot
    #[view]
    public fun get_message(addr: address): String acquires MessageHolder {
        assert!(exists<MessageHolder>(addr), error::not_found(ENO_MESSAGE));
        borrow_global<MessageHolder>(addr).message
    }

    /// Sets the message to the storage slot
    public entry fun set_message(account: signer, message: String)
    acquires MessageHolder {
        let account_addr = signer::address_of(&account);
        if (!exists<MessageHolder>(account_addr)) {
            move_to(&account, MessageHolder {
                message,
            })
        } else {
            let old_message_holder = borrow_global_mut<MessageHolder>(account_addr);
            let from_message = old_message_holder.message;
            event::emit(MessageChange {
                account: account_addr,
                from_message,
                to_message: copy message,
            });
            old_message_holder.message = message;
        }
    }
}
```

### 2. Single-Line Comments (`//`)

Single-line comments use two forward slashes (`//`) and are used for brief explanations or notes within your code.

```move
module my_module::example {
    // This is a single-line comment
    public fun add(x: u64, y: u64): u64 {
        x + y // Add the two numbers together
    }

    public fun process_data(data: vector<u64>): u64 {
        let sum = 0u64;
        let i = 0;
        let len = vector::length(&data);
        
        while (i < len) {
            sum = sum + *vector::borrow(&data, i); // Add current element to sum
            i = i + 1; // Increment counter
        };
        
        sum
    }

    // TODO: Implement error handling for edge cases
    // FIXME: This function needs optimization for large datasets
    public fun complex_calculation(input: u64): u64 {
        // Validate input
        assert!(input > 0, 0);
        
        // Perform calculation
        let result = input * 2;
        
        result
    }
}
```

### 3. Multi-Line Comments (`/* */`)

Multi-line comments use `/*` to start and `*/` to end. They can span multiple lines and are useful for longer explanations.

```move
module my_module::complex_example {
    /*
     * This is a multi-line comment that can span
     * multiple lines. It's useful for longer explanations
     * or when you need to comment out large blocks of code.
     */
    public fun complex_function(): u64 {
        /*
         * This function performs a complex calculation:
         * 1. Initialize variables
         * 2. Perform iterative computation
         * 3. Apply final transformation
         * 4. Return result
         */
        
        let result = 0u64;
        
        /* 
         * Commented out code block:
         * let temp = 100u64;
         * result = result + temp;
         */
        
        result
    }
}
```

## Best Practices for Comments

### Documentation Comments (`///`)

1. **Use for public APIs**: Always document public functions, structs, and modules
2. **Be descriptive**: Explain what the code does, not how it does it
3. **Include examples**: When helpful, include usage examples
4. **Document parameters and return values**: Explain what each parameter does and what the function returns
5. **Use consistent formatting**: Keep documentation style consistent across your codebase

```move
/// Calculates the sum of two unsigned 64-bit integers.
/// 
/// # Arguments
/// * `a` - The first number to add
/// * `b` - The second number to add
/// 
/// # Returns
/// The sum of `a` and `b`
/// 
/// # Example
/// ```
/// let result = add(5, 3); // Returns 8
/// ```
public fun add(a: u64, b: u64): u64 {
    a + b
}
```

### Single-Line Comments (`//`)

1. **Explain complex logic**: Use comments to explain non-obvious code
2. **Avoid obvious comments**: Don't comment on what the code obviously does
3. **Use TODO/FIXME**: Mark areas that need attention
4. **Keep comments up to date**: Ensure comments reflect the current code

```move
// Good: Explains complex logic
let hash = sha3_256::hash(&data); // Hash the data for verification

// Bad: Obvious comment
let sum = a + b; // Add a and b

// Good: Marks future work
// TODO: Add input validation for edge cases
public fun process_input(input: u64): u64 {
    input * 2
}
```

### Multi-Line Comments (`/* */`)

1. **Use for block comments**: When you need to comment out large sections
2. **Document complex algorithms**: Explain multi-step processes
3. **Temporary code removal**: Comment out code you might need later

```move
/*
 * This algorithm implements the following steps:
 * 1. Validate input parameters
 * 2. Initialize data structures
 * 3. Perform iterative computation
 * 4. Apply post-processing
 * 5. Return final result
 */
public fun complex_algorithm(input: vector<u64>): u64 {
    // Implementation here
    0
}
```

## Comment Guidelines

### What to Comment

1. **Public APIs**: Always document public functions, structs, and modules
2. **Complex logic**: Explain non-obvious algorithms or business logic
3. **Assumptions**: Document any assumptions your code makes
4. **Limitations**: Note any limitations or edge cases
5. **Dependencies**: Explain dependencies on external modules or systems

### What Not to Comment

1. **Obvious code**: Don't comment on what the code obviously does
2. **Outdated information**: Don't leave comments that are no longer accurate
3. **Implementation details**: Focus on what, not how (unless the how is complex)

### Comment Style

1. **Be concise**: Keep comments brief but informative
2. **Use proper grammar**: Write comments in clear, grammatically correct language
3. **Be consistent**: Use consistent terminology and style throughout your codebase
4. **Update with code**: When you change code, update related comments

## Examples in Context

### Module Documentation

```move
/// A simple banking module that allows users to deposit and withdraw funds.
/// 
/// This module provides basic banking functionality including:
/// * Account creation and management
/// * Deposit and withdrawal operations
/// * Balance checking
/// * Transaction history tracking
/// 
/// # Security
/// All operations require proper authorization and validation.
module my_bank::banking {
    use std::signer;
    use std::error;
    
    /// Error codes for banking operations
    const EINSUFFICIENT_FUNDS: u64 = 1;
    const EACCOUNT_NOT_FOUND: u64 = 2;
    
    /// Represents a user's bank account
    struct Account has key, store {
        balance: u64,
        owner: address,
    }
    
    /// Creates a new bank account for the given signer
    public entry fun create_account(account: &signer) {
        let account_addr = signer::address_of(account);
        move_to(account, Account {
            balance: 0,
            owner: account_addr,
        });
    }
    
    /// Deposits the specified amount into the account
    public entry fun deposit(account: &signer, amount: u64) acquires Account {
        let account_addr = signer::address_of(account);
        let account_ref = borrow_global_mut<Account>(account_addr);
        account_ref.balance = account_ref.balance + amount;
    }
}
```

### Function Documentation

```move
/// Calculates the factorial of a given number.
/// 
/// The factorial of a number n is the product of all positive integers
/// less than or equal to n. For example, 5! = 5 × 4 × 3 × 2 × 1 = 120.
/// 
/// # Arguments
/// * `n` - The number to calculate factorial for (must be <= 20)
/// 
/// # Returns
/// The factorial of n
/// 
/// # Panics
/// Panics if n > 20 due to u64 overflow
/// 
/// # Example
/// ```
/// let result = factorial(5); // Returns 120
/// ```
public fun factorial(n: u64): u64 {
    if (n <= 1) {
        return 1
    };
    
    let result = 1u64;
    let i = 2u64;
    
    while (i <= n) {
        result = result * i;
        i = i + 1;
    };
    
    result
}
```

## Documentation Generation

Move documentation comments can be used to generate documentation for your modules. The `///` comments are processed by documentation generators to create readable documentation for your codebase.

When writing documentation comments, remember that they should be:
- **Clear and concise**: Easy to understand
- **Complete**: Cover all important aspects
- **Accurate**: Reflect the actual behavior of the code
- **Helpful**: Provide value to developers using your code

By following these guidelines, you'll create well-documented, maintainable Move code that's easy for others to understand and use.
