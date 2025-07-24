# Binary Canonical Serialization (BCS)

Binary Canonical Serialization (BCS) is a method that allows for compact and efficient storage. It was invented at Diem for the purposes of a consistent signing mechanism.

## Properties

### Binary

The serialization method is directly in bytes and is not human-readable. For example, for a String `hello`, it would be
represented by the length of the string as a binary encoded uleb-128, followed by the UTF-8 encoded bytes of hello.  
e.g. `"hello" = 0x0548656C6C6F`  This is different from, say, a human-readable format such as JSON which would give
`"hello"`

### Canonical

There is only one canonical way to represent the bytes. This ensures that signing and representation are consistent.

Example:

Let's consider this struct in Move:

```move
module 0x42::example {
    struct FunStruct {
        a: u8,
        b: u8
    }
}
```

In JSON, the struct `{"a":1, "b": 2}` can also be represented as `{"b":2, "a":1}`. Both are interchangeable so
they are not canonical. In BCS, it would be a pre-defined order, so only one would be the valid representation.

However, in BCS, there is only one valid representation of that, which would be the bytes `0x0102`.  `0x0201` is not
canonical, and it would instead be interpreted as `{"a":2, "b":1}`.

### Non-self describing

The format is not self-describing. This means that deserialization requires knowledge of the shape and how to interpret
the bytes. This is in opposition to a type like JSON, which is self-describing.

Example:

Let's consider this struct in Move again:

```move
module 0x42::example {
    struct FunStruct {
        a: u8,
        b: u8
    }
}
```

The first byte will always be interpreted as `a` then `b`. So, `0x0A00` would be `{"a":10, "b":0}` and `0x0A01` would be
`{"a":10, "b":1}`. If we flip it to `0x000A` it would be `{"a":0, "b":10}`.

Note that this means if I do not know what the shape of the struct is, then I do not know if this is a single `u16`, the
above struct, or something else.

# Details about different types

- [Primitives](primitives.md)
- [Sequences](sequences.md)
- [Structs](structs.md)
- [Enums](enums.md)
- [Strings](strings.md)