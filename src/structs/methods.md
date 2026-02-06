# Struct Method Syntax

Move supports defining methods on structs using a receiver-style syntax. This allows you to call functions using dot notation on struct values, making code more readable and object-oriented in style.

## Defining Methods

A method is a function whose first parameter is a reference to the struct type. The method can then be called using dot notation.

```move
module my_addr::counter {
    struct Counter has key {
        value: u64,
    }

    /// Read the current value -- called as counter.value()
    public fun value(self: &Counter): u64 {
        self.value
    }

    /// Increment the counter -- called as counter.increment()
    public fun increment(self: &mut Counter) {
        self.value = self.value + 1;
    }
}
```

## Calling Methods

Once defined, methods can be called with dot notation:

```move
fun example() acquires Counter {
    let counter_ref = &Counter[@0x1];
    let val = counter_ref.value();      // Method call

    let counter_mut = &mut Counter[@0x1];
    counter_mut.increment();             // Mutable method call
}
```

## Receiver Types

Methods can take three types of receivers:

### Immutable Reference (`&Self`)

Used for read-only operations:

```move
public fun is_empty(self: &Counter): bool {
    self.value == 0
}
```

### Mutable Reference (`&mut Self`)

Used for operations that modify the struct:

```move
public fun reset(self: &mut Counter) {
    self.value = 0;
}
```

### By Value (`Self`)

Used for operations that consume the struct:

```move
public fun destroy(self: Counter): u64 {
    let Counter { value } = self;
    value
}
```

## Practical Example

Here is a more complete example showing methods in a token module:

```move
module my_addr::simple_token {
    use std::string::String;

    struct Token has store {
        name: String,
        balance: u64,
    }

    /// Create a new token
    public fun new(name: String, initial_balance: u64): Token {
        Token { name, balance: initial_balance }
    }

    /// Get the token name
    public fun name(self: &Token): &String {
        &self.name
    }

    /// Get the current balance
    public fun balance(self: &Token): u64 {
        self.balance
    }

    /// Check if the token has any balance
    public fun has_balance(self: &Token): bool {
        self.balance > 0
    }

    /// Add to the balance
    public fun deposit(self: &mut Token, amount: u64) {
        self.balance = self.balance + amount;
    }

    /// Subtract from the balance
    public fun withdraw(self: &mut Token, amount: u64): u64 {
        assert!(self.balance >= amount, 1);
        self.balance = self.balance - amount;
        amount
    }

    /// Consume the token and return the balance
    public fun redeem(self: Token): u64 {
        let Token { name: _, balance } = self;
        balance
    }
}
```

Usage with dot notation:

```move
fun example() {
    let mut token = simple_token::new(
        std::string::utf8(b"MyToken"),
        1000,
    );

    let name = token.name();
    let bal = token.balance();
    assert!(token.has_balance());

    token.deposit(500);
    let withdrawn = token.withdraw(200);
    let remaining = token.redeem();
}
```

## Method Resolution

When you write `x.method()`, the compiler looks for a function named `method` in the module where the type of `x` is defined. The first parameter of that function must be a reference to (or value of) the type of `x`.

The compiler automatically inserts the appropriate borrow. For example:

```move
let counter = Counter { value: 0 };
counter.value()  // Compiler inserts &counter as the first argument
```

## Best Practices

1. **Use methods for type-specific operations**: Any function that logically belongs to a struct should be defined as a method.
2. **Prefer `&self` over `&mut self`**: Use the least permissive receiver type.
3. **Name methods clearly**: Use verbs for actions (`deposit`, `withdraw`) and nouns for accessors (`balance`, `name`).
4. **Keep methods focused**: Each method should do one thing well.
