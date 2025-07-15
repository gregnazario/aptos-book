# Aptos Escrow

## 🪙 Storing Fungible Assets in a Smart Contract

In many decentralized applications, it's essential to store and manage fungible assets—also known as tokens—within a smart contract. Whether you're building a decentralized exchange (DEX), a staking protocol, or a game economy, you often need to securely hold tokens on behalf of users or the protocol itself.

In this example, we'll demonstrate how to store fungible tokens inside a Move smart contract on Aptos. We'll cover how to:

- Accept deposits of a specific token,
- Store those tokens securely in the contract,
- And (optionally) allow withdrawals under certain conditions.

This pattern forms the foundation of many on-chain financial applications, enabling safe and modular token handling using Move’s powerful resource-oriented programming model.


## Example code

Below is the full contract for aptos_escrow.

```move
/// # Aptos Escrow Contract
///
/// This module provides an escrow mechanism between two parties using `FungibleAsset` and `Object` APIs.
/// A sender can lock assets into an escrow object which only the receiver can accept or the sender can cancel.
/// It demonstrates object creation, capability restriction, and asset management using the Aptos framework.
module aptos_escrow::aptos_escrow {
    use std::signer::address_of;
    use aptos_framework::object::{Self, Object};
    use aptos_framework::primary_fungible_store;
    use aptos_framework::fungible_asset::{Self, Metadata, FungibleStore};
    use aptos_framework::event;

    /// Error code when a cancel action is attempted by someone other than the original sender.
    const ENOT_SENDER: u64 = 0;
    
    /// Error code when an accept action is attempted by someone other than the intended receiver.
    const ENOT_RECEIVER: u64 = 1;

    /// Escrow resource that stores the assets and receiver information.
    /// It lives as an Object under the Aptos object model.
    ///
    /// - `store`: the internal store holding the escrowed assets.
    /// - `receiver`: address of the intended recipient.
    /// - `extend_ref`: capability to allow extending object lifetime.
    /// - `delete_ref`: capability to allow object deletion.
    #[resource_group_member(group=aptos_framework::object::ObjectGroup)]
    struct Escrow has key {
        store: Object<FungibleStore>,
        receiver: address,
        extend_ref: object::ExtendRef,
        delete_ref: object::DeleteRef
    }

    /// Emitted when an escrow is successfully created.
    /// Contains sender, receiver, asset type, amount, and the address of the created escrow object.
    #[event]
    struct EscrowCreatedEvent has store, drop {
        sender: address,
        receiver: address,
        fa: address,
        amount: u64,
        escrow_obj: address
    }

    /// Creates a new escrow.
    ///
    /// - Withdraws `amount` of `metadata` asset from the `sender`.
    /// - Constructs a new object to store the asset.
    /// - Locks the asset inside the escrow store.
    /// - Stores receiver information and lifecycle capabilities.
    /// - Emits `EscrowCreatedEvent`.
    public entry fun create_escrow(sender: &signer, metadata: Object<Metadata>, amount: u64, receiver: address) {
        let asset = primary_fungible_store::withdraw(sender, metadata, amount);

        // Create a new object owned by the sender
        let constructor_ref = &object::create_object(address_of(sender));
        let obj_signer = &object::generate_signer(constructor_ref);

        // Generate capability refs for object control
        let transfer_ref = object::generate_transfer_ref(constructor_ref);
        object::disable_ungated_transfer(&transfer_ref);
        let extend_ref = object::generate_extend_ref(constructor_ref);
        let delete_ref = object::generate_delete_ref(constructor_ref);

        // Create an internal asset store for the escrow
        let store = fungible_asset::create_store(constructor_ref, metadata);
        fungible_asset::deposit(store, asset);

        // Construct the Escrow resource and move it into the new object
        let escrow = Escrow {
            store,
            receiver,
            extend_ref,
            delete_ref,
        };
        move_to(obj_signer, escrow);

        // Emit event for tracking
        event::emit(EscrowCreatedEvent {
            sender: address_of(sender),
            receiver,
            fa: object::object_address(&metadata),
            amount,
            escrow_obj: object::address_from_constructor_ref(constructor_ref)
        })
    }

    /// Allows the `sender` to cancel the escrow and retrieve the locked assets.
    ///
    /// Only the original sender (owner of the object) can perform this.
    public entry fun cancel_escrow(sender: &signer, escrow_obj: Object<Escrow>) acquires Escrow {
        assert!(object::is_owner(escrow_obj, address_of(sender)), ENOT_SENDER);
        let escrow_obj_addr = object::object_address(&escrow_obj);

        // Take full control of the escrow resource
        let Escrow {
            store,
            receiver: _,
            extend_ref,
            delete_ref,
        } = move_from<Escrow>(escrow_obj_addr);

        let amount = fungible_asset::balance(store);

        // Withdraw the asset using the signer derived from extend_ref
        let obj_signer = &object::generate_signer_for_extending(&extend_ref);
        let asset = fungible_asset::withdraw(obj_signer, store, amount);

        // Delete the escrow object
        object::delete(delete_ref);

        // Return the assets back to sender
        primary_fungible_store::deposit(address_of(sender), asset);
    }

    /// Allows the intended `receiver` to accept the escrow and receive the assets.
    ///
    /// Only the assigned receiver address is allowed to call this.
    public entry fun accept_escrow(receiver: &signer, escrow_obj: Object<Escrow>) acquires Escrow {
        let escrow_obj_addr = object::object_address(&escrow_obj);

        // Take full control of the escrow resource
        let Escrow {
            store,
            receiver: receiver_addr,
            extend_ref,
            delete_ref,
        } = move_from<Escrow>(escrow_obj_addr);

        // Validate that only the receiver can accept
        assert!(receiver_addr == address_of(receiver), ENOT_RECEIVER);

        let amount = fungible_asset::balance(store);

        // Withdraw the asset using signer for this object
        let obj_signer = &object::generate_signer_for_extending(&extend_ref);
        let asset = fungible_asset::withdraw(obj_signer, store, amount);

        // Delete the escrow object
        object::delete(delete_ref);

        // Deposit the assets into the receiver's account
        primary_fungible_store::deposit(receiver_addr, asset);
    }
}
```

