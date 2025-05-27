# Introduction

The Aptos book is an extension to the source documentation in the Move book. The purpose of the Aptos book is to
provide a single resource for design patterns, usage, and other resources for building on Aptos. This should only be
providing context for how to build on Aptos, and anything needed for that. The additional benefit is that it can be run
entirely offline, for other locations.

# Get Started

How to use this book, there are different sections to skip ahead for different topics. However, it is mostly built in an
opinionated way where the reader first learns about the building blocks of Aptos, and builds up to writing Move
contracts on top.

It's suggested to learn in this order:

- [Binary Canonical Serialization (BCS)](bcs/intro.md) - How data is serialized in Move on Aptos
- [Storage](storage/intro.md) - How data is stored on Aptos
- [Data models](data_models/intro.md) - How data is modeled on Aptos
- [Gas](gas/intro.md) - How execution and storage are charged on Aptos
- [Move](move/intro.md) - How smart contracts are built, syntax and others
- [Standard Libraries](standard_libraries/intro.md) - Standard libraries for building smart contracts
- [Learning Resources](resources.md) - More resources to learn more about Aptos and Move

If you learn better from examples, [Aptos By Example](aptos_by_example/intro.md) will be a better bet for you.

# Contribution

Please feel free to open a GitHub issue to add more information into each of these sections. All pull requests must:

1. Define the section that it is updating
2. Provide a concise description of the change
3. Callout any missing areas
