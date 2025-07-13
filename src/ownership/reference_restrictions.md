# Reference Restrictions

Move's reference system includes strict restrictions that prevent common programming errors like data races, dangling references, and use-after-free bugs. Understanding these restrictions is crucial for writing safe Move code.

## The Borrowing Rules

Move enforces three fundamental borrowing rules that must be followed at all times:

1. **At any given time, you can have either one mutable reference or any number of immutable references to a particular value**
2. **References must always be valid**
3. **References cannot outlive the data they refer to**

## Rule 1: Mutable vs Immutable References

This rule prevents data races by ensuring that data cannot be modified while it's being read.

### Multiple Immutable References Allowed

```move
module my_module::multiple_immutable {
    public fun multiple_immutable_demo() {
        let s = string::utf8(b"hello");
        
        // Multiple immutable references are allowed
        let r1 = &s;
        let r2 = &s;
        let r3 = &s;
        
        // All can be used simultaneously
        let len1 = string::length(r1);
        let len2 = string::length(r2);
        let len3 = string::length(r3);
        
        // This is safe because no one can modify the data
        let total = len1 + len2 + len3;
    }
}
```

### Only One Mutable Reference

```move
module my_module::single_mutable {
    public fun single_mutable_demo() {
        let mut s = string::utf8(b"hello");
        
        // Only one mutable reference allowed
        let r1 = &mut s;
        
        // This would cause a compilation error:
        // let r2 = &mut s;  // Second mutable reference
        
        // Use the mutable reference
        *r1 = *r1 + string::utf8(b" world");
    }
}
```

### Mutable and Immutable Reference Conflict

```move
module my_module::mutable_immutable_conflict {
    public fun conflict_demo() {
        let mut s = string::utf8(b"hello");
        
        // Create immutable reference
        let r1 = &s;
        let len = string::length(r1);
        
        // This would cause a compilation error:
        // let r2 = &mut s;  // Mutable reference while immutable exists
        
        // But this is fine - another immutable reference
        let r3 = &s;
        let is_empty = string::is_empty(r3);
    }
}
```

## Rule 2: References Must Always Be Valid

Move prevents dangling references by ensuring references always point to valid data.

### Preventing Dangling References

```move
module my_module::dangling_prevention {
    // This would cause a compilation error - dangling reference
    // fun dangle() -> &String {
    //     let s = string::utf8(b"hello");
    //     &s  // s goes out of scope, making this reference invalid
    // }
    
    // Instead, return the value itself
    fun no_dangle() -> String {
        let s = string::utf8(b"hello");
        s  // Ownership transferred to caller
    }
    
    // Or return a reference to data that lives long enough
    struct StringHolder has key, store {
        content: String,
    }
    
    fun get_reference(holder: &StringHolder) -> &String {
        &holder.content  // Reference to data that outlives the function
    }
}
```

### Reference Lifetime in Structs

```move
module my_module::struct_lifetime {
    // This would cause a compilation error - reference in struct
    // struct StringRef {
    //     content: &String,  // Reference without lifetime
    // }
    
    // Instead, store the value itself
    struct StringWrapper has drop, store {
        content: String,
    }
    
    // Or use a different design pattern
    struct StringHolder has key, store {
        content: String,
    }
    
    fun create_wrapper(s: String) -> StringWrapper {
        StringWrapper { content: s }
    }
}
```

## Rule 3: References Cannot Outlive Data

This rule ensures that references are always valid throughout their lifetime.

### Scope and Lifetime

```move
module my_module::scope_lifetime {
    public fun scope_demo() {
        let mut s = string::utf8(b"hello");
        
        {
            let r = &mut s;  // Mutable reference to s
            *r = *r + string::utf8(b" world");
        } // r goes out of scope here
        
        // s is still valid and can be used
        let len = string::length(&s);
    }
}
```

### Function Parameter Lifetimes

```move
module my_module::function_lifetime {
    public fun function_demo() {
        let s = string::utf8(b"hello");
        
        // Pass reference to function
        let len = calculate_length(&s);
        
        // s is still valid after the function call
        let is_empty = string::is_empty(&s);
    }
    
    fun calculate_length(s: &String) -> u64 {
        string::length(s)  // Reference is valid for the duration of the function
    }
}
```

## Reference Restrictions in Practice

### Working with Collections

```move
module my_module::collection_restrictions {
    public fun vector_restrictions() {
        let mut numbers = vector[1, 2, 3, 4, 5];
        
        // Immutable borrow
        let sum = calculate_sum(&numbers);
        
        // Mutable borrow
        double_values(&mut numbers);
        
        // Can use immutable borrow again after mutable borrow ends
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

### Global Storage Restrictions

```move
module my_module::global_storage_restrictions {
    struct Counter has key, store {
        value: u64,
    }
    
    public fun global_storage_demo(account: &signer) {
        let counter = Counter { value: 0 };
        move_to(account, counter);
        
        let addr = signer::address_of(account);
        
        // Immutable borrow from global storage
        let current_value = get_counter_value(addr);
        
        // Mutable borrow from global storage
        increment_counter(addr);
        
        // Can use immutable borrow again
        let new_value = get_counter_value(addr);
    }
    
    fun get_counter_value(addr: address) -> u64 {
        let counter = borrow_global<Counter>(addr);
        counter.value  // Return copy of value, not reference
    }
    
