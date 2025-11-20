# Structs and How They Become Resources

When a struct declares the `key` ability, it can live in global storage at an account or object address. Storing such a value requires the `move_to` primitive and later access uses `borrow_global`, `&[]` or `move_from`:

```move
move_to(account, Balance { amount: 10 });
let bal = &Balance[addr];
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

Placing `Balance` inside the `Wallet` resource group has a trade off on storage costs and lets the members be loaded together in a single storage slot.  The most common example is 0x1::object::ObjectGroup
