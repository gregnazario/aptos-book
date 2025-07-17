# Hello Blockchain!

Let's start with the simplest example, which shows you how to:

1. Build and publish a contract
2. Write data on-chain
3. Read data on-chain

## Deploying your first contract

First, we'll create an account on devnet to deploy your contract, we'll name it the profile `tutorial`:
```sh
aptos init --profile tutorial --network devnet --assume-yes
```

Next, open a new test folder, then call the command `aptos move init --template` to initialize a test.

```sh
mkdir hello_blockchain
cd hello_blockchain
aptos move init --template hello_blockchain
```

This will create a folder structure like so:
```
hello_blockchain
├── Move.toml
├── sources
├── scripts
└── tests
```

Then, the run next command to simply build and publish the contract:

```sh
aptos move publish --profile tutorial --named-addresses hello_blockhain=tutorial
```

> Note that `named-addresses` sets the named address `hello_blockchain` in the `Move.toml` file to
> the `tutorial` profile created in the CLI.

Great!  You've deployed your first contract!  TODO: add link to visit it in the explorer.

## Running the app

Now that you've deployed your first contract, let's interact with it.

Let's create your first message on-chain by calling an [entry function](../appendix/glossary.md#entry_function):

```sh
aptos move run --profile tutorial --function-id tutorial::hello_blockchain::set_message --args "string:Hello world!"
```

> Note that this runs the entry function `hello_blockchain::set_message` on the contract you just deployed.
> It then provides the first non-signer argument as a string.