    fun increment_counter(addr: address) {
        let counter = borrow_global_mut<Counter>(addr);
        counter.value = counter.value + 1;
    }
}
```

## Common Reference Errors and Solutions

### Error: Multiple Mutable References

```move
module my_module::multiple_mutable_error {
    public fun multiple_mutable_error() {
        let mut s = string::utf8(b"hello");
        
        // This would cause a compilation error:
        // let r1 = &mut s;
        // let r2 = &mut s;  // Second mutable reference
        
        // Solution: Use one mutable reference at a time
        {
            let r1 = &mut s;
            *r1 = *r1 + string::utf8(b" world");
        } // r1 goes out of scope
        
        {
            let r2 = &mut s;
            *r2 = *r2 + string::utf8(b"!");
        } // r2 goes out of scope
    }
}
```

### Error: Mutable and Immutable Reference Conflict

```move
module my_module::conflict_error {
    public fun conflict_error() {
        let mut s = string::utf8(b"hello");
        
        // This would cause a compilation error:
        // let r1 = &s;  // Immutable reference
        // let r2 = &mut s;  // Mutable reference while immutable exists
        
        // Solution: Use immutable references first, then mutable
        let len = string::length(&s);
        let is_empty = string::is_empty(&s);
        
        // Now use mutable reference
        let r2 = &mut s;
        *r2 = *r2 + string::utf8(b" world");
    }
}
```

### Error: Dangling Reference

```move
module my_module::dangling_error {
    // This would cause a compilation error:
    // fun dangling_reference() -> &String {
    //     let s = string::utf8(b"hello");
    //     &s  // s goes out of scope, making reference invalid
    // }
    
    // Solution: Return the value itself
    fun return_value() -> String {
        let s = string::utf8(b"hello");
        s  // Ownership transferred
    }
    
    // Or use a different design pattern
    struct StringHolder has key, store {
        content: String,
    }
    
    fun return_reference_to_stored_data(addr: address) -> &String {
        let holder = borrow_global<StringHolder>(addr);
        &holder.content  // Reference to data that lives in global storage
    }
}
```

## Reference Restrictions and Performance

### Avoiding Unnecessary Copies

```move
module my_module::performance_restrictions {
    // Good: Use references to avoid copying
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
    
    // Less efficient: Copy the entire vector
    // public fun inefficient_processing(data: vector<u64>) -> u64 {
    //     // data is moved into the function
    //     // processing happens
    //     // data would need to be returned if needed elsewhere
    // }
}
```

### Minimizing Borrowing Conflicts

```move
module my_module::minimize_conflicts {
    public fun minimize_conflicts_demo() {
        let mut data = vector[1, 2, 3, 4, 5];
        
        // Group immutable operations together
        let sum = calculate_sum(&data);
        let average = calculate_average(&data);
        let max = find_max(&data);
        
        // Then do mutable operations
        modify_data(&mut data);
        
        // Can use immutable operations again
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
    
    fun find_max(data: &vector<u64>) -> u64 {
        // Implementation
        0
    }
    
    fun modify_data(data: &mut vector<u64>) {
        // Implementation
    }
}
```

## Best Practices for Reference Restrictions

### Plan Your Borrowing Strategy

```move
module my_module::borrowing_strategy {
    public fun borrowing_strategy_demo() {
        let mut data = vector[1, 2, 3, 4, 5];
        
        // Strategy 1: Read-only operations first
        let analysis = analyze_data(&data);
        
        // Strategy 2: Single mutable operation
        modify_data(&mut data);
        
        // Strategy 3: Read-only operations after modification
        let new_analysis = analyze_data(&data);
    }
    
    fun analyze_data(data: &vector<u64>) -> (u64, u64, u64) {
        let sum = calculate_sum(data);
        let average = calculate_average(data);
        let max = find_max(data);
        (sum, average, max)
    }
    
    fun modify_data(data: &mut vector<u64>) {
        // Single modification operation
        double_all_values(data);
    }
    
    fun calculate_sum(data: &vector<u64>) -> u64 {
        // Implementation
        0
    }
    
    fun calculate_average(data: &vector<u64>) -> u64 {
        // Implementation
        0
    }
    
    fun find_max(data: &vector<u64>) -> u64 {
        // Implementation
        0
    }
    
    fun double_all_values(data: &mut vector<u64>) {
        // Implementation
    }
}
```

### Use Appropriate Reference Types

```move
module my_module::appropriate_references {
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
    
    // Avoid unnecessary mutable references
    // public fun unnecessary_mutable(data: &mut String) -> u64 {
    //     string::length(data)  // Doesn't need mutable reference
    // }
}
```

### Handle Borrowing Conflicts Gracefully

```move
module my_module::graceful_conflicts {
    public fun graceful_conflict_demo() {
        let mut data = vector[1, 2, 3, 4, 5];
        
        // Extract values before modification to avoid conflicts
        let current_sum = calculate_sum(&data);
        let current_average = calculate_average(&data);
        
        // Now modify the data
        modify_data(&mut data);
        
        // Use the extracted values
        let new_sum = calculate_sum(&data);
        let sum_difference = new_sum - current_sum;
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

Understanding and following Move's reference restrictions is essential for writing safe and correct code. These restrictions prevent common programming errors and ensure that your Move programs are memory-safe and free from data races.
