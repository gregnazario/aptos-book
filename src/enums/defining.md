# Defining Enums

An enum lists its possible variants inside curly braces. The enum may also declare abilities just like a struct:

```move
enum Status has copy, drop {
    Success(u64),
    Error { code: u64, message: vector<u8> },
    Pending,
}
```

Each variant is constructed by name, using either tuple-style or struct-style syntax:

```move
let s1 = Status::Success(100);
let s2 = Status::Error { code: 7, message: b"failed".to_vec() };
let s3 = Status::Pending;
```

All variants of an enum share the same abilities. The abilities must be supported by the fields carried in every variant.
