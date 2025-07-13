# Transfer and Borrowing

Understanding how to transfer ownership and borrow values is essential for writing efficient Move code. This section covers the mechanics of ownership transfer and the borrowing system that allows controlled access to values without transferring ownership.

## Ownership Transfer

Ownership transfer occurs when a value is moved from one owner to another. This is the default behavior in Move for most types.

### Basic Ownership Transfer

```move
module my_module::basic_transfer {
    public fun basic_transfer_demo() {
        let s1 = string::utf8(b"hello");
        let s2 = s1;  // Ownership transferred from s1 to s2
        
        // s1 is no longer valid
        // s2 is now the owner
        
        let len = string::length(&s2);
    } // s2 goes out of scope and is dropped
}
```

### Transfer in Function Calls

```move
module my_module::function_transfer {
    public fun function_transfer_demo() {
        let s = string::utf8(b"hello");
        
        // Ownership transferred to the function
        takes_ownership(s);
        
        // s is no longer valid here
        // This would cause a compilation error:
        // let len = string::length(&s);
    }
    
    fun takes_ownership(some_string: String) {
        // some_string is now owned by this function
        let len = string::length(&some_string);
    } // some_string goes out of scope and is dropped
}
```

### Transfer with Return Values

```move
module my_module::return_transfer {
    public fun return_transfer_demo() {
        let s1 = gives_ownership();  // Ownership transferred from function to s1
        
        let s2 = string::utf8(b"world");
        let s3 = takes_and_gives_back(s2);  // s2 moved in, s3 moved out
    }
    
    fun gives_ownership() -> String {
        let some_string = string::utf8(b"hello");
        some_string  // Ownership transferred to caller
    }
    
    fun takes_and_gives_back(a_string: String) -> String {
        // a_string comes into scope
        a_string  // Ownership transferred back to caller
    }
}
```

### Transfer with Structs

```move
module my_module::struct_transfer {
    struct Person has drop, store {
        name: String,
        age: u8,
    }
    
    public fun struct_transfer_demo() {
        let person1 = Person {
            name: string::utf8(b"Alice"),
            age: 30,
        };
        
        let person2 = person1;  // Ownership transferred
        
        // person1 is no longer valid
        // person2 is now the owner
        
        let age = person2.age;
    }
}
```

## Borrowing

Borrowing allows you to use a value without taking ownership of it. Borrowing is done using references (`&` for immutable references, `&mut` for mutable references).

### Immutable Borrowing

```move
module my_module::immutable_borrowing {
    public fun immutable_borrow_demo() {
        let s = string::utf8(b"hello");
        
        // Borrow s immutably
        let len = calculate_length(&s);
        let is_empty = string::is_empty(&s);
        
        // s is still valid and can be used
        let first_char = string::sub_string(&s, 0, 1);
    }
    
    fun calculate_length(s: &String) -> u64 {
        string::length(s)  // Can read but not modify
    }
}
```

### Mutable Borrowing

```move
module my_module::mutable_borrowing {
    public fun mutable_borrow_demo() {
        let mut s = string::utf8(b"hello");
        
        // Borrow s mutably
        change_string(&mut s);
        
        // s is still valid and has been modified
        let len = string::length(&s);
    }
    
    fun change_string(s: &mut String) {
        *s = *s + string::utf8(b" world");  // Can modify the value
    }
}
```

### Multiple Immutable Borrows

```move
module my_module::multiple_immutable_borrows {
    public fun multiple_immutable_demo() {
        let s = string::utf8(b"hello");
        
        // Multiple immutable borrows are allowed
        let len1 = string::length(&s);
        let len2 = string::length(&s);
        let is_empty = string::is_empty(&s);
        
        // All borrows can be used simultaneously
        let result = len1 + len2;
    }
}
```

### Mutable and Immutable Borrows

```move
module my_module::mutable_immutable_conflict {
    public fun conflict_demo() {
        let mut s = string::utf8(b"hello");
        
        let len = string::length(&s);  // Immutable borrow
        
        // This would cause a compilation error:
        // change_string(&mut s);  // Mutable borrow while immutable borrow exists
        
        // But this is fine:
        let is_empty = string::is_empty(&s);  // Another immutable borrow
    }
    
    fun change_string(s: &mut String) {
        *s = *s + string::utf8(b" world");
    }
}
```

