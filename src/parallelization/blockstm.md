# Block-STM

Block-STM is an optimistic parallel execution engine that runs transactions speculatively, validates their read and write sets, and re-executes only the ones that conflict. This approach enables high throughput for the Aptos blockchain by keeping cores busy while preserving deterministic results.

![Animated view of Block-STM](./blockstm-animation.svg)

## References

- [Block-STM: How We Execute Over 160k Transactions Per Second on the Aptos Blockchain](https://medium.com/aptoslabs/block-stm-how-we-execute-over-160k-transactions-per-second-on-the-aptos-blockchain-3b003657e4ba)
- [Block-STM blog article](https://blog.chain.link/block-stm/)
- [Block-STM research paper](https://arxiv.org/abs/2203.06871)
