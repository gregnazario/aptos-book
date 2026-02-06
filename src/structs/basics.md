# Defining and Instantiating Structs

Structs are the primary way to create custom data types in Move. They group related fields together under a single name, much like structs in Rust or C.

## Defining a Struct

A struct is defined using the `struct` keyword followed by the struct name, optional abilities, and the fields inside curly braces.

```move
module my_addr::profiles {
    use std::string::String;

    struct UserProfile has key, store {
        name: String,
        age: u8,
        balance: u64,
    }
}
```

Key points about struct definitions:

- The struct name must start with an uppercase letter by convention.
- Each field has a name and a type, separated by a colon.
- Fields are separated by commas.
- Abilities (`key`, `store`, `copy`, `drop`) are declared after `has`.

## Creating Struct Instances

You create a struct instance by specifying the struct name and providing values for each field.

```move
module my_addr::profiles {
    use std::string::{Self, String};

    struct UserProfile has key, store, drop {
        name: String,
        age: u8,
        balance: u64,
    }

    public fun create_profile(name: String, age: u8): UserProfile {
        UserProfile {
            name,
            age,
            balance: 0,
        }
    }
}
```

### Field Init Shorthand

When a variable has the same name as the struct field, you can use the shorthand syntax. In the example above, `name` and `age` are used directly without writing `name: name` and `age: age`.

## Accessing Struct Fields

You access struct fields using dot notation:

```move
public fun get_name(profile: &UserProfile): &String {
    &profile.name
}

public fun get_age(profile: &UserProfile): u8 {
    profile.age
}
```

## Modifying Struct Fields

To modify fields, you need a mutable reference to the struct:

```move
public fun update_age(profile: &mut UserProfile, new_age: u8) {
    profile.age = new_age;
}

public fun add_balance(profile: &mut UserProfile, amount: u64) {
    profile.balance = profile.balance + amount;
}
```

## Destructuring Structs

You can destructure a struct to extract its fields. This is required when you want to destroy a struct that does not have the `drop` ability.

```move
public fun destroy_profile(profile: UserProfile): (String, u8, u64) {
    let UserProfile { name, age, balance } = profile;
    (name, age, balance)
}
```

You can also partially destructure with `..` to ignore fields:

```move
public fun get_balance_from_profile(profile: UserProfile): u64 {
    let UserProfile { balance, .. } = profile;
    balance
}
```

## Storing Structs in Global Storage

Structs with the `key` ability can be stored in global storage under an account address:

```move
module my_addr::profiles {
    use std::signer;
    use std::string::String;

    struct UserProfile has key, store {
        name: String,
        age: u8,
        balance: u64,
    }

    /// Store a profile under the caller's account
    public entry fun register(account: &signer, name: String, age: u8) {
        let profile = UserProfile {
            name,
            age,
            balance: 0,
        };
        move_to(account, profile);
    }

    /// Read the profile for a given address
    #[view]
    public fun get_profile_age(addr: address): u8 acquires UserProfile {
        UserProfile[addr].age
    }
}
```

## Nested Structs

Structs can contain other structs as fields:

```move
module my_addr::game {
    struct Position has copy, drop, store {
        x: u64,
        y: u64,
    }

    struct Player has key, store {
        position: Position,
        health: u64,
        score: u64,
    }
}
```

## Best Practices

1. **Use descriptive field names**: Make field names clear and self-documenting.
2. **Minimize abilities**: Only add the abilities your struct actually needs.
3. **Group related data**: If several values are always used together, put them in a struct.
4. **Document with `///`**: Add doc comments above your struct definitions explaining their purpose.
5. **Use `key` for top-level storage**: Only structs that need to be stored directly under an address need `key`.
