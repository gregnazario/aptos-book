# Parallelization Basics

BlockSTM is the parallel execution engine that drives Aptos.  It uses what we call dynamic (or optimistic) parallelism.  What this means is that all transactions are executed in parallel, and the write sets between each are compared.  If they write (and then read or write) to the same storage slot, it's a conflict, and therefore those transactions must be serialized.

## How BlockSTM Works

1. **Optimistic Execution**: All transactions in a block are executed in parallel, assuming no conflicts. When all transactions complete without conflicts, the entire block can be committed without any re-execution -- this is the ideal case that BlockSTM is optimized for.
2. **Validation**: After execution, the read/write sets of each transaction are compared.
3. **Conflict Detection**: If transaction B reads a storage slot that transaction A wrote to, and A comes before B in the block ordering, this is a conflict.
4. **Re-execution**: Conflicting transactions are re-executed with the updated state.
5. **Commitment**: Once all transactions are validated, the block is committed.

This approach achieves near-linear scaling with the number of CPU cores when transactions access independent state, which is the common case for most blockchain workloads.
