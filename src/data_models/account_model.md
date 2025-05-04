# The Account Model

The Account model of Aptos behaves where each user has their data stored in global storage. Think of this as a giant
mapping between the set of `Address` and `Resource Name` to a single storage slot.

TODO: Diagram

There are two types of accounts today:

- [User Accounts](#user-accounts)
- [Resource Accounts](#resource-accounts)

## User Accounts

User accounts are the standard accounts that users create to interact with the Aptos blockchain. They are
denoted by the resource `0x1::account::Account` and are used to hold assets, execute transactions, and interact with
smart contracts. They are generated from a signer and are associated with a public key. The public key is then hashed
to create the account address.

## Resource Accounts

Resource accounts are accounts that are separate of a user account. The accounts are derived from an
existing account, and can have a `SignerCapability` stored in order to sign as the account. Alternatively, the signer
can be rotated to `0x0` preventing anyone from authenticating as an account.