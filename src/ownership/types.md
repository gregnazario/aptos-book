# Move Types and Ownership

Understanding how different Move types interact with ownership is crucial for writing correct and efficient code. This section explores how various types behave with respect to ownership, copying, and moving.

## Type Abilities and Ownership

Move's type system is built around abilities that determine how types can be used. These abilities directly affect ownership behavior:

- **`copy`**: The type can be duplicated
- **`drop`**: The type can be destroyed
- **`store`**: The type can be stored in global storage
- **`key`**: The type can be used as a key in global storage

## Primitive Types

Primitive types in Move have simple ownership behavior because they are stored on the stack and have known sizes.

### Integer Types

All integer types (`u8`, `u16`, `u32`, `u64`, `u128`, `u256`) have the `copy` and `drop` abilities:

```move
module my_module::integer_ownership {
    public fun integer_demo() {
        let x: u64 = 42;
        let y = x;  // Copy - x is still valid
        
        // Both x and y are valid
        let sum = x + y;
        
        // Both are automatically dropped at end of function
    }
}
```

### Boolean Type

The `bool` type has `copy` and `drop` abilities:

```move
module my_module::boolean_ownership {
    public fun boolean_demo() {
        let flag = true;
        let flag_copy = flag;  // Copy
        
        // Both flags are valid
        let result = flag && flag_copy;
    }
}
```

### Address Type

The `address` type has `copy` and `drop` abilities:

```move
module my_module::address_ownership {
    public fun address_demo() {
        let addr1 = @0x1;
        let addr2 = addr1;  // Copy
        
        // Both addresses are valid
        let is_equal = addr1 == addr2;
    }
}
```

## Vector Type

The `vector` type has `copy`, `drop`, and `store` abilities, but its behavior depends on the element type:

```move
module my_module::vector_ownership {
    public fun vector_demo() {
        // Vector of copyable types
        let numbers = vector[1, 2, 3, 4, 5];
        let numbers_copy = numbers;  // Copy - both are valid
        
        // Vector of non-copyable types (like String)
        let strings = vector[
            string::utf8(b"hello"),
            string::utf8(b"world")
        ];
        let strings_moved = strings;  // Move - strings is no longer valid
        
        // This would cause a compilation error:
        // let len = vector::length(&strings);
    }
}
```

## String Type

The `String` type has `copy`, `drop`, and `store` abilities, but copying can be expensive:

```move
module my_module::string_ownership {
    public fun string_demo() {
        let s1 = string::utf8(b"hello");
        let s2 = s1;  // Move - s1 is no longer valid
        
        // This would cause a compilation error:
        // let len = string::length(&s1);
        
        // s2 is still valid
        let len = string::length(&s2);
    }
    
    public fun string_copy_demo() {
        let s1 = string::utf8(b"hello");
        let s2 = string::clone(&s1);  // Explicit copy - both are valid
        
        // Both strings are valid
        let len1 = string::length(&s1);
        let len2 = string::length(&s2);
    }
}
```

## Struct Types

Struct ownership behavior depends on the abilities declared for the struct:

### Copyable Structs

```move
module my_module::copyable_struct {
    struct Point has copy, drop, store {
        x: u64,
        y: u64,
    }
    
    public fun copyable_demo() {
        let p1 = Point { x: 10, y: 20 };
        let p2 = p1;  // Copy - p1 is still valid
        
        // Both points are valid
        let sum_x = p1.x + p2.x;
        let sum_y = p1.y + p2.y;
    }
}
```

### Non-Copyable Structs

```move
module my_module::non_copyable_struct {
    struct Message has drop, store {
        content: String,
        timestamp: u64,
    }
    
    public fun non_copyable_demo() {
        let msg1 = Message {
            content: string::utf8(b"Hello"),
            timestamp: 1234567890,
        };
        let msg2 = msg1;  // Move - msg1 is no longer valid
        
        // This would cause a compilation error:
        // let content = msg1.content;
        
        // msg2 is still valid
        let content = msg2.content;
    }
}
```

### Resource Structs

Resources are special structs that cannot be copied or dropped:

```move
module my_module::resource_struct {
    struct Coin has key, store {
        value: u64,
    }
    
    public fun resource_demo() {
        let coin = Coin { value: 100 };
        
        // Resources cannot be copied
        // let coin_copy = coin;  // This would cause a compilation error
        
        // Resources cannot be dropped automatically
        // They must be explicitly moved to global storage or returned
        
        // Move to global storage
        // move_to(account, coin);
        
        // Or return the resource
        coin
    }
}
```

## Tuple Types

Tuple ownership behavior depends on the types of its elements:

```move
module my_module::tuple_ownership {
    public fun tuple_demo() {
        // Tuple with all copyable elements
        let t1 = (42, true, @0x1);
        let t2 = t1;  // Copy - t1 is still valid
        
        // Tuple with non-copyable elements
        let t3 = (string::utf8(b"hello"), 42);
        let t4 = t3;  // Move - t3 is no longer valid
        
        // This would cause a compilation error:
        // let (s, n) = t3;
        
        // t4 is still valid
        let (s, n) = t4;
    }
}
```

## Reference Types

References provide controlled access to values without transferring ownership:

### Immutable References

```move
module my_module::immutable_references {
    public fun immutable_ref_demo() {
        let s = string::utf8(b"hello");
        let len = calculate_length(&s);  // Pass immutable reference
        
        // s is still valid
        let is_empty = string::is_empty(&s);
    }
    
    fun calculate_length(s: &String): u64 {
        string::length(s)  // Can read but not modify
    }
}
```

