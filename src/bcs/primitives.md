# BCS Primitives

Here is a list of primitives, and more descriptions below. Keep in mind all numbers are stored in little-endian byte
order.

| Type                | Number of bytes | Description                             |
|---------------------|-----------------|-----------------------------------------|
| [bool](#bool)       | 1               | Boolean value (true or false)           |
| [u8](#u8)           | 1               | Unsigned 8-bit integer                  |
| [u16](#u16)         | 2               | Unsigned 16-bit integer                 |
| [u32](#u32)         | 4               | Unsigned 32-bit integer                 |
| [u64](#u64)         | 8               | Unsigned 64-bit integer                 |
| [u128](#u128)       | 16              | Unsigned 128-bit integer                |
| [u256](#u256)       | 32              | Unsigned 256-bit integer                |
| [address](#address) | 32              | Aptos Address (32-byte integer)         |
| [uleb128](#uleb128) | 1-32            | Unsigned little-endian base-128 integer |

## Bool

A boolean is a single byte.  `0x00` represents `false`, `0x01` represents `true`. All other values are defined as
invalid.

Examples:

| Value | BCS Serialized Value |
|-------|----------------------|
| false | 0x00                 |
| true  | 0x01                 |

## U8

A U8 is an unsigned 8-bit integer (1 byte).

Examples:

| Value | BCS Serialized Value |
|-------|----------------------|
| 0     | 0x00                 |
| 1     | 0x01                 |
| 16    | 0x0F                 |
| 255   | 0xFF                 |

## U16

A U16 is an unsigned 16-bit integer (2 bytes).

Examples:

| Value | BCS Serialized Value |
|-------|----------------------|
| 0     | 0x0000               |
| 1     | 0x0001               |
| 16    | 0x000F               |
| 255   | 0x00FF               |
| 256   | 0x0100               |
| 65535 | 0xFFFF               |

## U32

A U32 is an unsigned 32-bit integer (4 bytes).

Examples:

| Value      | BCS Serialized Value |
|------------|----------------------|
| 0          | 0x00000000           |
| 1          | 0x00000001           |
| 16         | 0x0000000F           |
| 255        | 0x000000FF           |
| 65535      | 0x0000FFFF           |
| 4294967295 | 0xFFFFFFFF           |

## U64

A U64 is an unsigned 64-bit integer (8 bytes).

Examples:

| Value                | BCS Serialized Value |
|----------------------|----------------------|
| 0                    | 0x0000000000000000   |
| 1                    | 0x0000000000000001   |
| 16                   | 0x000000000000000F   |
| 255                  | 0x00000000000000FF   |
| 65535                | 0x000000000000FFFF   |
| 4294967295           | 0x00000000FFFFFFFF   |
| 18446744073709551615 | 0xFFFFFFFFFFFFFFFF   |

## U128

A U128 is an unsigned 128-bit integer (16 bytes).

Examples:

| Value                                   | BCS Serialized Value               |
|-----------------------------------------|------------------------------------|
| 0                                       | 0x00000000000000000000000000000000 |
| 1                                       | 0x00000000000000000000000000000001 |
| 16                                      | 0x0000000000000000000000000000000F |
| 255                                     | 0x000000000000000000000000000000FF |
| 65535                                   | 0x0000000000000000000000000000FFFF |
| 4294967295                              | 0x000000000000000000000000FFFFFFFF |
| 18446744073709551615                    | 0x0000000000000000FFFFFFFFFFFFFFFF |
| 340282366920938463463374607431768211455 | 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF |

## U256

A U256 is an unsigned 256-bit integer (32 bytes).

Examples:

| Value                                                                          | BCS Serialized Value                                               |
|--------------------------------------------------------------------------------|--------------------------------------------------------------------|
| 0                                                                              | 0x0000000000000000000000000000000000000000000000000000000000000000 |
| 1                                                                              | 0x0000000000000000000000000000000000000000000000000000000000000001 |
| 16                                                                             | 0x000000000000000000000000000000000000000000000000000000000000000F |
| 255                                                                            | 0x00000000000000000000000000000000000000000000000000000000000000FF |
| 65535                                                                          | 0x000000000000000000000000000000000000000000000000000000000000FFFF |
| 4294967295                                                                     | 0x00000000000000000000000000000000000000000000000000000000FFFFFFFF |
| 18446744073709551615                                                           | 0x000000000000000000000000000000000000000000000000FFFFFFFFFFFFFFFF |
| 340282366920938463463374607431768211455                                        | 0x00000000000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF |
| 115792089237316195423570985008687907853269984665640564039457584007913129639935 | 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF |

## Address

An address is the 32-byte representation of a storage slot on Aptos. It can be used for accounts, objects, and other
addressable storage.

Addresses have special addresses `0x0` to `0xA`, and then full length addresses. For legacy purposes, addresses
with leading zeros can be shortened, and they will be automatically extended by padding with leading zeros.

Examples:

| Value                                                              | BCS Serialized Value                                               |
|--------------------------------------------------------------------|--------------------------------------------------------------------|
| 0x0                                                                | 0x0000000000000000000000000000000000000000000000000000000000000000 |
| 0x1                                                                | 0x0000000000000000000000000000000000000000000000000000000000000001 |
| 0xA                                                                | 0x000000000000000000000000000000000000000000000000000000000000000A |
| 0xABCDEF (Legacy shortened address)                                | 0x0000000000000000000000000000000000000000000000000000000000ABCDEF |
| 0x0000000000000000000000000000000000000000000000000000000000ABCDEF | 0x0000000000000000000000000000000000000000000000000000000000ABCDEF |
| 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF | 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF |

## Uleb128

A uleb128 is a variable-length integer used mainly for representing sequence lengths. It is very efficient at storing
small numbers, and takes up more space as the number grows. Note that the Aptos specific implementation only supports
representing a `u32` in the uleb128. Any value more than the max `u32` is considered invalid.

Examples:

| Value      | BCS Serialized Value |
|------------|----------------------|
| 0          | 0x00                 |
| 1          | 0x01                 |
| 127        | 0x7F                 |
| 128        | 0x8001               |
| 240        | 0xF001               |
| 255        | 0xFF01               |
| 65535      | 0xFFFF03             |
| 16777215   | 0xFFFFFF07           |
| 4294967295 | 0xFFFFFFFF0F         |