## Breakdown

### Module

The first few lines define documentation and the name of the module. The `///` represents a doc comment. Documentation can be generated from these comments, and each `///` describes what's directly below it.

`module aptos_escrow::aptos_escrow` represents the named address and the module name. `aptos_escrow` is a named address that determines where the module is deployed. The second `aptos_escrow` is the module name. By convention, module names are lowercase and use snake_case.

```move
/// # Aptos Escrow Contract
///
/// This module provides an escrow mechanism between two parties using `FungibleAsset` and `Object` APIs.
/// A sender can lock assets into an escrow object which only the receiver can accept or the sender can cancel.
/// It demonstrates object creation, capability restriction, and asset management using the Aptos framework.
module aptos_escrow::aptos_escrow {
````

### Imports

Next, we import modules needed for the contract. The `use` keyword is used to bring in external modules or types. Imports are of the form `use <module_address>::<module_name>`. Here we use both standard and framework modules.

* `std` - The standard library: contains base utilities like `signer`, `vector`, etc.
* `aptos_framework` - Provides object APIs, fungible asset handling, event emission, etc.

```move
use std::signer::address_of;
use aptos_framework::object::{Self, Object};
use aptos_framework::primary_fungible_store;
use aptos_framework::fungible_asset::{Self, Metadata, FungibleStore};
use aptos_framework::event;
```

### Structs

The `Escrow` struct defines the core data of the escrow. Structs are Move’s way of defining custom data types. This struct is a resource stored in an object.

```move
#[resource_group_member(group=aptos_framework::object::ObjectGroup)]
struct Escrow has key {
    store: Object<FungibleStore>,
    receiver: address,
    extend_ref: object::ExtendRef,
    delete_ref: object::DeleteRef
}
```

* `store`: Holds the actual escrowed tokens.
* `receiver`: The designated address that can accept the escrow.
* `extend_ref`, `delete_ref`: Capabilities to control the lifecycle of the object (e.g., allow deletion or extension).

### Events

Events allow recording important actions on-chain in a structured way. Here, `EscrowCreatedEvent` logs when an escrow is created.

```move
#[event]
struct EscrowCreatedEvent has store, drop {
    sender: address,
    receiver: address,
    fa: address,
    amount: u64,
    escrow_obj: address
}
```

* `sender`: The address initiating the escrow.
* `receiver`: The recipient of the escrowed assets.
* `fa`: The fungible asset type.
* `amount`: The amount being escrowed.
* `escrow_obj`: The address of the created escrow object.

### Entry Functions

These are public functions users interact with. Each represents a step in the escrow flow.

---

#### `create_escrow`

```move
public entry fun create_escrow(sender: &signer, metadata: Object<Metadata>, amount: u64, receiver: address) {
    ...
}
```

* Withdraws assets from the sender.
* Creates a new object to store the escrowed tokens.
* Locks the tokens and sets lifecycle capabilities.
* Emits `EscrowCreatedEvent`.

---

#### `cancel_escrow`

```move
public entry fun cancel_escrow(sender: &signer, escrow_obj: Object<Escrow>) acquires Escrow {
    ...
}
```

* Checks that the caller is the original sender.
* Withdraws all tokens from the escrow store.
* Deletes the escrow object.
* Returns the tokens back to the sender.

---

#### `accept_escrow`

```move
public entry fun accept_escrow(receiver: &signer, escrow_obj: Object<Escrow>) acquires Escrow {
    ...
}
```

* Validates that the caller is the intended receiver.
* Withdraws the tokens from escrow.
* Deletes the escrow object.
* Transfers the tokens to the receiver.

---

This contract demonstrates secure and object-based escrow logic in Aptos using `FungibleAsset` and `Object` APIs. It also shows how to lock, unlock, and restrict transfer of objects, making it suitable for trust-minimized payment flows.

