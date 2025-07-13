# Maps

Maps are key-value storage structures that allow efficient lookup and storage of data by unique keys. Aptos provides several map implementations with different characteristics and use cases.

## Available Map Types

### SimpleMap (`std::simple_map`)
A basic hash map implementation from the Move standard library.

```move
use std::simple_map::{Self, SimpleMap};

// Create an empty map
let map: SimpleMap<address, u64> = simple_map::create<address, u64>();

// Add key-value pairs
simple_map::add(&mut map, @0x1, 100);
simple_map::add(&mut map, @0x2, 200);
```

### OrderedMap (`std::ordered_map`)
A map implementation that maintains insertion order of keys.

```move
use std::ordered_map::{Self, OrderedMap};

// Create an ordered map
let ordered_map: OrderedMap<u64, String> = ordered_map::new<u64, String>();

// Add elements (maintains order)
ordered_map::add(&mut ordered_map, 1, string::utf8(b"first"));
ordered_map::add(&mut ordered_map, 2, string::utf8(b"second"));
```

### BigOrderedMap (`aptos_std::big_ordered_map`)
A scalable ordered map implementation for large datasets using table storage.

```move
use aptos_std::big_ordered_map::{Self, BigOrderedMap};

// Create a big ordered map
let big_map = big_ordered_map::new<address, u64>();
```

## How to Use Maps

### Basic Operations with SimpleMap

```move
module my_module::map_example {
    use std::simple_map::{Self, SimpleMap};
    use std::string::{Self, String};

    public fun create_and_use_map(): SimpleMap<address, u64> {
        // Create an empty map
        let map = simple_map::create<address, u64>();
        
        // Add key-value pairs
        simple_map::add(&mut map, @0x1, 100);
        simple_map::add(&mut map, @0x2, 200);
        simple_map::add(&mut map, @0x3, 300);
        
        // Check if key exists
        let has_key = simple_map::contains_key(&map, &@0x1);
        
        // Get value by key
        let value = *simple_map::borrow(&map, &@0x2);
        
        // Update existing value
        simple_map::set(&mut map, @0x1, 150);
        
        // Remove key-value pair
        let removed_value = simple_map::remove(&mut map, &@0x3);
        
        map
    }

    public fun map_with_strings(): SimpleMap<String, u64> {
        let map = simple_map::create<String, u64>();
        
        simple_map::add(&mut map, string::utf8(b"alice"), 1000);
        simple_map::add(&mut map, string::utf8(b"bob"), 2000);
        simple_map::add(&mut map, string::utf8(b"charlie"), 3000);
        
        map
    }
}
```

### Working with OrderedMap

```move
public fun ordered_map_operations(): OrderedMap<u64, String> {
    let map = ordered_map::new<u64, String>();
    
    // Add elements (order is preserved)
    ordered_map::add(&mut map, 3, string::utf8(b"third"));
    ordered_map::add(&mut map, 1, string::utf8(b"first"));
    ordered_map::add(&mut map, 2, string::utf8(b"second"));
    
    // Get length
    let len = ordered_map::length(&map);
    
    // Check if empty
    let is_empty = ordered_map::is_empty(&map);
    
    // Get value by key
    let value = *ordered_map::borrow(&map, &1);
    
    // Update value
    ordered_map::set(&mut map, 1, string::utf8(b"updated_first"));
    
    // Remove key-value pair
    let removed = ordered_map::remove(&mut map, &3);
    
    map
}
```

### Iterating Over Maps

```move
public fun iterate_simple_map(map: &SimpleMap<address, u64>): u64 {
    let total = 0u64;
    let keys = simple_map::keys(map);
    let i = 0;
    let len = vector::length(&keys);
    
    while (i < len) {
        let key = *vector::borrow(&keys, i);
        let value = *simple_map::borrow(map, &key);
        total = total + value;
        i = i + 1;
    };
    
    total
}

public fun iterate_ordered_map(map: &OrderedMap<u64, String>): vector<String> {
    let values = vector::empty<String>();
    let keys = ordered_map::keys(map);
    let i = 0;
    let len = vector::length(&keys);
    
    while (i < len) {
        let key = *vector::borrow(&keys, i);
        let value = *ordered_map::borrow(map, &key);
        vector::push_back(&mut values, value);
        i = i + 1;
    };
    
    values
}
```

