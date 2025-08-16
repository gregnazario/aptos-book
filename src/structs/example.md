# Example Program Using Structs

```move
module examples::wallet {
    #[resource_group]
    struct Wallet has key {
        balance: Balance,
    }

    #[resource_group_member(group = Wallet)]
    struct Balance has store { amount: u64 }

    /// Create an empty wallet resource under the signer
    public fun create(account: &signer) {
        move_to(account, Wallet { balance: Balance { amount: 0 } });
    }

    /// Add coins to the wallet
    public fun deposit(account: &signer, amount: u64) acquires Wallet {
        let wallet = borrow_global_mut<Wallet>(signer::address_of(account));
        wallet.balance.amount = wallet.balance.amount + amount;
    }

    /// Withdraw coins using deconstruction and reconstruction
    public fun withdraw(account: &signer, amount: u64) acquires Wallet {
        let wallet = borrow_global_mut<Wallet>(signer::address_of(account));
        let Balance { amount: bal } = wallet.balance; // deconstruct
        assert!(bal >= amount, 1);
        wallet.balance = Balance { amount: bal - amount }; // reconstruct
    }
}
```

This module shows struct definition, grouping with annotations, and how construction and deconstruction work when modifying a resource.
