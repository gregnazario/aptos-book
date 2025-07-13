# Ownership Basics

Understanding the basics of ownership is crucial for writing Move code. This section covers the fundamental rules and concepts that govern how ownership works in Move.

## What is Ownership?

Ownership is Move's most distinctive feature and the key to its memory safety guarantees. The ownership system consists of a set of rules that the compiler checks at compile time. No runtime overhead is incurred for any of the ownership features.

## The Rules of Ownership

1. **Each value has a variable that's called its owner**
2. **There can only be one owner at a time**
3. **When the owner goes out of scope, the value will be dropped**

Let's explore these rules through examples.

## Variable Scope

A scope is the range within a program for which an item is valid. Let's look at an example:

```move
module my_module::scope_example {
    public fun scope_demo() {
        // s is not valid here, it's not yet declared
        let s = string::utf8(b"hello");   // s is valid from this point forward

        // do stuff with s
        let len = string::length(&s);
    }   // this scope is now over, and s is no longer valid
}
```

In other words, there are two important points in time here:
- When `s` comes into scope, it is valid
- It remains valid until it goes out of scope

## The String Type

To illustrate the rules of ownership, we need a more complex data type than the ones we covered in the previous sections. The types covered previously are all a known size, can be stored on the stack and popped off the stack when their scope is over, and can be quickly and trivially copied to make a new, independent instance if another part of code needs to use the same value in a different scope.

But we want to look at data that is stored on the heap and explore how Move knows when to clean up that data, and the `String` type is a perfect example. We'll concentrate on the parts of `String` that relate to ownership. These aspects also apply to other complex data types, whether they are provided by the standard library or created by you.

## Memory and Allocation

In the case of a string literal, we know the contents at compile time, so the text is hardcoded directly into the final executable. This is why string literals are fast and efficient. But these properties only come from the string literal's immutability. Unfortunately, we can't put a blob of memory into the binary for each piece of text whose size is unknown at compile time and whose size might change while running the program.

With the `String` type, in order to support a mutable, growable piece of text, we need to allocate an amount of memory on the heap, unknown at compile time, to hold the contents. This means:

- The memory must be requested from the memory allocator at runtime
- We need a way of returning this memory to the allocator when we're done with our `String`

The first part is done by us: when we call `string::utf8()`, its implementation requests the memory it needs. This is pretty much universal in programming languages.

However, the second part is different. In languages with a garbage collector (GC), the GC keeps track of and cleans up memory that isn't being used anymore, and we don't need to think about it. In most languages without a GC, it's our responsibility to identify when memory is no longer being used and call code to explicitly return it, just as we did to request it. Doing this correctly has historically been a difficult programming problem. If we forget, we'll waste memory. If we do it too early, we'll have an invalid variable. If we do it twice, that's a bug too. We need to pair exactly one `allocate` with exactly one `free`.

Move takes a different path: the memory is automatically returned once the variable that owns it goes out of scope. Here's a version of our scope example using a `String` instead of a string literal:

```move
module my_module::string_scope {
    public fun string_scope_demo() {
        let s = string::utf8(b"hello");   // s comes into scope

        // do stuff with s
        let len = string::length(&s);
    }   // this scope is now over, and s is no longer valid
}
```

There is a natural point at which we can return the memory our `String` needs to the allocator: when `s` goes out of scope. When a variable goes out of scope, Move calls a special function for us. This function is called `drop`, and it's where the author of `String` can put the code to return the memory. Move calls `drop` automatically at the closing curly bracket.

## Ways Variables and Data Interact: Move

Multiple variables can interact with the same data in different ways in Move. Let's look at an example using an integer:

```move
module my_module::move_example {
    public fun move_demo() {
        let x = 5;
        let y = x;
    }
}
```

We can probably guess what this is doing: "bind the value `5` to `x`; then make a copy of the value in `x` and bind it to `y`." We now have two variables, `x` and `y`, and both equal `5`. This is indeed what is happening, because integers are simple values with a known, fixed size, and these two `5` values are pushed onto the stack.

Now let's look at the `String` version:

```move
module my_module::string_move {
    public fun string_move_demo() {
        let s1 = string::utf8(b"hello");
        let s2 = s1;
    }
}
```