### Map Abilities and Storage

```move
// Maps can be stored in global storage
struct MapHolder has key, store {
    user_balances: SimpleMap<address, u64>,
    user_names: OrderedMap<address, String>
}

public fun store_maps(account: &signer) {
    let balances = simple_map::create<address, u64>();
    let names = ordered_map::new<address, String>();
    
    // Add some data
    simple_map::add(&mut balances, @0x1, 1000);
    ordered_map::add(&mut names, @0x1, string::utf8(b"Alice"));
    
    move_to(account, MapHolder {
        user_balances: balances,
        user_names: names
    });
}
```

## Tradeoffs

### SimpleMap Advantages
- **Simple and efficient** - Basic hash map implementation
- **Fast lookups** - O(1) average case for key lookups
- **Memory efficient** - Compact storage for small to medium datasets
- **Standard library** - Part of Move standard library
- **BCS serializable** - Can be easily serialized

### SimpleMap Disadvantages
- **No ordering** - Keys are not stored in any particular order
- **Limited scalability** - Performance degrades with very large datasets
- **Single storage slot** - All data stored in one storage slot
- **No parallelization** - Operations cannot be parallelized

### OrderedMap Advantages
- **Maintains order** - Keys are stored in insertion order
- **Predictable iteration** - Consistent order when iterating
- **Useful for UI** - Good for displaying data in a consistent order
- **Standard library** - Part of Move standard library

### OrderedMap Disadvantages
- **Higher overhead** - Additional storage for maintaining order
- **Slower operations** - Slightly slower than SimpleMap due to ordering overhead
- **Limited scalability** - Similar limitations to SimpleMap

### BigOrderedMap Advantages
- **Scalable** - Designed for large datasets
- **Table-based storage** - Uses efficient table storage
- **Parallelizable** - Can benefit from table parallelization
- **Maintains order** - Preserves insertion order like OrderedMap

### BigOrderedMap Disadvantages
- **Higher storage cost** - Uses multiple storage slots
- **More complex** - More complex implementation
- **Not in standard library** - Part of Aptos standard library

## Performance Characteristics

| Operation | SimpleMap | OrderedMap | BigOrderedMap |
|-----------|-----------|------------|---------------|
| Insert | O(1) avg | O(1) avg | O(1) avg |
| Lookup | O(1) avg | O(1) avg | O(1) avg |
| Delete | O(1) avg | O(1) avg | O(1) avg |
| Iteration | Unordered | Ordered | Ordered |
| Storage | Single slot | Single slot | Multiple slots |
| Parallelization | No | No | Yes |

## When to Use Each Type

### Use SimpleMap when:
- You need basic key-value storage
- Order doesn't matter
- Dataset is small to medium size (< 10,000 entries)
- You want maximum performance
- You're working with standard library only

### Use OrderedMap when:
- You need to maintain insertion order
- You frequently iterate over the map
- Dataset is small to medium size
- Order is important for your use case
- You want predictable iteration order

### Use BigOrderedMap when:
- You have large datasets (> 10,000 entries)
- You need both ordering and scalability
- You want table storage benefits
- You need parallelizable operations
- You're building a high-scale application

## Best Practices

1. **Choose the right map type**: Consider your data size and ordering requirements
2. **Use appropriate key types**: Prefer simple types like `address` or `u64` for keys
3. **Handle missing keys**: Always check if a key exists before accessing it
4. **Consider storage costs**: Maps stored in global storage consume storage slots
5. **Plan for growth**: If your map might grow large, consider BigOrderedMap from the start
6. **Use references**: Borrow values instead of copying when you only need to read
7. **Batch operations**: When possible, batch multiple operations together


