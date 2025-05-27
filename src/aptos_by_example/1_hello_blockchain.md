# 1 - Hello Blockchain

Let's start with the simplest example, which shows you how to:

1. Build and publish a contract
2. Write data on-chain
3. Read data on-chain

## Example code

Below is the full contract for hello_blockchain.

```move
/// Writes a message to a single storage slot, all changes overwrite the previous.
/// Changes are recorded in `MessageChange` events.
module hello_blockchain::message {
    use std::error;
    use std::signer;
    use std::string::{Self, String};
    use aptos_framework::event;
    #[test_only]
    use std::debug::print;

    /// A resource for a single storage slot, holding a message.
    struct MessageHolder has key {
        message: String,
    }

    #[event]
    /// Event representing a change in a message, records the old and new messages, and who wrote it.
    struct MessageChange has drop, store {
        account: address,
        from_message: String,
        to_message: String,
    }

    /// The address does not contain a MessageHolder
    const E_NO_MESSAGE: u64 = 1;

    #[view]
    /// Reads the message from storage slot
    public fun get_message(addr: address): String acquires MessageHolder {
        assert!(exists<MessageHolder>(addr), error::not_found(E_NO_MESSAGE));
        MessageHolder[addr].message
    }

    /// Sets the message to the storage slot
    public entry fun set_message(account: signer, message: String) acquires MessageHolder {
        let account_addr = signer::address_of(&account);
        if (!exists<MessageHolder>(account_addr)) {
            move_to(&account, MessageHolder {
                message,
            })
        } else {
            let message_holder = &mut MessageHolder[account_addr];
            let from_message = message_holder.message;
            event::emit(MessageChange {
                account: account_addr,
                from_message,
                to_message: message,
            });
            message_holder.message = message;
        }
    }

    #[test(account = @0x1)]
    fun sender_can_set_message(account: signer) acquires MessageHolder {
        let msg: String = string::utf8(b"Running test sender_can_set_message...");
        print(&msg);

        let addr = signer::address_of(&account);
        aptos_framework::account::create_account_for_test(addr);
        set_message(account, string::utf8(b"Hello, Blockchain"));

        assert!(get_message(addr) == string::utf8(b"Hello, Blockchain"));
    }
}
```

## Breakdown

### Module

The first 3 lines here, define documentation and the name of the module. Here you can see that the `///` represents a
doc comment. Documentation can be generated from these comments, where `///` describes what's directly below it.

`module hello_blockchain::message` represents the name of the address, and the name of the module.  `hello_blockchain`
is what we call a named address. This named address can be passed in at compile time, and determines where the contract
is being deployed.  `message` is the name of the module. By convention, these are lowercased.

```move
/// Writes a message to a single storage slot, all changes overwrite the previous.
/// Changes are recorded in `MessageChange` events.
module hello_blockchain::message {
```