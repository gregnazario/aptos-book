# Data Types

Move is a statically typed language, which means every variable and expression has a type that is known at compile time. Understanding the available data types is fundamental to writing effective Move code.

## Primitive Types

### Integer Types

Move provides several integer types with different sizes and characteristics.

#### Unsigned Integers

```move
module my_module::integers {
    // 8-bit unsigned integer (0 to 255)
    public fun u8_example(): u8 {
        255u8
    }

    // 16-bit unsigned integer (0 to 65,535)
    public fun u16_example(): u16 {
        65535u16
    }

    // 32-bit unsigned integer (0 to 4,294,967,295)
    public fun u32_example(): u32 {
        4294967295u32
    }

    // 64-bit unsigned integer (0 to 18,446,744,073,709,551,615)
    public fun u64_example(): u64 {
        18446744073709551615u64
    }

    // 128-bit unsigned integer (0 to 2^128 - 1)
    public fun u128_example(): u128 {
        340282366920938463463374607431768211455u128
    }

    // 256-bit unsigned integer (0 to 2^256 - 1)
    public fun u256_example(): u256 {
        115792089237316195423570985008687907853269984665640564039457584007913129639935u256
    }
}
```

#### Integer Literals

```move
public fun integer_literals() {
    // Default integer literals are u64
    let default_int: u64 = 42;
    
    // Explicit type annotations
    let small_int: u8 = 255u8;
    let medium_int: u16 = 65535u16;
    let large_int: u32 = 4294967295u32;
    let very_large_int: u128 = 340282366920938463463374607431768211455u128;
    
    // Hex literals
    let hex_u8: u8 = 0xFFu8;
    let hex_u64: u64 = 0xFFFFFFFFu64;
}
```

#### Integer Operations

```move
public fun integer_operations() {
    let a: u64 = 10;
    let b: u64 = 3;
    
    // Arithmetic operations
    let sum = a + b;        // 13
    let difference = a - b;  // 7
    let product = a * b;     // 30
    let quotient = a / b;    // 3
    let remainder = a % b;   // 1
    
    // Bitwise operations
    let bitwise_and = a & b;  // 2
    let bitwise_or = a | b;   // 11
    let bitwise_xor = a ^ b;  // 9
    let left_shift = a << 2;  // 40
    let right_shift = a >> 1; // 5
    
    // Comparison operations
    let is_equal = a == b;     // false
    let is_not_equal = a != b; // true
    let is_greater = a > b;    // true
    let is_less = a < b;       // false
    let is_greater_equal = a >= b; // true
    let is_less_equal = a <= b;    // false
}
```

### Boolean Type

The boolean type represents true or false values.

```move
public fun boolean_examples() {
    // Boolean literals
    let true_value: bool = true;
    let false_value: bool = false;
    
    // Boolean operations
    let and_result = true && false;  // false
    let or_result = true || false;   // true
    let not_result = !true;          // false
    
    // Comparison results
    let comparison_result: bool = 5 > 3;  // true
    let equality_result: bool = 5 == 5;   // true
}
```

### Address Type

Addresses represent 32-byte identifiers used for accounts, modules, and resources.

```move
public fun address_examples() {
    // Address literals
    let account_address: address = @0x1;
    let custom_address: address = @0xABCDEF;
    let full_address: address = @0x0000000000000000000000000000000000000000000000000000000000000001;
    
    // Special addresses
    let zero_address: address = @0x0;
    let framework_address: address = @0x1;  // Aptos framework
    let token_address: address = @0x3;      // Legacy token standard
    let object_address: address = @0x4;     // Object standard
}
```

### Vector Type

Vectors are dynamic arrays that can hold multiple values of the same type.

```move
public fun vector_examples() {
    // Creating vectors
    let empty_vector: vector<u64> = vector::empty<u64>();
    let literal_vector: vector<u64> = vector[1, 2, 3, 4, 5];
    let string_vector: vector<String> = vector[
        string::utf8(b"hello"),
        string::utf8(b"world")
    ];
    
    // Vector operations
    let mut vec = vector[1, 2, 3];
    vector::push_back(&mut vec, 4);
    let length = vector::length(&vec);
    let first_element = *vector::borrow(&vec, 0);
    let last_element = vector::pop_back(&mut vec);
}
```

### String Type

Strings are UTF-8 encoded text stored as vectors of bytes.

```move
public fun string_examples() {
    // Creating strings
    let empty_string: String = string::utf8(b"");
    let hello_string: String = string::utf8(b"Hello, World!");
    let unicode_string: String = string::utf8(b"Hello 世界");
    
    // String operations
    let length = string::length(&hello_string);
    let is_empty = string::is_empty(&empty_string);
    let concatenated = string::utf8(b"Hello") + string::utf8(b" World");
    
    // String comparison
    let are_equal = hello_string == string::utf8(b"Hello, World!");
    let are_not_equal = hello_string != string::utf8(b"Goodbye");
}
```

### Signer Type

The signer type represents the account that signed the transaction.

```move
public fun signer_examples(account: &signer) {
    // Getting the address of the signer
    let account_address = signer::address_of(account);
    
    // Signer is used for resource operations
    // move_to(account, MyResource { data: 42 });
}
```

## Type Abilities

Move types have abilities that determine how they can be used. The main abilities are:

- **copy**: Can be copied
- **drop**: Can be dropped (destroyed)
- **store**: Can be stored in global storage
- **key**: Can be used as a key in global storage

### Ability Examples

