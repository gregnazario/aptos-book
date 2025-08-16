# Parallelization Considerations

When considering code on Aptos for parallelization, think of these three things:

1. Where will the most conflicts occur on my codebase?
2. Can I use different accounts or addresses to ensure that there are reduced conflicts?
3. Can I use separate storage slots (such as a table or objects) to ensure that there are reduced conflicts?
4. Can I use an aggregator instead for my conflicting read / writes to a single number?
