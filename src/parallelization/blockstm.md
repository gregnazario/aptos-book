# Block-STM

Block-STM is an optimistic parallel execution engine developed by Aptos Labs. It
runs transactions speculatively across multiple threads, validates their read and
write sets, and re-executes only the ones whose reads were invalidated by an
earlier transaction's writes. This approach keeps all available CPU cores busy
while still producing deterministic, serializable results identical to sequential
execution.

## How It Works

1. **Speculative Execution** — All transactions in a block are dispatched to
   worker threads in parallel. Each transaction optimistically reads the latest
   committed values and records its read-set and write-set.
2. **Validation** — After execution, the scheduler checks whether any value the
   transaction read has since been overwritten by a lower-indexed transaction.
   If the read-set is still consistent, validation passes.
3. **Re-execution** — When validation fails (a *conflict*), the transaction is
   re-executed with the updated values. Only conflicting transactions pay this
   cost; the rest proceed to commit.
4. **Commit** — Validated transactions commit in the original block order,
   ensuring deterministic output regardless of how threads were scheduled.

The animation below illustrates five transactions flowing through these stages.
**Tx 2** experiences a conflict during validation (its read-set was invalidated
by Tx 1's writes), so it re-executes before committing.

![Animated view of Block-STM parallel execution pipeline](./blockstm-animation.svg)

## Why It Matters

In workloads where most transactions touch different state (e.g., independent
token transfers), nearly all transactions validate on the first attempt and the
block executes in close to wall-clock time of a single transaction. Even under
contention, Block-STM gracefully falls back toward sequential performance rather
than producing incorrect results. This makes it one of the key reasons Aptos
achieves high throughput — over **160,000 transactions per second** in
benchmarks.

## References

- [Block-STM: How We Execute Over 160k Transactions Per Second on the Aptos Blockchain](https://medium.com/aptoslabs/block-stm-how-we-execute-over-160k-transactions-per-second-on-the-aptos-blockchain-3b003657e4ba)
- [Block-STM blog article](https://blog.chain.link/block-stm/)
- [Block-STM research paper (arXiv)](https://arxiv.org/abs/2203.06871)
