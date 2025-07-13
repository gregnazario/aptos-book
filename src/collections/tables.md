# Tables

Tables are hash-addressable storage structures designed for large-scale data storage on Aptos. They provide efficient storage and retrieval of data using unique keys, with each table entry stored in its own storage slot for better performance and parallelization.

## Available Table Types

### Table (`aptos_std::table`)
The basic table implementation that provides hash-addressable storage.

```move
use aptos_std::table::{Self, Table};

// Create a new table
let table: Table<address, u64> = table::new<address, u64>();

// Add key-value pairs
table::add(&mut table, @0x1, 100);
table::add(&mut table, @0x2, 200);
```

### TableWithLength (`aptos_std::table_with_length`)
A table implementation that tracks the number of entries and allows full deletion.

```move
use aptos_std::table_with_length::{Self, TableWithLength};

// Create a table with length tracking
let table: TableWithLength<address, u64> = table_with_length::new<address, u64>();

// Add elements (length is automatically tracked)
table_with_length::add(&mut table, @0x1, 100);
```

### SmartTable (`aptos_std::smart_table`)
A bucketed table implementation that groups entries into vectors for more efficient storage.

```move
use aptos_std::smart_table::{Self, SmartTable};

// Create a smart table
let smart_table: SmartTable<address, u64> = smart_table::new<address, u64>();

// Add elements (automatically bucketed)
smart_table::add(&mut smart_table, @0x1, 100);
```

## How to Use Tables

### Basic Operations with Table

```move
module my_module::table_example {
    use aptos_std::table::{Self, Table};
    use std::string::{Self, String};

    public fun create_and_use_table(): Table<address, u64> {
        // Create a new table
        let table = table::new<address, u64>();
        
        // Add key-value pairs
        table::add(&mut table, @0x1, 100);
        table::add(&mut table, @0x2, 200);
        table::add(&mut table, @0x3, 300);
        
        // Check if key exists
        let has_key = table::contains(&table, @0x1);
        
        // Get value by key
        let value = *table::borrow(&table, @0x2);
        
        // Update existing value
        table::set(&mut table, @0x1, 150);
        
        // Remove key-value pair
        let removed_value = table::remove(&mut table, @0x3);
        
        table
    }

    public fun table_with_strings(): Table<String, u64> {
        let table = table::new<String, u64>();
        
        table::add(&mut table, string::utf8(b"alice"), 1000);
        table::add(&mut table, string::utf8(b"bob"), 2000);
        table::add(&mut table, string::utf8(b"charlie"), 3000);
        
        table
    }
}
```

### Working with TableWithLength

```move
public fun table_with_length_operations(): TableWithLength<u64, String> {
    let table = table_with_length::new<u64, String>();
    
    // Add elements (length is tracked automatically)
    table_with_length::add(&mut table, 1, string::utf8(b"first"));
    table_with_length::add(&mut table, 2, string::utf8(b"second"));
    table_with_length::add(&mut table, 3, string::utf8(b"third"));
    
    // Get length
    let len = table_with_length::length(&table);
    
    // Check if empty
    let is_empty = table_with_length::is_empty(&table);
    
    // Get value by key
    let value = *table_with_length::borrow(&table, 1);
    
    // Update value
    table_with_length::set(&mut table, 1, string::utf8(b"updated_first"));
    
    // Remove key-value pair
    let removed = table_with_length::remove(&mut table, 3);
    
    // Length is automatically updated
    let new_len = table_with_length::length(&table);
    
    table
}
```

### Using SmartTable

```move
public fun smart_table_operations(): SmartTable<address, u64> {
    let table = smart_table::new<address, u64>();
    
    // Add elements (automatically bucketed)
    smart_table::add(&mut table, @0x1, 100);
    smart_table::add(&mut table, @0x2, 200);
    smart_table::add(&mut table, @0x3, 300);
    
    // Get length
    let len = smart_table::length(&table);
    
    // Check if empty
    let is_empty = smart_table::is_empty(&table);
    
    // Get value by key
    let value = *smart_table::borrow(&table, @0x2);
    
    // Update value
    smart_table::set(&mut table, @0x1, 150);
    
    // Remove key-value pair
    let removed = smart_table::remove(&mut table, @0x3);
    
    table
}
```

### Table Abilities and Storage

