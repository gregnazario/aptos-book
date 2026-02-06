# Account Authorization by Signer

The signer is the primary mechanism for authorization in Move. A `signer` value can only be created by the Aptos VM as part of a transaction -- it cannot be forged. This makes signers the foundation for access control in smart contracts.

## The Signer Type

A `signer` represents the identity of an account that signed a transaction. It is used to:

1. **Authorize resource creation**: `move_to` requires a signer to store resources under an address.
2. **Prove identity**: Functions can verify the caller's address.
3. **Control access**: Only the signer can modify their own resources (unless explicitly delegated).

## Basic Pattern

```move
module my_addr::profile {
    use std::signer;
    use std::string::String;

    /// Only the account owner can modify their profile
    struct Profile has key {
        name: String,
        bio: String,
    }

    /// Create a profile -- requires the signer's authorization
    public entry fun create_profile(
        account: &signer,
        name: String,
        bio: String,
    ) {
        move_to(account, Profile { name, bio });
    }

    /// Update a profile -- only the owner can call this
    public entry fun update_bio(
        account: &signer,
        new_bio: String,
    ) acquires Profile {
        let addr = signer::address_of(account);
        let profile = &mut Profile[addr];
        profile.bio = new_bio;
    }
}
```

The signer ensures that only the account owner can create or modify their own profile.

## Authorization Checks

### Verifying the Caller

```move
const E_NOT_ADMIN: u64 = 1;
const ADMIN_ADDRESS: address = @0x1;

public entry fun admin_only_action(account: &signer) {
    let addr = signer::address_of(account);
    assert!(addr == ADMIN_ADDRESS, E_NOT_ADMIN);
    // Perform admin action
}
```

### Multi-Signer Authorization

Entry functions can require multiple signers, which enables multi-party authorization:

```move
public entry fun joint_action(
    party_a: &signer,
    party_b: &signer,
) {
    let addr_a = signer::address_of(party_a);
    let addr_b = signer::address_of(party_b);
    // Both parties have authorized this action
}
```

## Signer vs. Address

A common question is when to use `&signer` versus `address` as a function parameter:

- Use **`&signer`** when the function modifies the caller's state or needs authorization.
- Use **`address`** when the function only reads state.

```move
/// Requires authorization -- uses signer
public entry fun deposit(account: &signer, amount: u64) { ... }

/// Read-only -- uses address
#[view]
public fun get_balance(addr: address): u64 { ... }
```

## Capability Pattern

For delegated authorization, you can use a capability pattern where a `signer` creates a capability object that can be used later:

```move
module my_addr::managed_token {
    use std::signer;

    struct MintCapability has key, store {
        max_amount: u64,
    }

    /// Only the admin can grant mint capabilities
    public entry fun grant_mint_capability(
        admin: &signer,
        recipient: &signer,
        max_amount: u64,
    ) {
        assert!(signer::address_of(admin) == @my_addr, 1);
        move_to(recipient, MintCapability { max_amount });
    }

    /// Anyone with a MintCapability can mint
    public entry fun mint(account: &signer, amount: u64) acquires MintCapability {
        let addr = signer::address_of(account);
        let cap = &MintCapability[addr];
        assert!(amount <= cap.max_amount, 2);
        // Perform minting
    }
}
```

## Best Practices

1. **Always use signers for state changes**: Never accept a plain `address` for operations that modify state.
2. **Check addresses explicitly**: When you need a specific caller (like an admin), verify the address with `assert!`.
3. **Minimize signer scope**: Pass `&signer` (reference) rather than `signer` (by value) to prevent unintended transfers.
4. **Use capabilities for delegation**: When you need to delegate authority, create capability resources rather than passing signers around.
