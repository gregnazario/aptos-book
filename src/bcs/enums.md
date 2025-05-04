# Enums

Enums allow for upgradable and different types in a compact representation. They are headed first by a type (in a
uleb128), followed by the expected type values.

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

This would first start with the initial uleb128 representing the type, then followed by the bytes. In this case, it is
the first in the enum, so it will be represented as enum `0`. All together it is represented by: `0x000103010001FFFF`.

For the second type, it's simply just represented as the uleb128 representing the type for value `1`:

```
ExampleStruct::T2 {} = 0x01
```

For the third type, it's represented as the uleb128 representing the type for value `2` followed by the tuple:

```
ExampleStruct::T2(3,true) = 0x020301
```