Once this is run successfully, you can view the on-chain state, with a [view function](../appendix/glossary.md#view_function):

```sh
aptos move view --profile tutorial --function-id tutorial::hello_blockchain::get_message --args address:tutorial
```

This will return the value `Hello world!` you just wrote on-chain.  Congrats you've just written and read your first data on-chain!
You can continue to run those two functions to write and read from the on-chain state respectively.

For more information about this, let's dive into the full contract and a breakdown next.

## Full Contract

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
module hello_blockchain::message {}
```

### Imports

Next, we import some libraries that we will use in our contract. The `use` keyword is used to import modules, and are of
the form `use <module_address>::<module_name>`. There are three standard library addresses that we can use from Aptos:

- `std` - The standard library, which contains basic functionality like strings, vectors, and events.
- `aptos_std` - The Aptos standard library, which contains functionality specific to the Aptos blockchain, like string
  manipulation.
- `aptos_framework` - The Aptos framework, which contains functionality specific to the Aptos framework, like events,
  objects, accounts and more.

> Note that the `#[test_only]` attribute is used to indicate that the module is only for testing purposes, and will not
> be compiled into the non-test bytecode. This is useful for debugging and testing purposes.

```move
use std::error;
use std::signer;
use std::string::{Self, String};
use aptos_framework::event;
#[test_only]
use std::debug::print;
```

### Structs

Next, we define a struct that will hold our message. Structs are structured data that is a collection of other types.
These types can be primitives (e.g. `u8`, `bool`, `address`) or other structs. In this case, the struct is called
`MessageHolder`, and it has a single field to hold the message.

```move
/// A resource for a single storage slot, holding a message.
struct MessageHolder has key {
    message: String,
}
```

### Events

Next, we define an event that will be emitted when the message is changed. Events are used to record changes to the
blockchain in an easily indexable way. They are similar to events in other programming languages, and can be used to log
changes to the blockchain. In this case, the event is called `MessageChange`, and it has three fields: `account`, which
is the address of the account that changed the message, `from_message`, which is the old message, and `to_message`,
which is the new message. The `has drop, store` attributes are required for events and indicate that the event can be
dropped from scope and stored in the blockchain.

Events are defined with the `#[event]` annotation, and is required to emit as an event.

```move
#[event]
/// Event representing a change in a message, records the old and new messages, and who wrote it.
struct MessageChange has drop, store {
    account: address,
    from_message: String,
    to_message: String,
}
```

> Note that the doc comments `///` must be directly above the struct, and not before the annotations.
> This differs from Rust, which allows the annotation in either location.

### Constants and Error messages

Next is specifically a constant.  Constants in Move must have a type definition, and can only be primitive types.
They can also be documented with a doc comment.  In this case, it will be used as an `error`, which is can define
a user defined message when aborting.  By convention, these start with a `E_` or `E`, and the doc comment will
define the abort error message.  We'll show how these are used later.

```move
/// The address does not contain a MessageHolder
const E_NO_MESSAGE: u64 = 1;
```

### View Functions and Reading State

View functions are how external callers can easily read state from the blockchain.  As you can see
here the function `get_message` allows for outputting the message stored on chain.  The `#[view]`
annotation marks a function as callable from outside of the Move VM.  Without this, the function
won't be able to be called by `aptos move view` or the SDKs.

You can see here we define a function as `public`, which means it can be called by other Move functions
within the Move VM.  You can see it takes a single `address` argument, which determines the location that
the `hello_blockchain` message is stored.  Additionally, you can see `String` which is the return value of
the function.  Lastly, in the function signature `acquires MessageHolder` shows that the function accesses
global state of the `MessageHolder`.

```move
#[view]
/// Reads the message from storage slot
public fun get_message(addr: address): String acquires MessageHolder {
    // ...
}
```

The function body is fairly simple, only 2 lines.  First, there's an `assert!`
statement, which defines an error condition.  The error condition shows that
if the `MessageHolder` is not at the `address`, it will throw the error specified
earlier in the constant.

This is then followed by accessing the message directly from that on-chain state,
and returning a copy to the user.

```move
#[view]
/// Reads the message from storage slot
public fun get_message(addr: address): String acquires MessageHolder {
    assert!(exists<MessageHolder>(addr), error::not_found(E_NO_MESSAGE));
    MessageHolder[addr].message
}
```

> Note that return values of view functions must have the abilities `copy` and `drop`

### Entry Functions and Writing State

Entry functions are the way that users can call a function as a standalone transaction.
The `set_message` function, is denoted in the function signature as `entry` which means
it can be called as an entry function payload, a standalone transaction.

Similar to the `view` function, you will see here, that it has two input arguments.  The
first argujment is the `signer`, which can only be provided by the transaction signature
or similar authorization mechanism.  The `signer` authorizes the function to *move global
state to* the address.  The second argument is a `String` and is the message to be written
to the blockchain.

```move
/// Sets the message to the storage slot
public entry fun set_message(account: signer, message: String) acquires MessageHolder {
```

> Note that an entry function does not always need to be public, it can be `private`, which
> is without the `public` in front.  This can be useful to ensure that the function cannot
> be called from within another Move function.

> Note also that `signer` can also be `&signer`, and as the first argument to the entry function.
> Requiring more than one `signer` as arguments, means that it needs to be a multi-agent transaction,
> or simply signed by more than one party.

Now for the function body, we have a few parts.  We can see that we get the `address` of the account
calling the transaction, the `signer`.  Once we get this address, we can check if the `MessageHolder`
resource (aka struct) is stored in global storage for this account.  If it hasn't been initialized
(there is no resource), we `move_to` the account, a new `MessageHolder` resource.  This adds the
resource to the account to read later, with the initial message.

```move
/// Sets the message to the storage slot
public entry fun set_message(account: signer, message: String) acquires MessageHolder {
    let account_addr = signer::address_of(&account);
    if (!exists<MessageHolder>(account_addr)) {
        move_to(&account, MessageHolder {
            message,
        })
```

Finally, if the resource already exists, we handle it smoothly by just updating the
state of the resource to use the new message.  When we do this, we also emit an event
for easy indexing of changes of the message.

```move
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
```

> Note that the signer is not required to change existing state on a resource.
> This is because only the module that owns the struct can modify the state of
> the resource.  However, the `signer` is always required to authorize storing
> state into an address.

### Unit Tests

Move has native built in unit testing.  To add a test, simply add the `#[test]` annotation
to a function.  As you can see in the function signature, you can define predefined addresses
to create signers for the test.  In this case, the `account` name is shared, and it is creating
a signer for the `0x1` address.  The test can then simply call any of the other functions in the
module, and assert behaviors afterwards.

```
    #[test(account = @0x1)]
    fun sender_can_set_message(account: signer) acquires MessageHolder {
        let msg: String = string::utf8(b"Running test sender_can_set_message...");
        print(&msg);

        let addr = signer::address_of(&account);
        aptos_framework::account::create_account_for_test(addr);
        set_message(account, string::utf8(b"Hello, Blockchain"));

        assert!(get_message(addr) == string::utf8(b"Hello, Blockchain"));
    }
```

> Note that tests can be placed into separate test files in the `tests` folder; However
> private functions cannot be called outside of the same file.  If you want to make test
> only functions that can be used in other modules, simply add the `#[test_only]` annotation.
