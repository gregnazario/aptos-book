# Structs

Structs are represented as an *ordered* list of bytes. They must always be in this same order. This makes it very simple
to always interpret the bytes in a struct.

Detailed example:

Consider the following struct:

```move
module 0x42::example {
    struct ExampleStruct {
        number: u8,
        vec: vector<bool>,
        uint16: u16
    }
}
```

We see here that we have mixed types. These types will *always* be interpreted in that order, and must be canonical.

Here is an example of the struct:

```
ExampleStruct {
  number: 255,
  vec: vector[true, false, true],
  uint16: 65535
}
```

This would be encoded as each of the individual encodings in order.

- `255 = 0xFF`
- `[true, false, true] = 0x03010001`
- `65535 = 0xFFFF`

So combined they would be:
`0xFF03010001FFFF`

## Strings

Strings are a special case. They are represented as a `vector<u8>`, but only `UTF-8` valid characters are allowed. This
means, it would look exactly the same as a vector. Note, that the sequence length is the number of _bytes_, not the
number of _characters_.

For example the string: `❤️12345` = `0x0BE29DA4EFB88F3132333435`