This looks very similar to the previous code, so we might assume that the second line would make a copy of the value in `s1` and bind it to `s2`. But this isn't quite what happens.

To explain what happens, we need to look at what a `String` looks like under the hood. A `String` is made up of three parts, shown on the left: a pointer to the memory that holds the contents of the string, a length, and a capacity. This group of data is stored on the stack. On the right is the memory on the heap that holds the contents.

When we assign `s1` to `s2`, the `String` data is copied, meaning we copy the pointer, the length, and the capacity that are on the stack. We do not copy the data on the heap that the pointer refers to. In other words, the data representation in memory looks like this:

```
s1: [ptr | len | cap] -> "hello" (on heap)
s2: [ptr | len | cap] -> "hello" (on heap)
```

The representation is not like this, which is what memory would look like if Move instead copied the heap data as well:

```
s1: [ptr | len | cap] -> "hello" (on heap)
s2: [ptr | len | cap] -> "hello" (on heap)  // This is NOT what happens
```

If Move had done this, the operation `let s2 = s1;` could be very expensive in terms of runtime performance if the data on the heap was large.

Earlier, we said that when a variable goes out of scope, Move automatically calls the `drop` function and cleans up the heap memory for that variable. But Figure 4-2 shows both data pointers pointing to the same location. This is a problem: when `s2` and `s1` go out of scope, they will both try to free the same memory. This is known as a double free error and is one of the memory safety bugs we mentioned previously. Freeing memory twice can lead to memory corruption, which can potentially lead to security vulnerabilities.

To ensure memory safety, after the line `let s2 = s1;`, Move considers `s1` as no longer valid. Therefore, Move doesn't need to free anything when `s1` goes out of scope. Check out what happens when you try to use `s1` after `s2` is created; it won't work:

```move
module my_module::invalid_use {
    public fun invalid_use_demo() {
        let s1 = string::utf8(b"hello");
        let s2 = s1;
        
        // This would cause a compilation error:
        // let len = string::length(&s1);
    }
}
```

If you've heard the terms shallow copy and deep copy while working with other languages, the concept of copying the pointer, length, and capacity without copying the data probably sounds like making a shallow copy. But because Move also invalidates the first variable, instead of being called a shallow copy, it's known as a move. In this example, we would say that `s1` was moved into `s2`. So what actually happens is shown in Figure 4-4.

That solves our problem! With only `s2` valid, when it goes out of scope, it alone will free the memory, and we're done.

In addition, there's a design choice that's implied by this: Move will never automatically create "deep" copies of your data. Therefore, any automatic copying can be assumed to be inexpensive in terms of runtime performance.

## Variables and Data Interacting with Clone

If we do want to deeply copy the heap data of the `String`, not just the stack data, we can use a common method called `clone`. We'll discuss method syntax in Chapter 5, but because methods are a common feature in many programming languages, you've probably seen them before.

Here's an example of the `clone` method in action:

```move
module my_module::clone_example {
    public fun clone_demo() {
        let s1 = string::utf8(b"hello");
        let s2 = string::clone(&s1);
        
        // Now both s1 and s2 are valid
        let len1 = string::length(&s1);
        let len2 = string::length(&s2);
    }
}
```

This works just fine and explicitly produces the behavior shown in Figure 4-3, where the heap data does get copied.

When you see a call to `clone`, you know that some arbitrary code is being executed and that code may be expensive. It's a visual indicator that something different is going on.

## Stack-Only Data: Copy

There's another wrinkle we haven't talked about yet. This code using integers works and is valid:

```move
module my_module::copy_example {
    public fun copy_demo() {
        let x = 5;
        let y = x;
        
        // Both x and y are valid here
        let sum = x + y;
    }
}
```

But this code seems to contradict what we just learned: we don't have a call to `clone`, but `x` is still valid and wasn't moved into `y`.

The reason is that types such as integers that have a known size at compile time are stored entirely on the stack, so copies of the actual values are quick to make. That means there's no reason we would want to prevent `x` from being valid after we create the variable `y`. In other words, there's no difference between deep and shallow copying here, so calling `clone` wouldn't create anything different from the usual shallow copying, and we can leave it out.