## Borrowing Rules

Move enforces strict borrowing rules to prevent data races and ensure memory safety:

1. **At any given time, you can have either one mutable reference or any number of immutable references to a particular value**
2. **References must always be valid**

### Borrowing Rule Examples

```move
module my_module::borrowing_rules {
    public fun borrowing_rules_demo() {
        let mut s = string::utf8(b"hello");
        
        // Rule 1: Multiple immutable borrows allowed
        let r1 = &s;
        let r2 = &s;
        let r3 = &s;
        
        // All immutable borrows can be used
        let len1 = string::length(r1);
        let len2 = string::length(r2);
        let len3 = string::length(r3);
        
        // Rule 2: Cannot have mutable borrow while immutable borrows exist
        // This would cause a compilation error:
        // let r4 = &mut s;
        
        // Rule 3: Cannot have multiple mutable borrows
        // let r5 = &mut s;
        // let r6 = &mut s;  // This would cause a compilation error
    }
}
```

## Dangling References

Move prevents dangling references (references to data that no longer exists):

```move
module my_module::dangling_references {
    // This would cause a compilation error - dangling reference
    // fun dangle() -> &String {
    //     let s = string::utf8(b"hello");
    //     &s  // s goes out of scope, so this reference would be invalid
    // }
    
    // Instead, return the value itself
    fun no_dangle() -> String {
        let s = string::utf8(b"hello");
        s  // Ownership transferred to caller
    }
}
```

## Borrowing in Structs

Structs can contain references, but they must follow the borrowing rules:

```move
module my_module::struct_borrowing {
    struct StringWrapper has drop, store {
        content: String,
    }
    
    public fun struct_borrow_demo() {
        let wrapper = StringWrapper {
            content: string::utf8(b"hello"),
        };
        
        // Borrow the struct immutably
        let len = get_length(&wrapper);
        
        // Borrow the struct mutably
        append_world(&mut wrapper);
        
        // Both operations work on the same struct
        let final_len = string::length(&wrapper.content);
    }
    
    fun get_length(wrapper: &StringWrapper) -> u64 {
        string::length(&wrapper.content)
    }
    
    fun append_world(wrapper: &mut StringWrapper) {
        wrapper.content = wrapper.content + string::utf8(b" world");
    }
}
```

## Borrowing with Collections

Borrowing works with collections like vectors:

```move
module my_module::collection_borrowing {
    public fun vector_borrow_demo() {
        let mut numbers = vector[1, 2, 3, 4, 5];
        
        // Immutable borrow
        let sum = calculate_sum(&numbers);
        
        // Mutable borrow
        double_values(&mut numbers);
        
        // Both operations work on the same vector
        let new_sum = calculate_sum(&numbers);
    }
    
    fun calculate_sum(numbers: &vector<u64>) -> u64 {
        let sum = 0u64;
        let i = 0;
        let len = vector::length(numbers);
        
        while (i < len) {
            sum = sum + *vector::borrow(numbers, i);
            i = i + 1;
        };
        
        sum
    }
    
    fun double_values(numbers: &mut vector<u64>) {
        let i = 0;
        let len = vector::length(numbers);
        
        while (i < len) {
            let value = *vector::borrow(numbers, i);
            *vector::borrow_mut(numbers, i) = value * 2;
            i = i + 1;
        };
    }
}
```

## Borrowing in Global Storage

Borrowing is essential for working with global storage:

```move
module my_module::global_storage_borrowing {
    struct Counter has key, store {
        value: u64,
    }
    
    public fun global_borrow_demo(account: &signer) {
        let counter = Counter { value: 0 };
        move_to(account, counter);
        
        let addr = signer::address_of(account);
        
        // Immutable borrow from global storage
        let current_value = get_counter_value(addr);
        
        // Mutable borrow from global storage
        increment_counter(addr);
        
        // Verify the change
        let new_value = get_counter_value(addr);
    }
    
    fun get_counter_value(addr: address) -> u64 {
        let counter = borrow_global<Counter>(addr);
        counter.value
    }
    
    fun increment_counter(addr: address) {
        let counter = borrow_global_mut<Counter>(addr);
        counter.value = counter.value + 1;
    }
}
```

