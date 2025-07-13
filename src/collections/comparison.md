# Collection Types Comparison

This document provides a comprehensive comparison of all collection types available in Move on Aptos, helping you choose the right collection for your specific use case.

## Quick Reference Table

| Collection Type | Library | Ordering | Length Tracking | Scalability | Parallelization | Storage Cost | Best For |
|-----------------|---------|----------|-----------------|-------------|-----------------|--------------|----------|
| Vector | std | Yes | Yes | Low | No | Single slot | Small sequences |
| BigVector | aptos_std | Yes | Yes | High | Yes | Multiple slots | Large sequences |
| SimpleMap | std | No | No | Low | No | Single slot | Small key-value |
| OrderedMap | std | Yes | Yes | Low | No | Single slot | Ordered key-value |
| BigOrderedMap | aptos_std | Yes | Yes | High | Yes | Multiple slots | Large ordered key-value |
| Table | aptos_std | No | No | High | Yes | N+1 slots | Large key-value |
| TableWithLength | aptos_std | No | Yes | High | No | N+2 slots | Large key-value with length |
| SmartTable | aptos_std | No | Yes | High | Yes | Variable | Storage-efficient large key-value |

## Detailed Comparison

### Vectors

**Use Cases:**
- Storing ordered sequences of data
- Building lists, arrays, or queues
- When you need to maintain insertion order
- Small to medium datasets (< 1,000 elements)

**When to Choose:**
- **Standard Vector**: Small datasets, simple use cases, memory efficiency
- **BigVector**: Large datasets, frequent additions, scalability requirements

**Example:**
```move
// Standard Vector for small dataset
let small_list: vector<u64> = vector[1, 2, 3, 4, 5];

// BigVector for large dataset
let large_list = big_vector::new<u64>();
big_vector::push_back(&mut large_list, 1);
```

### Maps

**Use Cases:**
- Key-value storage and lookup
- Associative data structures
- When you need fast access by unique keys
- Small to medium datasets (< 10,000 entries)

**When to Choose:**
- **SimpleMap**: Basic key-value storage, maximum performance, order doesn't matter
- **OrderedMap**: Need to maintain insertion order, predictable iteration
- **BigOrderedMap**: Large datasets, need both ordering and scalability

**Example:**
```move
// SimpleMap for basic storage
let balances = simple_map::create<address, u64>();
simple_map::add(&mut balances, @0x1, 1000);

// OrderedMap for ordered storage
let profiles = ordered_map::new<address, String>();
ordered_map::add(&mut profiles, @0x1, string::utf8(b"Alice"));
```

### Tables

**Use Cases:**
- Large-scale key-value storage
- When you need parallelizable operations
- Hash-addressable storage requirements
- Large datasets (> 10,000 entries)

**When to Choose:**
- **Table**: Basic hash-addressable storage, parallelization needed
- **TableWithLength**: Need length tracking, want to delete entire table
- **SmartTable**: Storage efficiency, iteration, length tracking

**Example:**
```move
// Table for basic hash storage
let balances = table::new<address, u64>();
table::add(&mut balances, @0x1, 1000);

// SmartTable for efficient storage
let scores = smart_table::new<address, u64>();
smart_table::add(&mut scores, @0x1, 95);
```

## Performance Characteristics

### Time Complexity

| Operation | Vector | BigVector | SimpleMap | OrderedMap | BigOrderedMap | Table | TableWithLength | SmartTable |
|-----------|--------|-----------|-----------|------------|---------------|-------|-----------------|------------|
| Insert (end) | O(1) | O(1) | O(1) | O(1) | O(1) | O(1) | O(1) | O(1) |
| Insert (index) | O(n) | O(n) | N/A | N/A | N/A | N/A | N/A | N/A |
| Access | O(1) | O(1) | O(1) | O(1) | O(1) | O(1) | O(1) | O(1) |
| Delete (end) | O(1) | O(1) | O(1) | O(1) | O(1) | O(1) | O(1) | O(1) |
| Delete (index) | O(n) | O(n) | O(1) | O(1) | O(1) | O(1) | O(1) | O(1) |
| Length | O(1) | O(1) | O(n) | O(1) | O(1) | N/A | O(1) | O(1) |
| Iteration | O(n) | O(n) | O(n) | O(n) | O(n) | O(n) | O(n) | O(n) |

### Storage Characteristics

| Characteristic | Vector | BigVector | SimpleMap | OrderedMap | BigOrderedMap | Table | TableWithLength | SmartTable |
|----------------|--------|-----------|-----------|------------|---------------|-------|-----------------|------------|
| Storage slots | 1 | N | 1 | 1 | N | N+1 | N+2 | Variable |
| Parallelization | No | Yes | No | No | Yes | Yes | No | Yes |
| BCS serializable | Yes | No | Yes | Yes | No | No | No | No |
| Memory efficient | Yes | No | Yes | No | No | No | No | Yes |

## Decision Matrix

### For Small Datasets (< 1,000 elements)
- **Sequential data**: Use **Vector**
- **Key-value data**: Use **SimpleMap** (if order doesn't matter) or **OrderedMap** (if order matters)

### For Medium Datasets (1,000 - 10,000 elements)
- **Sequential data**: Use **Vector** (if memory efficient) or **BigVector** (if scalable)
- **Key-value data**: Use **SimpleMap**/**OrderedMap** (if standard library only) or **Table** (if scalable)

### For Large Datasets (> 10,000 elements)
- **Sequential data**: Use **BigVector**
- **Key-value data**: Use **Table** (basic), **TableWithLength** (need length), or **SmartTable** (storage efficient)

### Special Considerations

#### When You Need Parallelization
- Use **BigVector**, **BigOrderedMap**, **Table**, or **SmartTable**

#### When You Need Length Tracking
- Use **Vector**, **BigVector**, **OrderedMap**, **BigOrderedMap**, **TableWithLength**, or **SmartTable**

#### When You Need Ordering
- Use **Vector**, **BigVector**, **OrderedMap**, or **BigOrderedMap**

#### When You Need BCS Serialization
- Use **Vector**, **SimpleMap**, or **OrderedMap**

#### When Storage Cost is Critical
- Use **Vector**, **SimpleMap**, or **SmartTable**

## Best Practices Summary

1. **Start Simple**: Begin with standard library collections (Vector, SimpleMap, OrderedMap)
2. **Plan for Growth**: If your dataset might grow large, consider scalable alternatives early
3. **Consider Storage Costs**: Each storage slot has a cost, so choose efficiently
4. **Match Use Case**: Choose collections that match your specific requirements
5. **Test Performance**: Benchmark with realistic data sizes before committing
6. **Monitor Gas Costs**: Different collections have different gas costs for operations
7. **Consider Parallelization**: Use parallelizable collections when possible for better performance

## Migration Paths

### Growing from Small to Large
- **Vector** → **BigVector**: When you exceed ~1,000 elements
- **SimpleMap** → **Table**: When you exceed ~10,000 entries
- **OrderedMap** → **BigOrderedMap**: When you need both ordering and scalability

### Optimizing for Storage
- **Table** → **SmartTable**: When you want to reduce storage slot usage
- **Table** → **TableWithLength**: When you need length tracking

### Optimizing for Performance
- **TableWithLength** → **Table**: When you need parallelization
- **OrderedMap** → **SimpleMap**: When you don't need ordering

This comparison should help you make informed decisions about which collection type to use for your specific use case on Aptos. 