Move has a special annotation called the `copy` ability that we can place on types like integers that are stored on the stack (we'll talk more about abilities in Chapter 10). If a type has the `copy` ability, an older variable is still usable after assignment. Move won't let us annotate a type with `copy` if the type, or any of its parts, has implemented the `drop` ability. If the type needs something special to happen when the value goes out of scope and we add the `copy` annotation to that type, we'll get a compile-time error.

So what types have the `copy` ability? You can check the documentation for the given type to be sure, but as a general rule, any group of simple scalar values can have `copy`, and nothing that requires allocation or is some form of resource can have `copy`. Here are some types that have `copy`:

- All the integer types, such as `u32`
- The Boolean type, `bool`
- The address type, `address`
- All floating point types, such as `f64`
- Tuples, if they only contain types that also have `copy`. For example, `(u32, u64)` has `copy`, but `(u32, String)` does not

## Ownership and Functions

The semantics for passing a value to a function are similar to those for assigning a value to a variable. Passing a variable to a function will move or copy, just as assignment does. Here's an example with some annotations showing where variables go into and out of scope:

```move
module my_module::function_ownership {
    public fun function_ownership_demo() {
        let s = string::utf8(b"hello");  // s comes into scope

        takes_ownership(s);             // s's value moves into the function...
                                        // ... and so is no longer valid here

        let x = 5;                      // x comes into scope

        makes_copy(x);                  // x would move into the function,
                                        // but u64 is Copy, so it's okay to still
                                        // use x afterward
    } // Here, x goes out of scope, then s. But because s's value was moved, nothing
      // special happens.

    fun takes_ownership(some_string: String) { // some_string comes into scope
        let len = string::length(&some_string);
    } // Here, some_string goes out of scope and `drop` is called. The backing
      // memory is freed.

    fun makes_copy(some_integer: u64) { // some_integer comes into scope
        let doubled = some_integer * 2;
    } // Here, some_integer goes out of scope. Nothing special happens.
}
```

If we tried to use `s` after the call to `takes_ownership`, Move would throw a compile-time error. These static checks protect us from mistakes. Try adding code to `main` that uses `s` and `x` to see where you can use them and where the ownership rules prevent you from doing so.

## Return Values and Scope

Returning values can also transfer ownership. Here's an example with similar annotations:

```move
module my_module::return_ownership {
    public fun return_ownership_demo() {
        let s1 = gives_ownership();         // gives_ownership moves its return
                                            // value into s1

        let s2 = string::utf8(b"hello");     // s2 comes into scope

        let s3 = takes_and_gives_back(s2);  // s2 is moved into
                                            // takes_and_gives_back, which also
                                            // moves its return value into s3
    } // Here, s3 goes out of scope and is dropped. s2 was moved, so nothing
      // happens. s1 goes out of scope and is dropped.

    fun gives_ownership() -> String {             // gives_ownership will move its
                                                 // return value into the function
                                                 // that calls it

        let some_string = string::utf8(b"hello"); // some_string comes into scope

        some_string                              // some_string is returned and
                                                 // moves out to the calling
                                                 // function
    }

    // This function takes a String and returns one
    fun takes_and_gives_back(a_string: String) -> String { // a_string comes into
                                                          // scope

        a_string  // a_string is returned and moves out to the calling function
    }
}
```

The ownership of a variable follows the same pattern every time: assigning a value to another variable moves it. When a variable that includes data on the heap goes out of scope, the value will be cleaned up by `drop` unless ownership of the data has been moved to another variable.

While this works, taking ownership and then returning ownership with every function is a bit tedious. What if we want to let a function use a value but not take ownership? It's quite annoying that anything we pass in also needs to be passed back if we want to use it again, in addition to any data resulting from the body of the function that we might want to return as well.

It's possible to return multiple values using tuples, like this:

```move
module my_module::tuple_return {
    public fun tuple_return_demo() {
        let s1 = string::utf8(b"hello");

        let (s2, len) = calculate_length(s1);
    }

    fun calculate_length(s: String) -> (String, u64) {
        let length = string::length(&s); // len() returns the length of a String

        (s, length) // return both the String and the length
    }
}
```

But this is too much ceremony and a lot of work for a concept that should be common. Luckily for us, Move has a feature for using a value without transferring ownership, called references.