### Mutable References

```move
module my_module::mutable_references {
    public fun mutable_ref_demo() {
        let mut s = string::utf8(b"hello");
        append_world(&mut s);  // Pass mutable reference
        
        // s is still valid and has been modified
        let len = string::length(&s);
    }
    
    fun append_world(s: &mut String) {
        *s = *s + string::utf8(b" world");  // Can modify the value
    }
}
```

## Global Storage and Ownership

Global storage in Move has special ownership rules:

### Storing Resources

```move
module my_module::global_storage {
    struct UserProfile has key, store {
        name: String,
        age: u8,
    }
    
    public fun store_profile(account: &signer, name: String, age: u8) {
        let profile = UserProfile { name, age };
        move_to(account, profile);  // Transfer ownership to global storage
    }
    
    public fun get_profile_name(addr: address): String {
        let profile = borrow_global<UserProfile>(addr);
        profile.name  // Return a copy of the name
    }
    
    public fun update_profile_age(addr: address, new_age: u8) {
        let profile = borrow_global_mut<UserProfile>(addr);
        profile.age = new_age;  // Modify the stored value
    }
}
```

### Moving Resources Out of Storage

```move
module my_module::move_from_storage {
    struct Coin has key, store {
        value: u64,
    }
    
    public fun withdraw_coin(account: &signer, amount: u64): Coin {
        let coin = move_from<Coin>(signer::address_of(account));
        
        // Split the coin if needed
        if (coin.value > amount) {
            let (withdrawn, remaining) = split_coin(coin, amount);
            // Return the remaining coin to storage
            move_to(account, remaining);
            withdrawn
        } else {
            coin
        }
    }
    
    fun split_coin(coin: Coin, amount: u64): (Coin, Coin) {
        // Implementation of coin splitting
        // This is a simplified example
        (Coin { value: amount }, Coin { value: coin.value - amount })
    }
}
```

## Type Abilities and Constraints

Understanding abilities helps you design types with the right ownership behavior:

### Designing Copyable Types

```move
module my_module::copyable_design {
    // Good: All fields are copyable
    struct Config has copy, drop, store {
        max_retries: u8,
        timeout: u64,
        enabled: bool,
    }
    
    // Bad: Contains non-copyable field
    // struct BadConfig has copy, drop, store {
    //     max_retries: u8,
    //     name: String,  // String doesn't have copy ability
    // }
}
```

### Designing Resource Types

```move
module my_module::resource_design {
    // Good: Resource with key and store abilities
    struct Token has key, store {
        id: u64,
        owner: address,
        metadata: String,
    }
    
    // Bad: Resource with copy ability (contradiction)
    // struct BadToken has key, store, copy {
    //     id: u64,
    //     owner: address,
    // }
}
```

## Ownership Patterns

### Value Semantics

```move
module my_module::value_semantics {
    struct Point has copy, drop, store {
        x: u64,
        y: u64,
    }
    
    public fun value_demo() {
        let p1 = Point { x: 10, y: 20 };
        let p2 = p1;  // Copy - value semantics
        
        // Modifying p2 doesn't affect p1
        p2.x = 30;
        
        // p1.x is still 10
        let x1 = p1.x;
        let x2 = p2.x;  // 30
    }
}
```

### Reference Semantics

```move
module my_module::reference_semantics {
    struct Counter has key, store {
        value: u64,
    }
    
    public fun reference_demo(account: &signer) {
        let counter = Counter { value: 0 };
        move_to(account, counter);
        
        // All operations work on the same instance
        increment_counter(signer::address_of(account));
        increment_counter(signer::address_of(account));
        
        let final_value = get_counter_value(signer::address_of(account));
        // final_value is 2
    }
    
    fun increment_counter(addr: address) {
        let counter = borrow_global_mut<Counter>(addr);
        counter.value = counter.value + 1;
    }
    
    fun get_counter_value(addr: address): u64 {
        let counter = borrow_global<Counter>(addr);
        counter.value
    }
}
```

## Best Practices

### Choose Appropriate Abilities

```move
module my_module::ability_best_practices {
    // Use copy for small, simple data
    struct SmallData has copy, drop, store {
        id: u64,
        flag: bool,
    }
    
    // Use drop for temporary data
    struct TempData has drop {
        buffer: vector<u8>,
    }
    
    // Use store for data that needs persistence
    struct PersistentData has key, store {
        data: String,
    }
    
    // Use key for resources
    struct Resource has key, store {
        value: u64,
    }
}
```

### Avoid Unnecessary Copies

```move
module my_module::avoid_copies {
    public fun efficient_processing(data: &vector<u64>): u64 {
        let sum = 0u64;
        let i = 0;
        let len = vector::length(data);
        
        while (i < len) {
            sum = sum + *vector::borrow(data, i);
            i = i + 1;
        };
        
        sum
    }
    
    // Less efficient - creates unnecessary copies
    // public fun inefficient_processing(data: vector<u64>): u64 {
    //     // data is moved into the function
    //     // and would need to be returned if needed elsewhere
    // }
}
```

### Use References for Read-Only Access

```move
module my_module::reference_best_practices {
    public fun read_only_operations(data: &String): (u64, bool) {
        let length = string::length(data);
        let is_empty = string::is_empty(data);
        (length, is_empty)
    }
    
    public fun modify_data(data: &mut String) {
        *data = *data + string::utf8(b" modified");
    }
}
```

Understanding how different types interact with ownership is essential for writing efficient and correct Move code. The ability system provides a clear way to express ownership semantics, and following best practices helps you avoid common pitfalls.
