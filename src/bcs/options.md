# Options

Options are a special case of [enums](enums.md). It is simply either a `0` for a `None` option and a `1` plus the value
for a `Some` option.  The purpose of the option is to represent a value that may or may not be present, similar to other
programming languages' `Option` or `Maybe` types.

Examples:

| Type                 | Value           | Encoded Value  |
|----------------------|-----------------|----------------|
| Option<bool>         | None            | 0x00           |
| Option<bool>         | Some(false)     | 0x0100         |
| Option<bool>         | Some(true)      | 0x0101         |
| Option<vector\<u16>> | None            | 0x00           |
| Option<vector\<u16>> | Some([1,65535)) | 0x01020001FFFF |