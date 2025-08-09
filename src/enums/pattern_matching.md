# Pattern Matching with Enums

Pattern matching lets you branch on the variant of an enum and bind any inner values in a single expression:

```move
fun describe(status: Status): vector<u8> {
    match status {
        Status::Success(v) => b"ok".to_vec(),
        Status::Error { code, message } => message,
        Status::Pending => b"pending".to_vec(),
    }
}
```

Matches must be *exhaustive*—every variant is handled. This trait aids upgradability. If a new variant is later added to `Status`, existing `match` expressions that do not include a wildcard arm like `_ =>` will fail to compile, drawing attention to the new case and ensuring the code is updated accordingly.
