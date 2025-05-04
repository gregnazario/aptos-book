# Gas

Gas is used to measure the amount of execution, storage, and IO used for every transaction. This is to provide fairness
and ensure the network runs smoothly and with high performance. Gas cost for a transaction has three parts:

- The gas used - which is the amount of units used to execute the transaction (execution, storage, and IO).
- The gas unit price (also sometimes called price per unit gas) - which is the amount the fee payer chose to pay to
  prioritize the transaction.
- The storage refund - which is based on the number of storage slots deleted.

The total gas cost (fee or refund) is calculated as:
TODO: Add LaTeX to make this nicer

```
(gas used x gas unit price) + storage refund = total gas
```

Keep in mind, the storage refund can be greater than the other side, so you can actually gain gas in a transaction by
freeing storage slots.

## How is gas used calculated?

Gas used is calculated by three parts:

1. The number of [execution units](execution.md), which vary based on the operations taken.
2. The number of [IO units](io.md), which vary based on which storage slots are read or written.
3. The [storage deposit](storage.md), which is the cost for each new storage slot created. Storage deposit is returned
   to users.

Each one of these has an individual upper bound, so keep that in mind if you have a task that uses any one of these
heavily.