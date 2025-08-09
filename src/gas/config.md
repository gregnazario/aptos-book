# Configuring Gas

There are only 2 knobs you can turn today on Aptos to configure gas cost for a transaction.

- Max gas amount - The number of gas units you are willing to spend on a transaction.
- Gas unit price - The number of octas (APT*10^-8) from a minimum of 100.

## Max gas amount

If a max gas amount is too low for a transaction to complete, `OUT_OF_GAS` will be returned, and the transaction will
abort. This means that nothing will happen in the transaction, but you will still pay the gas. Setting this to a
reasonable bound prevents you from spending too much on a single transaction.

Range: 2 - ??? (TODO: Put number or how to get it from gas config)

If you do not have enough APT to fulfill the gas deposit (max gas amount * gas unit price), you will get an error of
`INSUFFICIENT_BALANCE_FOR_TRANSACTION_FEE`. This means you will need more APT in your account, or to adjust one of these
two values.

## Gas unit price

Gas unit price is the amount you're willing to pay per gas unit on a transaction. Higher values are prioritized over
lower values. When choosing a gas unit price, keep in mind that your account needs enough APT to pay for the entire max
gas amount times the gas unit price.

Range: 100 - ??? (TODO: put number or how to get it from gas config)

## Gas Config

TODO: Explain how to get it directly from on-chain.