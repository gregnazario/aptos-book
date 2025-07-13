# Resource Types

Resources are a fundamental concept in Move that represents digital assets on the blockchain. They are special types that cannot be copied or dropped, ensuring that digital assets are always accounted for and cannot be accidentally lost or duplicated.

## What Are Resources?

Resources are Move's way of representing digital assets like coins, tokens, NFTs, or any other valuable data that should be treated with special care. They have unique properties that make them different from regular values:

- **Cannot be copied**: Resources represent unique assets that cannot be duplicated
- **Cannot be dropped**: Resources must be explicitly handled, never accidentally destroyed
- **Must be moved**: Resources can only be transferred from one owner to another
- **Global storage**: Resources are typically stored in global storage under specific addresses

## Resource Abilities

Resources have specific abilities that define their behavior:

```move
module my_module::resource_abilities {
    // Resources have key and store abilities
    struct Coin has key, store {
        value: u64,
    }
    
    // Regular values can have copy and drop abilities
    struct Metadata has copy, drop, store {
        name: String,
        symbol: String,
    }
}
```

### Key Ability

The `key` ability allows a type to be used as a key in global storage. This means resources can be stored under specific addresses.

### Store Ability

The `store` ability allows a type to be stored in global storage. Resources need this to persist on the blockchain.

### No Copy or Drop

Resources cannot have the `copy` or `drop` abilities, which prevents them from being duplicated or accidentally destroyed.

## Creating Resources

Resources are typically created through specific functions and immediately stored in global storage:

```move
module my_module::resource_creation {
    struct Coin has key, store {
        value: u64,
    }
    
    public fun create_coin(account: &signer, value: u64) {
        let coin = Coin { value };
        move_to(account, coin);  // Store in global storage
    }
    
    public fun create_coin_and_return(value: u64): Coin {
        Coin { value }  // Return resource to caller
    }
}
```

## Storing Resources

Resources are stored in global storage using the `move_to` function:

```move
module my_module::resource_storage {
    struct UserProfile has key, store {
        name: String,
        age: u8,
        coins: u64,
    }
    
    public fun create_profile(account: &signer, name: String, age: u8) {
        let profile = UserProfile {
            name,
            age,
            coins: 0,
        };
        move_to(account, profile);  // Store under account address
    }
    
    public fun add_coins(account: &signer, amount: u64) {
        let profile = borrow_global_mut<UserProfile>(signer::address_of(account));
        profile.coins = profile.coins + amount;
    }
}
```

## Accessing Resources

Resources stored in global storage can be accessed using borrowing functions:

```move
module my_module::resource_access {
    struct Coin has key, store {
        value: u64,
    }
    
    // Immutable access
    public fun get_coin_value(addr: address): u64 {
        let coin = borrow_global<Coin>(addr);
        coin.value
    }
    
    // Mutable access
    public fun increase_coin_value(addr: address, amount: u64) {
        let coin = borrow_global_mut<Coin>(addr);
        coin.value = coin.value + amount;
    }
    
    // Check if resource exists
    public fun has_coin(addr: address): bool {
        exists<Coin>(addr)
    }
}
```

## Moving Resources

Resources can be moved out of global storage using `move_from`:

```move
module my_module::resource_movement {
    struct Coin has key, store {
        value: u64,
    }
    
    public fun withdraw_coin(account: &signer, amount: u64): Coin {
        let coin = move_from<Coin>(signer::address_of(account));
        
        if (coin.value > amount) {
            // Split the coin
            let (withdrawn, remaining) = split_coin(coin, amount);
            // Return remaining coin to storage
            move_to(account, remaining);
            withdrawn
        } else {
            coin
        }
    }
    
    fun split_coin(coin: Coin, amount: u64): (Coin, Coin) {
        assert!(coin.value >= amount, 0);
        (Coin { value: amount }, Coin { value: coin.value - amount })
    }
}
```

## Resource Safety

Move's type system ensures resource safety through several mechanisms:

### No Accidental Copying

```move
module my_module::no_copying {
    struct Token has key, store {
        id: u64,
        owner: address,
    }
    
    public fun token_safety() {
        let token = Token { id: 1, owner: @0x1 };
        
        // This would cause a compilation error:
        // let token_copy = token;  // Cannot copy a resource
        
        // Instead, move the resource
        move_to(&account, token);
    }
}
```

### No Accidental Dropping

```move
module my_module::no_dropping {
    struct Coin has key, store {
        value: u64,
    }
    
    public fun coin_safety() {
        let coin = Coin { value: 100 };
        
        // This would cause a compilation error:
        // coin;  // Cannot drop a resource
        
        // Must explicitly handle the resource
        move_to(&account, coin);
    }
}
```

### Explicit Resource Handling

```move
module my_module::explicit_handling {
    struct Coin has key, store {
        value: u64,
    }
    
    public fun handle_coin(account: &signer, coin: Coin) {
        // Must explicitly decide what to do with the resource
        if (coin.value > 0) {
            move_to(account, coin);  // Store it
        } else {
            // Cannot drop, so must handle somehow
            // This would cause a compilation error:
            // coin;
            
            // Instead, maybe destroy it through a specific function
            destroy_zero_coin(coin);
        }
    }
    
    fun destroy_zero_coin(coin: Coin) {
        // This function can destroy the resource because it's designed for it
        // The resource is consumed and not returned
    }
}
```