```move
module my_module::abilities {
    // Integer types have copy, drop, and store abilities
    public fun integer_abilities() {
        let x: u64 = 42;
        let y = x;  // Copy
        // x is still available due to copy ability
    }
    
    // Vector has copy, drop, and store abilities
    public fun vector_abilities() {
        let v1: vector<u64> = vector[1, 2, 3];
        let v2 = v1;  // Copy
        // v1 is still available
    }
    
    // String has copy, drop, and store abilities
    public fun string_abilities() {
        let s1: String = string::utf8(b"hello");
        let s2 = s1;  // Copy
        // s1 is still available
    }
    
    // Signer has drop ability only
    public fun signer_abilities(account: &signer) {
        let addr = signer::address_of(account);
        // Cannot copy signer, but can drop it
    }
}
```

## Type Annotations

Move uses type annotations to specify the type of variables and function parameters.

```move
public fun type_annotations() {
    // Explicit type annotations
    let explicit_u64: u64 = 42;
    let explicit_bool: bool = true;
    let explicit_address: address = @0x1;
    let explicit_vector: vector<u64> = vector[1, 2, 3];
    let explicit_string: String = string::utf8(b"hello");
    
    // Type inference (when possible)
    let inferred_u64 = 42;  // Inferred as u64
    let inferred_bool = true;  // Inferred as bool
    let inferred_vector = vector[1, 2, 3];  // Inferred as vector<u64>
}
```

## Type Conversion

Move is strict about type conversions and requires explicit casting.

```move
public fun type_conversion() {
    // Explicit casting between integer types
    let small: u8 = 255;
    let medium: u16 = (small as u16);
    let large: u64 = (medium as u64);
    
    // Casting to smaller types (may truncate)
    let large_num: u64 = 1000;
    let small_num: u8 = (large_num as u8);  // Will be 232 (1000 % 256)
    
    // Boolean to integer conversion
    let bool_val: bool = true;
    let int_val: u64 = (bool_val as u64);  // 1 for true, 0 for false
}
```

## Generic Types

Move supports generic types for creating reusable code.

```move
public fun generic_examples() {
    // Generic vector operations
    let int_vector: vector<u64> = vector[1, 2, 3];
    let string_vector: vector<String> = vector[
        string::utf8(b"hello"),
        string::utf8(b"world")
    ];
    
    // Generic function example
    let int_length = vector::length(&int_vector);
    let string_length = vector::length(&string_vector);
}
```

## Type Safety

Move's type system prevents many common programming errors.

```move
public fun type_safety_examples() {
    // This would cause a compilation error:
    // let x: u64 = "hello";  // Cannot assign string to u64
    
    // This would cause a compilation error:
    // let y: u8 = 256;  // Value too large for u8
    
    // This would cause a compilation error:
    // let z = x + "world";  // Cannot add u64 and string
    
    // Correct usage
    let x: u64 = 42;
    let y: u8 = 255;
    let z: u64 = x + (y as u64);
}
```

## Best Practices

### Choose Appropriate Types

```move
public fun choose_types() {
    // Use u8 for small numbers (0-255)
    let age: u8 = 25;
    
    // Use u64 for most integer operations
    let balance: u64 = 1000000;
    
    // Use u128 for large financial calculations
    let total_supply: u128 = 1000000000000000000u128;
    
    // Use u256 for cryptographic operations
    let private_key: u256 = 0x1234567890ABCDEFu256;
}
```

### Use Type Annotations for Clarity

```move
public fun clear_types() {
    // Explicit types make code more readable
    let user_id: u64 = 12345;
    let is_active: bool = true;
    let user_address: address = @0xABCDEF;
    let user_name: String = string::utf8(b"Alice");
    
    // Avoid ambiguous literals
    let small_number: u8 = 42u8;  // Clear that this is u8
    let large_number: u128 = 1000000000000000000u128;  // Clear that this is u128
}
```

### Handle Type Conversions Carefully

```move
public fun safe_conversions() {
    let large: u64 = 1000;
    
    // Check bounds before converting to smaller types
    if (large <= 255) {
        let small: u8 = (large as u8);
        // Safe conversion
    } else {
        // Handle overflow case
        // abort 0
    }
    
    // Use appropriate types for calculations
    let a: u64 = 1000000;
    let b: u64 = 2000000;
    let result: u64 = a * b;  // May overflow u64
    
    // Consider using u128 for large calculations
    let safe_result: u128 = (a as u128) * (b as u128);
}
```

### Use Vectors Efficiently

```move
public fun vector_best_practices() {
    // Pre-allocate when you know the size
    let mut numbers = vector::empty<u64>();
    vector::push_back(&mut numbers, 1);
    vector::push_back(&mut numbers, 2);
    vector::push_back(&mut numbers, 3);
    
    // Use appropriate element types
    let small_numbers: vector<u8> = vector[1, 2, 3, 4, 5];
    let large_numbers: vector<u64> = vector[1000000, 2000000, 3000000];
    
    // Consider storage costs for large vectors
    // Each vector element in global storage uses a storage slot
}
```

## Common Type Patterns

### Error Handling with Types

```move
enum Result<T> {
    Ok(T),
    Err(String),
}

public fun safe_divide(a: u64, b: u64): Result<u64> {
    if (b == 0) {
        return Result::Err(string::utf8(b"Division by zero"))
    };
    Result::Ok(a / b)
}
```

### Option Type Pattern

```move
enum Option<T> {
    Some(T),
    None,
}

public fun find_element(numbers: vector<u64>, target: u64): Option<u64> {
    let i = 0;
    let len = vector::length(&numbers);
    
    while (i < len) {
        let current = *vector::borrow(&numbers, i);
        if (current == target) {
            return Option::Some(current)
        };
        i = i + 1;
    };
    
    Option::None
}
```

Understanding these data types and their characteristics is essential for writing efficient and correct Move code. The type system helps prevent errors and makes code more maintainable and readable.
