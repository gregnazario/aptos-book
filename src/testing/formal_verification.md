# Formal Verification

Beyond unit testing, Move supports **formal verification** through the Move Prover. The prover mathematically proves that your code satisfies specified properties, providing stronger guarantees than testing alone.

## What is Formal Verification?

Unit tests check specific inputs, but formal verification checks **all possible inputs**. If the Move Prover verifies a property, it holds for every possible execution path.

## Specification Language

Move uses a specification language to express properties that should hold. Specifications are written in `spec` blocks:

```move
module my_addr::math {
    public fun add(a: u64, b: u64): u64 {
        a + b
    }

    spec add {
        // The result is the sum of the inputs
        ensures result == a + b;
        // The result is at least as large as either input
        ensures result >= a;
        ensures result >= b;
        // Aborts if the addition would overflow
        aborts_if a + b > MAX_U64;
    }
}
```

## Common Specification Constructs

### `ensures`

Describes postconditions -- what must be true after the function executes:

```move
spec get_balance {
    ensures result >= 0;
}
```

### `requires`

Describes preconditions -- what must be true when the function is called:

```move
spec transfer {
    requires amount > 0;
    requires from_addr != to_addr;
}
```

### `aborts_if`

Describes under what conditions the function may abort:

```move
spec withdraw {
    aborts_if !exists<Account>(addr);
    aborts_if Account[addr].balance < amount;
}
```

### `invariant`

Describes properties that must always hold for a struct:

```move
spec module {
    invariant forall addr: address where exists<Counter>(addr):
        Counter[addr].value <= MAX_COUNT;
}
```

## Running the Prover

```sh
aptos move prove --dev
```

The prover will either confirm that all specifications are satisfied or report a counterexample showing a violation.

## When to Use Formal Verification

- **Financial logic**: Verify that token transfers preserve total supply.
- **Access control**: Prove that only authorized accounts can perform privileged operations.
- **Invariants**: Ensure that data structure invariants are maintained across all operations.

## Limitations

- The prover may time out on complex functions.
- Not all Move features are fully supported by the specification language.
- Writing good specifications requires practice and careful thought.

## Best Practices

1. **Start with critical functions**: Focus verification on security-sensitive code.
2. **Write specifications incrementally**: Add specifications as you develop.
3. **Combine with testing**: Use unit tests for basic correctness and formal verification for stronger guarantees.
4. **Keep functions simple**: Simpler functions are easier to specify and verify.
