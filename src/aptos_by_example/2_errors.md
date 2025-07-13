# Errors

## Introduction

Error handling is a critical aspect of smart contract development. In Move, errors are handled through a combination of abort codes and structured error types. This chapter demonstrates how to handle errors effectively in Aptos smart contracts.

**Definition 3.1 (Error)**
An error is an exceptional condition that occurs during program execution, requiring special handling to maintain program correctness and user experience.

## Error Handling in Move

### Abort Codes

**Definition 3.2 (Abort Code)**
An abort code is a numeric identifier that indicates why a program terminated abnormally.

```move
module errors::basic_errors {
    use std::signer;
    
    const E_INSUFFICIENT_BALANCE: u64 = 1;
    const E_INVALID_AMOUNT: u64 = 2;
    const E_UNAUTHORIZED: u64 = 3;
    
    struct Account has key {
        balance: u64,
    }
    
    public entry fun withdraw(account: &signer, amount: u64) {
        let account_addr = signer::address_of(account);
        let account_ref = borrow_global_mut<Account>(account_addr);
        
        if (amount == 0) {
            abort E_INVALID_AMOUNT
        };
        
        if (account_ref.balance < amount) {
            abort E_INSUFFICIENT_BALANCE
        };
        
        account_ref.balance = account_ref.balance - amount;
    }
    
    public entry fun transfer(
        from: &signer,
        to: address,
        amount: u64,
    ) {
        let from_addr = signer::address_of(from);
        
        if (amount == 0) {
            abort E_INVALID_AMOUNT
        };
        
        let from_account = borrow_global_mut<Account>(from_addr);
        if (from_account.balance < amount) {
            abort E_INSUFFICIENT_BALANCE
        };
        
        let to_account = borrow_global_mut<Account>(to);
        from_account.balance = from_account.balance - amount;
        to_account.balance = to_account.balance + amount;
    }
}
```

### Error Constants

**Principle 3.1 (Error Constant Naming)**
Use descriptive names for error constants that clearly indicate the error condition:

```move
// Good: Clear and descriptive
const E_INSUFFICIENT_FUNDS: u64 = 1;
const E_INVALID_RECIPIENT: u64 = 2;
const E_ACCOUNT_NOT_FOUND: u64 = 3;

// Bad: Unclear and generic
const E_ERROR_1: u64 = 1;
const E_BAD: u64 = 2;
```

### Error Ranges

**Definition 3.3 (Error Range)**
A range of abort codes reserved for a specific module or functionality.

```move
module errors::error_ranges {
    // Reserve error codes 1000-1999 for this module
    const E_BASE: u64 = 1000;
    
    const E_INVALID_OPERATION: u64 = E_BASE + 1;
    const E_INSUFFICIENT_PERMISSIONS: u64 = E_BASE + 2;
    const E_RESOURCE_NOT_FOUND: u64 = E_BASE + 3;
    const E_INVALID_STATE: u64 = E_BASE + 4;
}
```

## Advanced Error Handling

### Custom Error Types

**Definition 3.4 (Custom Error Type)**
A structured error type that provides additional context about the error condition.

```move
module errors::custom_errors {
    use std::signer;
    use std::vector;
    
    struct ErrorInfo has store {
        code: u64,
        message: vector<u8>,
        details: vector<u8>,
    }
    
    struct Account has key {
        balance: u64,
        error_history: vector<ErrorInfo>,
    }
    
    public entry fun withdraw_with_details(
        account: &signer,
        amount: u64,
    ) {
        let account_addr = signer::address_of(account);
        let account_ref = borrow_global_mut<Account>(account_addr);
        
        if (amount == 0) {
            let error = ErrorInfo {
                code: 1,
                message: b"Invalid amount: cannot withdraw zero",
                details: b"Amount must be greater than 0",
            };
            account_ref.error_history.push_back(error);
            abort 1
        };
        
        if (account_ref.balance < amount) {
            let error = ErrorInfo {
                code: 2,
                message: b"Insufficient balance",
                details: vector::empty<u8>(), // Could include balance info
            };
            account_ref.error_history.push_back(error);
            abort 2
        };
        
        account_ref.balance = account_ref.balance - amount;
    }
}
```

### Error Recovery

**Algorithm 3.1 (Error Recovery Strategy)**
```
1. Detect the error condition
2. Log or record the error details
3. Attempt to recover if possible
4. If recovery fails, abort with appropriate code
5. Provide meaningful error information
```

