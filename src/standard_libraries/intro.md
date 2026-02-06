# Standard Libraries

Aptos provides multiple standard libraries at the given addresses:

- 0x1
    - [MoveStdLib](move_stdlib.md)
    - [AptosStdLib](aptos_stdlib.md)
    - [AptosFramework](aptos_framework.md)
- 0x3
    - AptosToken - Legacy NFT standard (not suggested for any future usage)
- 0x4
    - AptosTokenObjects - Digital Assets -> New NFT and semi-fungible token standard

## Standards

These standards are built into the 0x1 and 0x4 addresses:

- Fungible Tokens
    - [Coins (Legacy)](fungible_tokens/coin.md)
    - [Fungible Assets](fungible_tokens/fungible_assets.md)
- Non-fungible and Semi-fungible Tokens
    - [Digital Assets](non_fungible_tokens/digital_assets.md)

# Additional Libraries

The Aptos ecosystem also has third-party libraries and tools:

- [Aptos Token Objects](https://github.com/aptos-labs/aptos-framework/tree/main/aptos-move/framework/aptos-token-objects) -- The modern NFT and semi-fungible token framework
- [Pyth Network](https://pyth.network/) -- Price oracle data feeds
- [Switchboard](https://switchboard.xyz/) -- Decentralized oracle network
- [Econia](https://github.com/econia-labs/econia) -- On-chain order book DEX protocol