## Borrowing Patterns

### Read-Only Operations

```move
module my_module::read_only_pattern {
    public fun read_only_demo(data: &vector<u64>) -> (u64, u64, bool) {
        let sum = calculate_sum(data);
        let average = calculate_average(data);
        let is_empty = vector::is_empty(data);
        (sum, average, is_empty)
    }
    
    fun calculate_sum(data: &vector<u64>) -> u64 {
        let sum = 0u64;
        let i = 0;
        let len = vector::length(data);
        
        while (i < len) {
            sum = sum + *vector::borrow(data, i);
            i = i + 1;
        };
        
        sum
    }
    
    fun calculate_average(data: &vector<u64>) -> u64 {
        let sum = calculate_sum(data);
        let len = vector::length(data);
        if (len == 0) {
            0
        } else {
            sum / len
        }
    }
}
```

### Modification Operations

```move
module my_module::modification_pattern {
    public fun modification_demo(data: &mut vector<u64>) {
        // Sort the data
        sort_vector(data);
        
        // Remove duplicates
        remove_duplicates(data);
        
        // Double all values
        double_all(data);
    }
    
    fun sort_vector(data: &mut vector<u64>) {
        // Implementation of sorting
        // This is a simplified example
    }
    
    fun remove_duplicates(data: &mut vector<u64>) {
        // Implementation of duplicate removal
        // This is a simplified example
    }
    
    fun double_all(data: &mut vector<u64>) {
        let i = 0;
        let len = vector::length(data);
        
        while (i < len) {
            let value = *vector::borrow(data, i);
            *vector::borrow_mut(data, i) = value * 2;
            i = i + 1;
        };
    }
}
```

## Best Practices

### Prefer Borrowing Over Transfer

```move
module my_module::borrowing_best_practices {
    // Good: Use borrowing for read-only access
    public fun efficient_processing(data: &vector<u64>) -> u64 {
        let sum = 0u64;
        let i = 0;
        let len = vector::length(data);
        
        while (i < len) {
            sum = sum + *vector::borrow(data, i);
            i = i + 1;
        };
        
        sum
    }
    
    // Less efficient: Transfer ownership
    // public fun inefficient_processing(data: vector<u64>) -> (vector<u64>, u64) {
    //     let sum = calculate_sum(&data);
    //     (data, sum)  // Must return data to avoid moving
    // }
}
```

### Use Appropriate Reference Types

```move
module my_module::reference_types {
    // Use immutable references for read-only access
    public fun read_operations(data: &String) -> (u64, bool) {
        let length = string::length(data);
        let is_empty = string::is_empty(data);
        (length, is_empty)
    }
    
    // Use mutable references only when modification is needed
    public fun modification_operations(data: &mut String) {
        *data = *data + string::utf8(b" modified");
    }
}
```

### Avoid Borrowing Conflicts

```move
module my_module::avoid_conflicts {
    public fun avoid_conflict_demo() {
        let mut data = vector[1, 2, 3, 4, 5];
        
        // Good: Use immutable borrows first
        let sum = calculate_sum(&data);
        let average = calculate_average(&data);
        
        // Then use mutable borrow
        modify_data(&mut data);
        
        // Now can use immutable borrows again
        let new_sum = calculate_sum(&data);
    }
    
    fun calculate_sum(data: &vector<u64>) -> u64 {
        // Implementation
        0
    }
    
    fun calculate_average(data: &vector<u64>) -> u64 {
        // Implementation
        0
    }
    
    fun modify_data(data: &mut vector<u64>) {
        // Implementation
    }
}
```

Understanding ownership transfer and borrowing is fundamental to writing safe and efficient Move code. The borrowing system provides a powerful way to control access to data while maintaining Move's safety guarantees.