## Resource Patterns

### Resource as Digital Asset

```move
module my_module::digital_asset {
    struct NFT has key, store {
        id: u64,
        owner: address,
        metadata: String,
    }
    
    public fun mint_nft(account: &signer, id: u64, metadata: String) {
        let nft = NFT {
            id,
            owner: signer::address_of(account),
            metadata,
        };
        move_to(account, nft);
    }
    
    public fun transfer_nft(from: &signer, to: address, nft_id: u64) {
        let nft = move_from<NFT>(signer::address_of(from));
        assert!(nft.id == nft_id, 0);
        nft.owner = to;
        // Note: In practice, you'd need to handle the transfer to the new owner
        // This is a simplified example
    }
}
```

### Resource as State Container

```move
module my_module::state_container {
    struct GameState has key, store {
        player: address,
        score: u64,
        level: u8,
        inventory: vector<String>,
    }
    
    public fun create_game(account: &signer) {
        let game_state = GameState {
            player: signer::address_of(account),
            score: 0,
            level: 1,
            inventory: vector::empty<String>(),
        };
        move_to(account, game_state);
    }
    
    public fun update_score(account: &signer, points: u64) {
        let game_state = borrow_global_mut<GameState>(signer::address_of(account));
        game_state.score = game_state.score + points;
    }
}
```

### Resource as Access Control

```move
module my_module::access_control {
    struct AdminCap has key, store {
        admin: address,
    }
    
    public fun create_admin(account: &signer) {
        let admin_cap = AdminCap {
            admin: signer::address_of(account),
        };
        move_to(account, admin_cap);
    }
    
    public fun admin_only_function(admin: &signer) {
        let admin_cap = borrow_global<AdminCap>(signer::address_of(admin));
        assert!(admin_cap.admin == signer::address_of(admin), 0);
        
        // Perform admin-only operation
    }
}
```

## Resource Best Practices

### Design Resources Carefully

```move
module my_module::resource_design {
    // Good: Clear resource structure
    struct Token has key, store {
        id: u64,
        owner: address,
        metadata: String,
        created_at: u64,
    }
    
    // Good: Separate concerns
    struct TokenMetadata has copy, drop, store {
        name: String,
        symbol: String,
        decimals: u8,
    }
    
    // Bad: Mixing resource and regular data
    // struct BadToken has key, store, copy {  // Cannot have copy
    //     id: u64,
    //     owner: address,
    // }
}
```

### Handle Resources Explicitly

```move
module my_module::explicit_handling {
    struct Coin has key, store {
        value: u64,
    }
    
    public fun process_coin(coin: Coin): Coin {
        // Must return the resource - cannot drop it
        if (coin.value > 100) {
            // Process large coin
            coin
        } else {
            // Process small coin
            coin
        }
    }
    
    public fun destroy_coin(coin: Coin) {
        // This function consumes the resource
        // The resource is not returned, so it's effectively destroyed
        // This is only acceptable if the function is designed for destruction
    }
}
```

### Use Resource Abilities Appropriately

```move
module my_module::ability_usage {
    // Resources should have key and store
    struct Resource has key, store {
        data: u64,
    }
    
    // Regular data can have copy and drop
    struct RegularData has copy, drop, store {
        data: u64,
    }
    
    // Temporary data can have drop only
    struct TempData has drop {
        buffer: vector<u8>,
    }
}
```

## Common Resource Patterns

### Resource Factory

```move
module my_module::resource_factory {
    struct Factory has key, store {
        total_created: u64,
    }
    
    struct Product has key, store {
        id: u64,
        factory: address,
    }
    
    public fun create_factory(account: &signer) {
        let factory = Factory { total_created: 0 };
        move_to(account, factory);
    }
    
    public fun create_product(account: &signer): Product {
        let factory = borrow_global_mut<Factory>(signer::address_of(account));
        factory.total_created = factory.total_created + 1;
        
        Product {
            id: factory.total_created,
            factory: signer::address_of(account),
        }
    }
}
```

### Resource Collection

```move
module my_module::resource_collection {
    struct Collection has key, store {
        items: vector<u64>,
    }
    
    struct Item has key, store {
        id: u64,
        collection: address,
    }
    
    public fun create_collection(account: &signer) {
        let collection = Collection { items: vector::empty<u64>() };
        move_to(account, collection);
    }
    
    public fun add_item(account: &signer, item: Item) {
        let collection = borrow_global_mut<Collection>(signer::address_of(account));
        vector::push_back(&mut collection.items, item.id);
        // Note: item would need to be handled appropriately
    }
}
```

## Resource Safety Guarantees

Move's resource system provides several safety guarantees:

1. **No Double-Spending**: Resources cannot be copied, preventing double-spending attacks
2. **No Accidental Loss**: Resources cannot be dropped accidentally
3. **Explicit Ownership**: All resource transfers are explicit and visible
4. **Type Safety**: The type system ensures resources are handled correctly
5. **Storage Safety**: Resources in global storage are protected by the type system

Understanding resource types is essential for building secure and reliable smart contracts on Move. Resources represent the core concept of digital assets and provide the foundation for building complex financial applications on the blockchain.