```move
// Tables can be stored in global storage
struct TableHolder has key, store {
    user_balances: Table<address, u64>,
    user_profiles: TableWithLength<address, String>,
    user_scores: SmartTable<address, u64>
}

public fun store_tables(account: &signer) {
    let balances = table::new<address, u64>();
    let profiles = table_with_length::new<address, String>();
    let scores = smart_table::new<address, u64>();
    
    // Add some data
    table::add(&mut balances, @0x1, 1000);
    table_with_length::add(&mut profiles, @0x1, string::utf8(b"Alice"));
    smart_table::add(&mut scores, @0x1, 95);
    
    move_to(account, TableHolder {
        user_balances: balances,
        user_profiles: profiles,
        user_scores: scores
    });
}
```

### Iterating Over Tables

```move
public fun iterate_table(table: &Table<address, u64>): u64 {
    let total = 0u64;
    let keys = table::keys(table);
    let i = 0;
    let len = vector::length(&keys);
    
    while (i < len) {
        let key = *vector::borrow(&keys, i);
        let value = *table::borrow(table, key);
        total = total + value;
        i = i + 1;
    };
    
    total
}

// SmartTable supports direct iteration
public fun iterate_smart_table(table: &SmartTable<address, u64>): u64 {
    let total = 0u64;
    let keys = smart_table::keys(table);
    let i = 0;
    let len = vector::length(&keys);
    
    while (i < len) {
        let key = *vector::borrow(&keys, i);
        let value = *smart_table::borrow(table, key);
        total = total + value;
        i = i + 1;
    };
    
    total
}
```

## Tradeoffs

### Table Advantages
- **Hash-addressable storage** - Each entry stored in its own storage slot
- **Parallelizable operations** - Different entries can be processed in parallel
- **Scalable** - Designed for large datasets
- **Efficient lookups** - O(1) average case for key lookups
- **Individual storage slots** - Each entry has its own storage slot

### Table Disadvantages
- **Higher storage cost** - Each entry uses a separate storage slot
- **Table handle cost** - The table handle itself uses a storage slot
- **No length tracking** - Basic table doesn't track number of entries
- **Handle cannot be deleted** - Table handle persists even when empty

### TableWithLength Advantages
- **Length tracking** - Automatically tracks number of entries
- **Full deletion** - Can delete the entire table including handle
- **All table benefits** - Inherits all advantages of basic table
- **Useful for queries** - Easy to check if table is empty or get size

### TableWithLength Disadvantages
- **Not parallelizable** - Length updates prevent parallelization
- **Higher overhead** - Additional storage for length tracking
- **Sequential operations** - Length updates must be sequential

### SmartTable Advantages
- **Bucketed storage** - Groups entries into vectors for efficiency
- **Length tracking** - Automatically tracks number of entries
- **Iterable** - Supports iteration over all entries
- **Storage efficient** - Reduces number of storage slots used
- **Parallelizable** - Can be parallelized for certain operations

### SmartTable Disadvantages
- **DDoS vulnerability** - Malicious keys could create large buckets
- **Complex implementation** - More complex than basic table
- **Variable performance** - Performance depends on key distribution

## Performance Characteristics

| Operation | Table | TableWithLength | SmartTable |
|-----------|-------|-----------------|------------|
| Insert | O(1) avg | O(1) avg | O(1) avg |
| Lookup | O(1) avg | O(1) avg | O(1) avg |
| Delete | O(1) avg | O(1) avg | O(1) avg |
| Length | N/A | O(1) | O(1) |
| Iteration | Yes | Yes | Yes |
| Storage slots | N+1 | N+2 | Variable |
| Parallelization | Yes | No | Yes |

## When to Use Each Type

### Use Table when:
- You need basic hash-addressable storage
- You have large datasets
- You want parallelizable operations
- You don't need length tracking
- You want maximum flexibility

### Use TableWithLength when:
- You need to track the number of entries
- You want to be able to delete the entire table
- You need to check if the table is empty
- You don't need parallelization
- You want all table benefits plus length tracking

### Use SmartTable when:
- You want more storage-efficient bucketing
- You need both length tracking and iteration
- You want to reduce storage slot usage
- You can control key distribution
- You need scalable storage with iteration

## Best Practices

1. **Choose the right table type**: Consider your specific needs for length tracking and iteration
2. **Use appropriate key types**: Prefer simple types like `address` or `u64` for keys
3. **Handle missing keys**: Always check if a key exists before accessing it
4. **Consider storage costs**: Each table entry uses a storage slot
5. **Plan for parallelization**: Use basic Table when you need parallel operations
6. **Monitor key distribution**: For SmartTable, ensure keys are well-distributed
7. **Use references**: Borrow values instead of copying when you only need to read
8. **Batch operations**: When possible, batch multiple operations together
9. **Consider deletion**: Use TableWithLength if you need to delete the entire table
10. **Monitor storage usage**: Tables can be expensive for very large datasets
