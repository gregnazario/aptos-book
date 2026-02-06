# Using Structs to Structure Related Data

A *struct* is a custom data type that lets you package together and name multiple related values that make up a meaningful group. If you're familiar with an object-oriented language, a struct is like the data attributes of an object. In this chapter, we'll compare and contrast structs, demonstrate how to use them, and discuss how structs in Move become powerful resources that represent digital assets.

## Why Structs?

When building smart contracts, you frequently need to group related data together. For example, a user profile might include a name, age, and email address. Rather than managing these as separate variables, a struct lets you combine them into a single, named type.

Move structs are more powerful than structures in many other languages because of the **abilities system**. By assigning different abilities to a struct, you control whether it can be:
- Stored in global storage (`key`)
- Embedded within other structures (`store`)
- Copied (`copy`)
- Automatically destroyed (`drop`)

This fine-grained control is what makes Move's type system uniquely suited for representing digital assets on the blockchain.

## What You'll Learn

In this chapter, we'll cover:

1. **[Defining and Instantiating Structs](basics.md)** - How to declare structs and create instances
2. **[Structs and How They Become Resources](resources.md)** - How abilities transform structs into resources
3. **[Structs and Abilities](abilities.md)** - A deep dive into the four abilities
4. **[Example Program Using Structs](example.md)** - A practical, end-to-end example
5. **[Struct Method Syntax](methods.md)** - How to define methods on structs
