# Structs and How They Become Resources

When a struct declares the `key` ability, it can live in global storage at an account or object address. Storing such a value requires the `move_to` primitive and later access uses `borrow_global` or `move_from`:

```move
move_to(account, Balance { amount: 10 });
let bal = borrow_global<Balance>(addr);
```

On Aptos, related resources can be grouped together so they occupy a single storage slot. The group container is annotated with `#[resource_group]` and each member is annotated with `#[resource_group_member(group = <GroupStruct>)]`:

```move
#[resource_group]
struct Wallet has key {
    balance: Balance,
}

#[resource_group_member(group = Wallet)]
struct Balance has key { amount: u64 }
```

Placing `Balance` inside the `Wallet` resource group reduces storage overhead and lets the members be loaded together.
