# Variables

Variables are fundamental building blocks in Move programs that allow you to store and manipulate data. Understanding how to create and manage variables is essential for writing effective Move code.

## Variable Declaration

### Basic Variable Declaration

Variables in Move are declared using the `let` keyword, followed by the variable name and an optional type annotation.

```move
module my_module::variables {
    public fun basic_variables() {
        // Variable with type inference
        let x = 42;
        
        // Variable with explicit type annotation
        let y: u64 = 100;
        
        // Variable with explicit type and suffix
        let z = 255u8;
        
        // Boolean variable
        let is_active = true;
        
        // String variable
        let message = string::utf8(b"Hello, Move!");
        
        // Address variable
        let account_addr = @0x1;
    }
}
```

### Variable Declaration with Different Types

```move
public fun variable_types() {
    // Integer types
    let small_number: u8 = 255;
    let medium_number: u16 = 65535;
    let large_number: u64 = 18446744073709551615;
    let very_large_number: u128 = 340282366920938463463374607431768211455u128;
    
    // Boolean type
    let flag: bool = true;
    
    // Address type
    let addr: address = @0xABCDEF;
    
    // Vector type
    let numbers: vector<u64> = vector[1, 2, 3, 4, 5];
    
    // String type
    let text: String = string::utf8(b"Move programming");
    
    // Tuple type
    let pair: (u64, String) = (42, string::utf8(b"answer"));
}
```

## Variable Assignment and Mutability

### Immutable Variables (Default)

By default, variables in Move are immutable, meaning they cannot be changed after declaration.

```move
public fun immutable_variables() {
    let x = 42;
    // x = 50; // This would cause a compilation error
    
    let message = string::utf8(b"Hello");
    // message = string::utf8(b"World"); // This would cause a compilation error
}
```

### Mutable Variables

To create a mutable variable, use the `mut` keyword.

```move
public fun mutable_variables() {
    // Mutable variable declaration
    let mut x = 42;
    x = 50; // Now this is allowed
    
    let mut counter = 0u64;
    counter = counter + 1;
    counter = counter + 1;
    
    // Mutable vector
    let mut numbers = vector[1, 2, 3];
    vector::push_back(&mut numbers, 4);
    vector::push_back(&mut numbers, 5);
    
    // Mutable string
    let mut message = string::utf8(b"Hello");
    message = message + string::utf8(b" World");
}
```

### Variable Reassignment

```move
public fun variable_reassignment() {
    let mut value = 10;
    
    // Reassign with different value
    value = 20;
    
    // Reassign with calculation
    value = value * 2;
    
    // Reassign with function result
    value = add(value, 5);
    
    // Reassign with conditional
    if (value > 50) {
        value = 100;
    } else {
        value = 0;
    };
}

fun add(a: u64, b: u64): u64 {
    a + b
}
```

## Variable Scoping

### Local Variables

Variables declared within a function are local to that function and are automatically dropped when the function ends.

```move
public fun local_variables() {
    let x = 10; // Local variable
    
    {
        let y = 20; // Local variable in inner scope
        let z = x + y; // Can access outer scope variable
        // z is dropped at end of inner scope
    };
    
    // y is not accessible here
    // z is not accessible here
    
    // x is still accessible
    let result = x * 2;
}
```

### Variable Shadowing

Move allows variable shadowing, where a new variable with the same name can be declared in an inner scope.

```move
public fun variable_shadowing() {
    let x = 10;
    
    {
        let x = 20; // Shadows the outer x
        // x is 20 in this scope
    };
    
    // x is 10 again in outer scope
}
```

### Variable Lifetime

```move
public fun variable_lifetime() {
    let mut counter = 0u64;
    
    while (counter < 5) {
        let temp = counter * 2; // temp is created in each iteration
        counter = counter + 1;
        // temp is dropped at end of each iteration
    };
    
    // counter is still available here
    let final_value = counter;
}
```

## Variable Initialization

### Immediate Initialization

Variables must be initialized when declared.

```move
public fun immediate_initialization() {
    // All variables must be initialized
    let x = 42;
    let y: u64 = 100;
    let flag = true;
    let message = string::utf8(b"Hello");
}
```

### Conditional Initialization

Variables can be initialized conditionally.

```move
public fun conditional_initialization() {
    let condition = true;
    
    let value = if (condition) {
        100
    } else {
        200
    };
    
    // value is now either 100 or 200
}
```

### Initialization with Function Calls

```move
public fun initialization_with_functions() {
    let result = calculate_value(10);
    let message = create_message(string::utf8(b"Hello"));
    let numbers = create_vector(5);
}

fun calculate_value(input: u64): u64 {
    input * 2
}

fun create_message(prefix: String): String {
    prefix + string::utf8(b" World")
}

fun create_vector(size: u64): vector<u64> {
    let mut vec = vector::empty<u64>();
    let i = 0;
    while (i < size) {
        vector::push_back(&mut vec, i);
        i = i + 1;
    };
    vec
}
```

## Variable Patterns

### Destructuring Assignment

Move supports destructuring assignment for tuples and structs.

```move
public fun destructuring() {
    // Tuple destructuring
    let (x, y) = (10, 20);
    
    // Nested tuple destructuring
    let ((a, b), c) = ((1, 2), 3);
    
    // Struct destructuring (if you have a struct)
    // let Point { x, y } = Point { x: 10, y: 20 };
}
```

### Multiple Variable Declaration

```move
public fun multiple_variables() {
    // Declare multiple variables
    let x = 1;
    let y = 2;
    let z = 3;
    
    // Or use tuple destructuring
    let (a, b, c) = (1, 2, 3);
    
    // With different types
    let (number, text, flag) = (42, string::utf8(b"Hello"), true);
}
```

