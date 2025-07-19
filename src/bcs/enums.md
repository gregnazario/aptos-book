# Enums

Enums allow for upgradable and different types in a compact representation. They are encoded with a variant index (as a uleb128 value) followed by the values of the variant's fields.

Example:

Here is an enum in Move, you can see the first value is a struct, the second is a simple value, and the third is a
tuple.

```move
module 0x42::example {
    enum ExampleStruct {
        T1 {
            number: u8,
            vec: vector<bool>,
            uint16: u16
        },
        T2,
        T3(u8, bool)
    }
}
```

Let's start with the first type:

```
ExampleStruct::T1 {
  number: 1,
  vec: [true, false, true]
  uint16: 65535
}
```

The encoding starts with a uleb128-encoded variant index (0 for T1), followed by the field values. The complete encoding is `0x000103010001FFFF` where:

- `00`: Variant index 0 (T1)
- `01`: Value of `number` (1)
- `030100`: Vector of bools `[true, false, true]` (length 3, values 0x01, 0x00, 0x01)
- `FFFF`: Value of `uint16` (65535) in little-endian

For the second type, it's simply just represented as the uleb128 representing the type for value `1`:

```
ExampleStruct::T2 {} = 0x01
```

For the third type, it's represented as the uleb128 representing the type for value `2` followed by the tuple:

```
ExampleStruct::T3(3,true) = 0x020301
```