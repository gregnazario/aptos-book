# Vectors

Vectors are ordered sequences of elements in Move. They are one of the most fundamental collection types and are used extensively throughout Move programs.

## Available Vector Types

### Standard Vector (`std::vector`)
The basic vector type from the Move standard library.

```move
use std::vector;

// Create an empty vector
let empty_vec: vector<u64> = vector::empty<u64>();

// Create a vector with initial elements
let numbers: vector<u64> = vector[1, 2, 3, 4, 5];

// Create a vector of strings
let strings: vector<String> = vector[
    string::utf8(b"hello"),
    string::utf8(b"world")
];
```

### BigVector (`aptos_std::big_vector`)
A specialized vector implementation for large datasets that uses table storage internally.

```move
use aptos_std::big_vector::{Self, BigVector};

// Create a BigVector
let big_vec = big_vector::new<u64>();

// Add elements
big_vector::push_back(&mut big_vec, 1);
big_vector::push_back(&mut big_vec, 2);
```

## How to Use Vectors

### Basic Operations

```move
module my_module::vector_example {
    use std::vector;
    use std::string::{Self, String};

    public fun create_and_manipulate_vector(): vector<u64> {
        // Create an empty vector
        let v = vector::empty<u64>();
        
        // Add elements
        vector::push_back(&mut v, 1);
        vector::push_back(&mut v, 2);
        vector::push_back(&mut v, 3);
        
        // Get length
        let len = vector::length(&v);
        
        // Access element by index
        let first = *vector::borrow(&v, 0);
        let last = *vector::borrow(&v, len - 1);
        
        // Remove and return last element
        let popped = vector::pop_back(&mut v);
        
        v
    }

    public fun vector_operations(): vector<String> {
        let v = vector::empty<String>();
        
        // Add strings
        vector::push_back(&mut v, string::utf8(b"hello"));
        vector::push_back(&mut v, string::utf8(b"world"));
        
        // Check if empty
        let is_empty = vector::is_empty(&v);
        
        // Get capacity (if available)
        let capacity = vector::length(&v);
        
        v
    }
}
```

### Iterating Over Vectors

```move
public fun sum_vector(v: &vector<u64>): u64 {
    let sum = 0u64;
    let i = 0;
    let len = vector::length(v);
    
    while (i < len) {
        sum = sum + *vector::borrow(v, i);
        i = i + 1;
    };
    
    sum
}

// Using for loop (Move 2024+)
public fun sum_vector_for(v: &vector<u64>): u64 {
    let sum = 0u64;
    for (element in v) {
        sum = sum + *element;
    };
    sum
}
```

### Vector Manipulation

```move
public fun vector_manipulation(): vector<u64> {
    let v = vector[1, 2, 3, 4, 5];
    
    // Insert at specific index
    vector::insert(&mut v, 2, 10);
    // Result: [1, 2, 10, 3, 4, 5]
    
    // Remove element at index
    let removed = vector::remove(&mut v, 1);
    // Result: [1, 10, 3, 4, 5], removed = 2
    
    // Swap elements
    vector::swap(&mut v, 0, 2);
    // Result: [3, 10, 1, 4, 5]
    
    // Reverse the vector
    vector::reverse(&mut v);
    // Result: [5, 4, 1, 10, 3]
    
    v
}
```

## Vector Abilities and Constraints

Vectors have specific abilities that determine how they can be used:

```move
// Vector has copy, drop, and store abilities
struct VectorHolder has key, store {
    data: vector<u64>
}

// Vectors can be stored in global storage
public fun store_vector(account: &signer) {
    let v = vector[1, 2, 3];
    move_to(account, VectorHolder { data: v });
}

// Vectors can be copied and dropped
public fun vector_abilities() {
    let v1 = vector[1, 2, 3];
    let v2 = v1; // Copy
    // v1 is still available due to copy ability
    
    // Both v1 and v2 are automatically dropped at end of function
}
```

## Tradeoffs

### Advantages of Standard Vectors
- **Simple and familiar** - Easy to understand and use
- **Efficient for small datasets** - Good performance for collections with < 1000 elements
- **Flexible** - Supports all basic operations (push, pop, insert, remove, etc.)
- **Memory efficient** - Compact storage for small collections
- **BCS serializable** - Can be easily serialized and deserialized

### Disadvantages of Standard Vectors
- **Limited scalability** - Performance degrades with large datasets
- **Single storage slot** - All elements stored in one storage slot
- **No parallelization** - Operations cannot be parallelized
- **Memory constraints** - Limited by single storage slot size
- **Expensive operations** - Insert/remove operations are O(n)

### When to Use BigVector
- **Large datasets** - When you need to store thousands of elements
- **Frequent additions** - When you frequently add elements
- **Table-based storage** - When you want table storage benefits
- **Scalability requirements** - When you need to scale to large collections

### When to Use Standard Vector
- **Small datasets** - Collections with < 1000 elements
- **Simple use cases** - When you need basic sequential storage
- **Memory efficiency** - When storage space is a concern
- **BCS serialization** - When you need to serialize the data

## Performance Characteristics

| Operation | Standard Vector | BigVector |
|-----------|----------------|-----------|
| Push back | O(1) amortized | O(1) |
| Pop back | O(1) | O(1) |
| Access by index | O(1) | O(1) |
| Insert at index | O(n) | O(n) |
| Remove at index | O(n) | O(n) |
| Storage cost | Single slot | Multiple slots |
| Parallelization | No | Yes (for table operations) |

## Best Practices

1. **Choose the right type**: Use standard vectors for small collections, BigVector for large ones
2. **Prefer push_back/pop_back**: These are the most efficient operations
3. **Avoid frequent insert/remove**: These operations are expensive
4. **Use references when possible**: Borrow elements instead of copying when you only need to read
5. **Consider storage costs**: Vectors stored in global storage consume storage slots
6. **Plan for growth**: If your collection might grow large, consider BigVector from the start