## Variable Best Practices

### Choose Descriptive Names

```move
public fun good_naming() {
    // Good: Descriptive names
    let user_age = 25;
    let account_balance = 1000;
    let is_user_active = true;
    let user_name = string::utf8(b"Alice");
    
    // Bad: Unclear names
    let x = 25;
    let y = 1000;
    let flag = true;
    let s = string::utf8(b"Alice");
}
```

### Use Appropriate Types

```move
public fun appropriate_types() {
    // Use u8 for small numbers
    let age: u8 = 25;
    
    // Use u64 for most calculations
    let balance: u64 = 1000000;
    
    // Use u128 for large financial values
    let total_supply: u128 = 1000000000000000000u128;
    
    // Use bool for flags
    let is_enabled: bool = true;
    
    // Use address for account identifiers
    let user_address: address = @0x1;
}
```

### Minimize Mutable Variables

```move
public fun minimize_mutability() {
    // Good: Use immutable variables when possible
    let max_attempts = 3;
    let timeout_duration = 5000;
    
    // Only use mut when you need to change the value
    let mut current_attempt = 0;
    let mut elapsed_time = 0;
    
    while (current_attempt < max_attempts) {
        current_attempt = current_attempt + 1;
        elapsed_time = elapsed_time + 1000;
    };
}
```

### Initialize Variables Close to Use

```move
public fun initialize_close_to_use() {
    // Good: Initialize when needed
    let result = perform_calculation(10);
    
    if (result > 50) {
        let message = string::utf8(b"High result");
        // Use message here
    } else {
        let message = string::utf8(b"Low result");
        // Use message here
    };
    
    // Bad: Initialize too early
    // let message = string::utf8(b""); // Unused variable
    // let result = perform_calculation(10);
    // if (result > 50) {
    //     message = string::utf8(b"High result");
    // } else {
    //     message = string::utf8(b"Low result");
    // };
}
```

## Common Variable Patterns

### Counter Pattern

```move
public fun counter_pattern() {
    let mut counter = 0u64;
    let max_count = 10;
    
    while (counter < max_count) {
        // Process something
        counter = counter + 1;
    };
}
```

### Accumulator Pattern

```move
public fun accumulator_pattern() {
    let numbers = vector[1, 2, 3, 4, 5];
    let mut sum = 0u64;
    let i = 0;
    let len = vector::length(&numbers);
    
    while (i < len) {
        let current = *vector::borrow(&numbers, i);
        sum = sum + current;
        i = i + 1;
    };
    
    // sum now contains the total
}
```

### Flag Pattern

```move
public fun flag_pattern() {
    let numbers = vector[1, 2, 3, 4, 5];
    let mut found = false;
    let mut found_value = 0u64;
    let target = 3;
    let i = 0;
    let len = vector::length(&numbers);
    
    while (i < len && !found) {
        let current = *vector::borrow(&numbers, i);
        if (current == target) {
            found = true;
            found_value = current;
        };
        i = i + 1;
    };
}
```

### Temporary Variable Pattern

```move
public fun temporary_variable_pattern() {
    let x = 10;
    let y = 20;
    
    // Use temporary variable for complex calculation
    let temp_sum = x + y;
    let result = temp_sum * 2;
    
    // Or for readability
    let base_value = calculate_base(x, y);
    let adjusted_value = apply_adjustment(base_value);
    let final_result = apply_discount(adjusted_value);
}

fun calculate_base(a: u64, b: u64): u64 {
    a + b
}

fun apply_adjustment(value: u64): u64 {
    value * 2
}

fun apply_discount(value: u64): u64 {
    value - (value / 10)
}
```

## Variable Safety

### Type Safety

Move's type system prevents many common programming errors.

```move
public fun type_safety() {
    let x: u64 = 42;
    let y: u8 = 255;
    
    // Type conversion is explicit
    let z: u64 = x + (y as u64);
    
    // This would cause a compilation error:
    // let invalid = x + y; // Cannot add u64 and u8 directly
}
```

### Bounds Checking

```move
public fun bounds_checking() {
    let mut index = 0u64;
    let max_index = 10;
    
    // Safe bounds checking
    if (index < max_index) {
        index = index + 1;
    };
    
    // Safe array access (if you had an array)
    // if (index < vector::length(&array)) {
    //     let element = *vector::borrow(&array, index);
    // };
}
```

### Null Safety

Move doesn't have null values, which prevents null pointer errors.

```move
public fun null_safety() {
    // Move doesn't have null, so no null pointer errors
    let value: u64 = 42; // Always has a value
    
    // Use Option<T> for optional values
    // let optional_value: Option<u64> = option::some(42);
}
```

## Performance Considerations

### Variable Reuse

```move
public fun variable_reuse() {
    let mut temp = 0u64;
    
    // Reuse variable for different purposes
    temp = calculate_value(10);
    // Use temp...
    
    temp = calculate_value(20);
    // Use temp again...
    
    temp = calculate_value(30);
    // Use temp one more time...
}

fun calculate_value(input: u64): u64 {
    input * 2
}
```

### Avoid Unnecessary Variables

```move
public fun avoid_unnecessary_variables() {
    // Good: Direct return
    let result = add(10, 20);
    
    // Bad: Unnecessary intermediate variable
    // let temp = add(10, 20);
    // let result = temp;
}

fun add(a: u64, b: u64): u64 {
    a + b
}
```

By understanding and following these variable management practices, you can write more readable, maintainable, and efficient Move code. Variables are the foundation of data manipulation in Move, and proper variable management is essential for building robust smart contracts.
