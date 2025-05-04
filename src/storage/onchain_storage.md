# On-chain Storage

On-chain Rocks DB uses a concept of storage slots. The storage slots are accessible storage, and each slot has an
associated cost with it. The slots are accessible by a hash of given inputs.

There are a few types:

- Resources
- Resource Groups
- Tables
- TODO: Vectors, BigVectors, SimpleMap, OrderedMap, BigOrderedMap, etc.

## Resources

Resource storage a single slot is the combination of _address_ and _resource name_. This combination gives a single
slot, which storing a lot of data in that resource, can be efficient.

TODO: Diagram

Keep in mind that the storage deposit associated with a resource is a single slot per resource.

## Resource Groups

As specified in [AIP-XX](todo.md), resource groups are a collection of resources in a single storage slot. These are
stored as a b-tree, in the storage slot, which allows for more efficient packing of data (fewer slots). This is a slight
tradeoff where, if accessing multiple resources together often, will be much more efficient, but all writes send all
resources in the group to the output writeset. There is also slight cost to navigate the b-tree.

TODO: Diagram

The most common usage for resource groups is for the `0x1::object::ObjectGroup` group for objects.

## Tables

Tables are hash addressable storage based on a handle stored in a resource. Each item in a table is a single storage
slot, but with the advantage that has less execution cost associated. Additionally, each storage slot can be
parallelized separately. Note that by far tables are the most expensive, as you need to store both the slot for the
handle and the slot for each individual table item. The basic table handle cannot be deleted, but the table items can
be. The cost of the table handle's slot cannot be recovered via storage refund.

TODO: Diagram

Note that there is no indexed tracking of which table items are filled or not and how many there are, this must be done
off-chain or with a different table variant.

There are other variants of the table with different tradeoffs:

- Table with length
- Smart Table

### Table With Length

Table with length is exactly the same as a table, but with a length value. Keep in mind that table with length can be
deleted fully including the table handle. However, table with length is not parallelizable on creation or deletion of
table items, because every transaction increments or decrements the length.

TODO: Diagram

### Smart Table

Smart table uses buckets to lower the number of storage slots used. It keeps track of the length, and it buckets items
into vectors. It is additionally iterable over the course of the whole table.

TODO: Diagram

Note: there is a possible DDoS vector if people can create keys that end up in a single storage item.