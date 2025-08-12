# Defining and Instantiating Structs

A struct definition lists its name, any abilities it supports, and its fields:

```move
module examples::points {
    /// A simple struct representing a point in 2D space
    struct Point has copy, drop {
        x: u64,
        y: u64,
    }
}
```

The `has` clause declares the abilities a value of `Point` possesses. A struct may only declare abilities that all of its fields also possess.

Instantiate a struct by providing values for every field in any order:

```move
let p = Point { x: 1, y: 2 };
```

Move supports *deconstruction* to pull a struct back apart. This moves the fields out of the struct:

```move
let Point { x, y } = p; // `p` is now consumed
```

If the struct has the `copy` ability, deconstruction can copy the value instead of moving it:

```move
let Point { x, y } = p; // `p` remains usable
```

Deconstruction can also rename fields:

```move
let Point { x: x0, y: y0 } = p;
```

These patterns allow you to build and manipulate structured data naturally in Move.
