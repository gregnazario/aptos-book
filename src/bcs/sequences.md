# Sequences

Sequences are represented as an initial uleb128 followed by a sequence of encoded types. This can include sequences
nested inside each other. You can compose them together to make more complex nested vectors

Detailed Example:

The most trivial example is an empty sequence, which is always represented as the zero length byte `0x00`. This is for
any sequence no matter the type.

A more complex example is the `vector<u8>` `[0, 1, 2]`. We first encode the length, as a uleb128, which is the byte
`0x03`. Then, it is followed up by the three individual u8 bytes `0x00`, `0x01`, `0x02`. This gives us an entire byte
array of `0x03000102`.

Examples:

| Type                       | Value                       | Encoded Value                |
|----------------------------|-----------------------------|------------------------------|
| vector<u8>                 | []                          | 0x00                         |
| vector<u8>                 | [2]                         | 0x0102                       |
| vector<u8>                 | [2,3,4,5]                   | 0x0402030405                 |
| vector<bool>               | [true, false]               | 0x020100                     |
| vector<u16>                | [65535, 1]                  | 0x02FFFF0001                 |
| vector<vector<u8>>         | [[], [1], [2,3]]            | 0x03000101020203             |
| vector<vector<vector<u8>>> | [[[],[1]],[],[[2,3],[4,5]]] | 0x03020001010002020203020405 |

Longer examples (multi-byte uleb128 length):

| Type        | Value                                        | Encoded Value                                    |
|-------------|----------------------------------------------|--------------------------------------------------|
| vector<u8>  | [0,1,2,3,...,126,127]                        | 0x8001000102...FDFEFF                            |
| vector<u32> | [0,1,2,...,4294967293,4294967294,4294967295] | 0xFFFFFFFF0F0000000000000001...FFFFFFFEFFFFFFFFF | 