```move
module errors::error_recovery {
    use std::signer;
    use std::vector;
    
    struct RecoveryAttempt has store {
        error_code: u64,
        retry_count: u64,
        max_retries: u64,
    }
    
    struct Account has key {
        balance: u64,
        recovery_info: RecoveryAttempt,
    }
    
    public entry fun withdraw_with_retry(
        account: &signer,
        amount: u64,
    ) {
        let account_addr = signer::address_of(account);
        let account_ref = borrow_global_mut<Account>(account_addr);
        
        if (amount == 0) {
            abort 1
        };
        
        if (account_ref.balance < amount) {
            // Try to recover by checking if we can withdraw a smaller amount
            let available = account_ref.balance;
            if (available > 0) {
                account_ref.balance = 0;
                // Could emit an event about partial withdrawal
            } else {
                abort 2
            }
        } else {
            account_ref.balance = account_ref.balance - amount;
        }
    }
}
```

## Error Propagation

### Function-Level Error Handling

**Definition 3.5 (Error Propagation)**
The process of passing error information from lower-level functions to higher-level functions.

```move
module errors::error_propagation {
    use std::signer;
    
    const E_INVALID_INPUT: u64 = 1;
    const E_COMPUTATION_FAILED: u64 = 2;
    const E_STORAGE_ERROR: u64 = 3;
    
    struct Account has key {
        balance: u64,
    }
    
    fun validate_input(amount: u64): bool {
        amount > 0 && amount <= 1000000
    }
    
    fun perform_computation(amount: u64): u64 {
        if (amount > 500000) {
            abort E_COMPUTATION_FAILED
        };
        amount * 2
    }
    
    fun update_storage(account: &mut Account, new_balance: u64) {
        if (new_balance > 1000000) {
            abort E_STORAGE_ERROR
        };
        account.balance = new_balance;
    }
    
    public entry fun complex_operation(
        account: &signer,
        amount: u64,
    ) {
        // Validate input
        if (!validate_input(amount)) {
            abort E_INVALID_INPUT
        };
        
        // Perform computation
        let result = perform_computation(amount);
        
        // Update storage
        let account_ref = borrow_global_mut<Account>(signer::address_of(account));
        update_storage(account_ref, result);
    }
}
```

### Module-Level Error Handling

**Principle 3.2 (Module Error Organization)**
Organize errors at the module level for better maintainability:

```move
module errors::module_errors {
    // Module-specific error codes
    const E_MODULE_BASE: u64 = 2000;
    
    // Account-related errors
    const E_ACCOUNT_NOT_FOUND: u64 = E_MODULE_BASE + 1;
    const E_INSUFFICIENT_BALANCE: u64 = E_MODULE_BASE + 2;
    const E_INVALID_ACCOUNT_STATE: u64 = E_MODULE_BASE + 3;
    
    // Transaction-related errors
    const E_INVALID_TRANSACTION: u64 = E_MODULE_BASE + 10;
    const E_TRANSACTION_TOO_LARGE: u64 = E_MODULE_BASE + 11;
    const E_TRANSACTION_EXPIRED: u64 = E_MODULE_BASE + 12;
    
    // Permission-related errors
    const E_INSUFFICIENT_PERMISSIONS: u64 = E_MODULE_BASE + 20;
    const E_UNAUTHORIZED_OPERATION: u64 = E_MODULE_BASE + 21;
    
    struct Account has key {
        balance: u64,
        permissions: vector<address>,
    }
    
    public entry fun authorized_withdraw(
        account: &signer,
        target: address,
        amount: u64,
    ) {
        let account_addr = signer::address_of(account);
        
        // Check if account exists
        if (!exists<Account>(target)) {
            abort E_ACCOUNT_NOT_FOUND
        };
        
        // Check permissions
        let account_ref = borrow_global<Account>(target);
        if (!vector::contains(&account_ref.permissions, &account_addr)) {
            abort E_INSUFFICIENT_PERMISSIONS
        };
        
        // Check balance
        if (account_ref.balance < amount) {
            abort E_INSUFFICIENT_BALANCE
        };
        
        // Perform withdrawal
        let mut_account_ref = borrow_global_mut<Account>(target);
        mut_account_ref.balance = mut_account_ref.balance - amount;
    }
}
```

## Error Testing

### Unit Testing Errors

**Definition 3.6 (Error Testing)**
Testing that functions correctly handle error conditions and abort with appropriate codes.

