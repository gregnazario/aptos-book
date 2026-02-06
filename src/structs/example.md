# Example Program Using Structs

Let's build a practical example that uses structs to create a simple on-chain address book. This will demonstrate struct definition, creation, storage, reading, updating, and destruction.

## The Address Book Contract

```move
/// A simple on-chain address book that stores contact information.
module my_addr::address_book {
    use std::signer;
    use std::string::String;
    use std::vector;

    /// No address book found for this account
    const E_NO_ADDRESS_BOOK: u64 = 1;
    /// Contact not found in the address book
    const E_CONTACT_NOT_FOUND: u64 = 2;
    /// Address book already exists
    const E_ALREADY_EXISTS: u64 = 3;

    /// A single contact entry
    struct Contact has store, drop, copy {
        name: String,
        phone: String,
    }

    /// The address book resource stored under an account
    struct AddressBook has key {
        contacts: vector<Contact>,
        owner: address,
    }

    /// Create a new address book for the caller
    public entry fun create_address_book(account: &signer) {
        let addr = signer::address_of(account);
        assert!(!exists<AddressBook>(addr), E_ALREADY_EXISTS);
        move_to(account, AddressBook {
            contacts: vector[],
            owner: addr,
        });
    }

    /// Add a contact to the address book
    public entry fun add_contact(
        account: &signer,
        name: String,
        phone: String,
    ) acquires AddressBook {
        let addr = signer::address_of(account);
        assert!(exists<AddressBook>(addr), E_NO_ADDRESS_BOOK);

        let book = &mut AddressBook[addr];
        book.contacts.push_back(Contact { name, phone });
    }

    /// Remove a contact by index
    public entry fun remove_contact(
        account: &signer,
        index: u64,
    ) acquires AddressBook {
        let addr = signer::address_of(account);
        assert!(exists<AddressBook>(addr), E_NO_ADDRESS_BOOK);

        let book = &mut AddressBook[addr];
        assert!(index < book.contacts.length(), E_CONTACT_NOT_FOUND);
        book.contacts.remove(index);
    }

    /// View all contacts
    #[view]
    public fun get_contacts(addr: address): vector<Contact> acquires AddressBook {
        assert!(exists<AddressBook>(addr), E_NO_ADDRESS_BOOK);
        AddressBook[addr].contacts
    }

    /// View the number of contacts
    #[view]
    public fun contact_count(addr: address): u64 acquires AddressBook {
        assert!(exists<AddressBook>(addr), E_NO_ADDRESS_BOOK);
        AddressBook[addr].contacts.length()
    }

    /// Remove the address book entirely
    public entry fun delete_address_book(account: &signer) acquires AddressBook {
        let addr = signer::address_of(account);
        assert!(exists<AddressBook>(addr), E_NO_ADDRESS_BOOK);
        let AddressBook { contacts: _, owner: _ } = move_from<AddressBook>(addr);
    }

    // ---- Tests ----

    #[test(account = @0x1)]
    fun test_create_and_add_contact(account: &signer) acquires AddressBook {
        let addr = signer::address_of(account);

        create_address_book(account);
        assert!(exists<AddressBook>(addr));
        assert!(contact_count(addr) == 0);

        add_contact(
            account,
            std::string::utf8(b"Alice"),
            std::string::utf8(b"555-1234"),
        );
        assert!(contact_count(addr) == 1);

        let contacts = get_contacts(addr);
        let first = contacts[0];
        assert!(first.name == std::string::utf8(b"Alice"));
    }

    #[test(account = @0x1)]
    fun test_delete_address_book(account: &signer) acquires AddressBook {
        let addr = signer::address_of(account);
        create_address_book(account);
        assert!(exists<AddressBook>(addr));

        delete_address_book(account);
        assert!(!exists<AddressBook>(addr));
    }

    #[test(account = @0x1)]
    fun test_remove_contact(account: &signer) acquires AddressBook {
        let addr = signer::address_of(account);
        create_address_book(account);
        add_contact(account, std::string::utf8(b"Alice"), std::string::utf8(b"555-1234"));
        add_contact(account, std::string::utf8(b"Bob"), std::string::utf8(b"555-5678"));
        assert!(contact_count(addr) == 2);

        remove_contact(account, 0);
        assert!(contact_count(addr) == 1);
    }

    #[test(account = @0x1)]
    #[expected_failure(abort_code = E_ALREADY_EXISTS)]
    fun test_double_create_fails(account: &signer) {
        create_address_book(account);
        create_address_book(account);
    }

    #[test(account = @0x1)]
    #[expected_failure(abort_code = E_CONTACT_NOT_FOUND)]
    fun test_remove_invalid_index_fails(account: &signer) acquires AddressBook {
        create_address_book(account);
        remove_contact(account, 0); // No contacts -- should fail
    }
}
```

## Breakdown

### Struct Design

- **`Contact`** has `store`, `drop`, and `copy` -- it is a lightweight data value that can be freely duplicated and is embeddable inside other stored types.
- **`AddressBook`** has only `key` -- it is a resource that lives in global storage and cannot be copied or accidentally dropped.

### Entry Functions

- `create_address_book` stores a new empty address book under the caller's account.
- `add_contact` appends a contact to the caller's existing address book.
- `remove_contact` removes a contact by index, using `E_CONTACT_NOT_FOUND` if the index is out of bounds.
- `delete_address_book` removes and destructures the resource, freeing the storage slot.

### View Functions

- `get_contacts` returns a copy of all contacts.
- `contact_count` returns the number of contacts.

### Error Handling

Each function validates preconditions with `assert!` and descriptive error codes. This is a best practice for all Move contracts.

### Tests

The test functions verify the full lifecycle: creation, modification, reading, and deletion. The `#[expected_failure]` test ensures that duplicate creation is properly rejected.

## Key Takeaways

1. **Structs model your domain**: Use them to represent entities and their relationships.
2. **Abilities control behavior**: Choose abilities carefully to enforce safety properties.
3. **Resources live in global storage**: Use `move_to`, `move_from`, and borrowing operations.
4. **Test everything**: Move's built-in testing makes it easy to verify correctness.
