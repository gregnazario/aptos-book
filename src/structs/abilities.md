# Structs and Abilities

Abilities describe what operations are permitted on a type. Move defines four abilities:

* `copy` – the value can be duplicated implicitly or explicitly copied with the `copy` keyword.
* `drop` – the value can be discarded without being returned or stored in global storage.
* `store` – the value may be stored in another struct or enum. 
* `key` – the value serves as a top-level resource in global storage.  It also defines if a type can be used as a key in a table.

A struct lists the abilities it supports after the `has` keyword:

```move
struct Balance has key, store { amount: u64 }
```

This declaration means that `Balance` can live in global storage as a resource and can be read or written. Because it lacks `copy` and `drop`, values of `Balance` must be moved or explicitly destroyed.  It can also be put inside another struct.

If a struct has fields that do not have a particular ability, the struct cannot declare that ability. For example, if one field lacks `copy`, the containing struct also lacks `copy` and will fail at compilation time.
