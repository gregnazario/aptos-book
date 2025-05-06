# Data Model Tradeoffs

You probably are asking, when would I use one over the other? Here are some details of advantages and disadvantages of
each.

## Account Model

The account model is very simple where each address has direct ownership over its resources. The resources at
that address can only be added with that signer. Keep in mind, we'll mention both user and resource accounts below.

### Account Model Advantages

- User accounts are simple and directly tied to a key.
- Resource accounts are similar to contract addresses in Eth, and can have programmatic access.
- Only the signer associated with the key can write data to the account.
- All resources are indexed by account, and type. Easily accessed automatically in transactions by the signer.
- Creator control over how resources in an account are accessed.
- Ownership based indexing is simple, the account containing the resources is the owner.

### Account Model Disadvantages

- Parallelism is not as easy, requires to ensure that multiple accounts don't access a shared resource.
- No programmatic access except for resource accounts.
- No way to get rid of resources in an account, except through the original contract.

## Object Model

The object model also has each address has resources owned by the owner of the object. This helps provide more complex
ownership models, as well as some tricks for providing composability, and soul-bound resources.

### Object Model Advantages

- Parallelism across objects are easy, just create separate objects for parallel tasks.
- Built in ownership.
- Resources are collected easily in a resource group.
- With the resource group, all resources in the group get written to the write set.
- Multiple resources in the resource group only cause a single storage read (less gas).
- Addresses can be randomly generated or derived from the initial owner for instant access.
- Programmatic signer access.
- Composability is easy, NFTs own other NFTs etc.
- Creator control over ownership, transfers, and other pieces.
- Owner can choose to hide the object, allowing wallets or other items to hide it.

### Object Model Disadvantages

- For full parallelism, addresses need to be stored off-chain and passed into functions,
- Keeping track of objects can be complex.
- More complex access, does require handling ownership or other access actions.
- Soul-bound objects cannot be removed entirely, indexers need to ignore the resources to make them disappear.
- More complex indexing needed to keep track of object owners and properties (especiallly with ownership chains).
