## Account Authorization by Signer

### Authorized by a specific account

```move
module deployer::example {

    use aptos_framework::primary_fungible_store;

    const EXAMPLE: vector<u8> = b"example";
    const EXAMPLE_DECIMALS: u8 = 2;

    /// Minting not allowed, must be called by the address 0x42
    const E_NOT_MINTER: u64 = 1;

    struct FAInfo {
        mint_ref: MintRef,
    }

    fun init_module(deployer: &signer) {
        let const_ref = object::create_named_object(
            deployer,
            EXAMPLE
        );
        primary_fungible_store::create_primary_store_enabled_fungible_asset(
            &const_ref,
            option::none(),
            string::utf8(&EXAMPLE),
            string::utf8(&EXAMPLE),
            EXAMPLE_DECIMALS,
            string::utf8(b""),
            string::utf8(b""),
        );

        let mint_ref = fungible_asset::generate_mint_ref(&const_ref);
        move_to(deployer, FAInfo {
            mint_ref
        });
    }

    /// Mints fungible assets to an account, only the account at 0x42 is allowed
    public fun mint(caller: &signer, receiver: address, amount: u64) acquires FAInfo {
        assert!(signer::address_of(caller) == @0x42, E_NOT_MINTER);
        let fa_info = &FAInfo[@deployer];
        primary_fungible_store::mint(&fa_info.mint_ref, receiver, amount)
    }
}
```