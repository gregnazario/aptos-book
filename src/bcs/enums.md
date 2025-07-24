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

## Struct Enums

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

To use the struct enum in a match statement, you can do the following:

```move
module 0x42::example {
    enum ExampleStruct has drop {
        T1 {
            number: u8,
            vec: vector<bool>,
            uint16: u16
        },
        T2,
        T3(u8, bool)
    }

    public fun handle_example(example: ExampleStruct): u8 {
        match (example) {
            ExampleStruct::T1 { number, vec: _, uint16 } => {
                // Do something with the struct fields
                return number + uint16 as u8; // Just an example operation
            }
            _ => {
                abort 1 // Handle other cases
            }
        }
    }
}
```

## Simple Value Enums

For the second type, it's simply just represented as the uleb128 representing the type for value `1`. This is useful for
traditional enums that do not have any additional data. In this case, the enum is `T2`, which has no fields, and can be
represented as:

```
ExampleStruct::T2 {} = 0x01
```
To use the simple value enum in a match statement, you can do the following:

```move
module 0x42::example {

    enum ExampleStruct has drop {
        T1 {
            number: u8,
            vec: vector<bool>,
            uint16: u16
        },
        T2,
        T3(u8, bool)
    }

    public fun handle_example(example: ExampleStruct): u8 {
        match (example) {
            ExampleStruct::T2 => {
                return 42; // some arbitrary value for T2
            }
            _ => {
                abort 1
            }
        }
    }
}
```


## Tuple Enums

For the third type, it's represented as the uleb128 representing the type for value `2` followed by the tuple. The tuple
can contain any types, and they will be encoded in the same way as structs, just without named fields. In this case, the
tuple is `(3, true)`, and can be represented as:

```
ExampleStruct::T2(3,true) = 0x020301
```

To use the tuple enum in a match statement, you can do the following:

```move
module 0x42::example {
    enum ExampleStruct has drop {
        T1 {
            number: u8,
            vec: vector<bool>,
            uint16: u16
        },
        T2,
        T3(u8, bool)
    }

    public fun handle_example(example: ExampleStruct): (u8, bool) {
        let (start, end) = match (example) {
            ExampleStruct::T3(x, y) => {
                (x, y)
            }
            _ => {
                abort 1
            }
        };

        return (start, end)
    }
}
```