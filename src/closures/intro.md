# Closures, Lambdas, and Function Values

Aptos has extended the Move language with support for closures, lambdas, and function values. These features allow you to pass functions as arguments to other functions, enabling higher-order programming patterns.

## Function Types

Move supports function types that describe the signature of a callable:

```move
module my_addr::functional {
    /// Apply a function to each element of a vector
    public fun map(v: &vector<u64>, f: |u64| -> u64): vector<u64> {
        let result = vector[];
        let i = 0;
        let len = v.length();
        while (i < len) {
            result.push_back(f(v[i]));
            i = i + 1;
        };
        result
    }
}
```

## Lambda Expressions

Lambdas are anonymous functions defined inline:

```move
fun example() {
    let numbers = vector[1, 2, 3, 4, 5];
    let doubled = map(&numbers, |x| x * 2);
    // doubled = [2, 4, 6, 8, 10]
}
```

## Using with Standard Library

The standard library provides functions that accept closures:

```move
fun example() {
    let numbers = vector[1, 2, 3, 4, 5];

    // for_each applies a function to each element
    numbers.for_each(|n| {
        std::debug::print(&n);
    });

    // filter keeps elements matching a predicate
    let evens = numbers.filter(|n| *n % 2 == 0);
}
```

## Inline Functions with Closures

Inline functions that accept closures allow the compiler to optimize away the function call overhead:

```move
public inline fun do_if<T>(condition: bool, f: || -> T, default: T): T {
    if (condition) {
        f()
    } else {
        default
    }
}
```

## Limitations

Closures in Move have some restrictions compared to other languages:

- Closures cannot capture mutable references from the enclosing scope in all cases.
- Function values cannot be stored in structs or global storage.
- Recursive closures are not supported.

These restrictions exist to maintain Move's safety guarantees while providing the expressiveness of higher-order functions.

## When to Use Closures

- **Collection processing**: Mapping, filtering, and folding over vectors.
- **Custom iteration**: Providing callback functions for iteration patterns.
- **Configuration**: Passing behavior as a parameter to generic functions.