```move
#[test_only]
module errors::error_tests {
    use std::signer;
    use errors::basic_errors;
    
    #[test]
    fun test_withdraw_zero_amount() {
        let account = account::create_account_for_test(@0x1);
        account::initialize_account(&account);
        
        // This should abort with E_INVALID_AMOUNT
        basic_errors::withdraw(&account, 0);
    }
    
    #[test]
    #[expected_failure(abort_code = errors::basic_errors::E_INVALID_AMOUNT)]
    fun test_withdraw_zero_amount_expected() {
        let account = account::create_account_for_test(@0x1);
        account::initialize_account(&account);
        
        // This test expects the function to abort with E_INVALID_AMOUNT
        basic_errors::withdraw(&account, 0);
    }
    
    #[test]
    fun test_withdraw_insufficient_balance() {
        let account = account::create_account_for_test(@0x1);
        account::initialize_account(&account);
        
        // This should abort with E_INSUFFICIENT_BALANCE
        basic_errors::withdraw(&account, 100);
    }
    
    #[test]
    #[expected_failure(abort_code = errors::basic_errors::E_INSUFFICIENT_BALANCE)]
    fun test_withdraw_insufficient_balance_expected() {
        let account = account::create_account_for_test(@0x1);
        account::initialize_account(&account);
        
        // This test expects the function to abort with E_INSUFFICIENT_BALANCE
        basic_errors::withdraw(&account, 100);
    }
}
```

### Integration Testing

```move
#[test_only]
module errors::integration_tests {
    use std::signer;
    use errors::custom_errors;
    
    #[test]
    fun test_error_recovery_flow() {
        let account = account::create_account_for_test(@0x1);
        account::initialize_account(&account);
        
        // Test that error recovery works as expected
        // Implementation would depend on the specific recovery mechanism
    }
    
    #[test]
    fun test_error_propagation() {
        let account = account::create_account_for_test(@0x1);
        account::initialize_account(&account);
        
        // Test that errors propagate correctly through function calls
        // Implementation would test the complex_operation function
    }
}
```

## Best Practices

**Principle 3.3 (Error Handling Best Practices)**
1. **Use Descriptive Error Codes**: Make error codes meaningful and well-documented
2. **Organize Error Ranges**: Use ranges to avoid conflicts between modules
3. **Test Error Conditions**: Write tests for all error paths
4. **Provide Context**: Include relevant information in error messages
5. **Handle Errors Gracefully**: Attempt recovery when possible
6. **Log Errors**: Record error information for debugging
7. **Use Expected Failures**: Use `#[expected_failure]` in tests for error conditions

## Common Error Patterns

### Input Validation

```move
module errors::input_validation {
    use std::signer;
    
    const E_INVALID_AMOUNT: u64 = 1;
    const E_INVALID_ADDRESS: u64 = 2;
    const E_INVALID_STRING: u64 = 3;
    
    public entry fun validate_and_process(
        amount: u64,
        recipient: address,
        message: vector<u8>,
    ) {
        // Validate amount
        if (amount == 0 || amount > 1000000) {
            abort E_INVALID_AMOUNT
        };
        
        // Validate address
        if (recipient == @0x0) {
            abort E_INVALID_ADDRESS
        };
        
        // Validate string
        if (std::string::length(&message) == 0) {
            abort E_INVALID_STRING
        };
        
        // Process the validated inputs
        // Implementation here...
    }
}
```

### State Validation

```move
module errors::state_validation {
    use std::signer;
    
    const E_INVALID_STATE: u64 = 1;
    const E_ALREADY_INITIALIZED: u64 = 2;
    const E_NOT_INITIALIZED: u64 = 3;
    
    struct State has key {
        initialized: bool,
        value: u64,
    }
    
    public entry fun initialize(account: &signer) {
        let account_addr = signer::address_of(account);
        
        if (exists<State>(account_addr)) {
            let state = borrow_global<State>(account_addr);
            if (state.initialized) {
                abort E_ALREADY_INITIALIZED
            }
        };
        
        move_to(account, State {
            initialized: true,
            value: 0,
        });
    }
    
    public entry fun update_value(account: &signer, new_value: u64) {
        let account_addr = signer::address_of(account);
        
        if (!exists<State>(account_addr)) {
            abort E_NOT_INITIALIZED
        };
        
        let state = borrow_global_mut<State>(account_addr);
        if (!state.initialized) {
            abort E_INVALID_STATE
        };
        
        state.value = new_value;
    }
}
```

## Conclusion

Error handling is essential for building robust smart contracts. Move's abort mechanism provides a simple but effective way to handle errors, while custom error types and recovery mechanisms allow for more sophisticated error handling.

By following best practices and testing error conditions thoroughly, developers can create smart contracts that handle exceptional situations gracefully and provide meaningful feedback to users.

## Exercises

1. **Exercise 3.1**: Create a module with custom error types and implement error recovery
2. **Exercise 3.2**: Write comprehensive tests for error conditions using `#[expected_failure]`
3. **Exercise 3.3**: Implement a function that validates multiple inputs and provides detailed error information
4. **Exercise 3.4**: Design an error handling system that logs errors and attempts recovery

## References

1. Move Language Error Handling Guide
2. Aptos Error Codes Reference
3. Smart Contract Testing Best Practices
4. Move Prover Error Verification

