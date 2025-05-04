# Strings

Strings are a special case. They are represented as a `vector<u8>`, but only `UTF-8` valid characters are allowed. This
means, it would look exactly the same as a vector. Note, that the sequence length is the number of _bytes_, not the
number of _characters_.

For example the string: `❤️12345` = `0x0BE29DA4EFB88F3132333435`

Examples:

| Value   | Encoded Value      |
|---------|--------------------|
| A       | 0x0141             |
| hello   | 0x0568656C6C6f     |
| goodbye | 0x07676F6F64627965 |
| ❤️      | 0x06e29da4efb88f   |
| 💻      | 0x03E29C8D         |