# Parallelization Basics

BlockSTM is the parallel execution engine that drives Aptos.  It uses what we call dynamic (or optimistic) parallelism.  What this means is that all transactions are executed in parallel, and the write sets between each are compared.  If they write (and then read or write) to the same storage slot, it's a conflict, and therefore those transactions must be serialized.

TODO: GIF of block STM
