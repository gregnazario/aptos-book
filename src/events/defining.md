# Defining and Emitting Events

## Choosing your events

There are two types of events: handle events and module events.

> Note that, handle events are mostly deprecated except in some situations, and are not parallelizable.  For this reason, I will only go over module events in this book.

## Module Events

To define a module event in Move, you simply need to add a `#[event]` annotation above the struct you want to be an event.  Then call `emit` for each one you want to emit.  Here's an example:

```move
module my_addr::my_module {
    use std::signer;
    use std::string::String;

    #[event]
    struct Message {
        caller: address,
        inner: String
    }

    entry fun emit_message(caller: &signer, message: String) {
        aptos_framework::event::emit(Message {
            caller: signer::address_of(caller),
            inner: message
        })
    }
}
```

This will emit a message, which will show up in the writeset for later indexing.

> Note that the events do not have a sequence number.
