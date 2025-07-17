# Testing the Contract

Move provides a unit testing framework that's really easy to test different functionality. The tests can simply be
written in Move alongside the code in the same module.

All unit tests can be run from the Aptos CLI by using the command `aptos move test`. For this example, we will
specifically use the `--dev` flag to fill in the address, with the full command being `aptos move test --dev`

## Testing successful functionality

To define a test, you simply need to add `#[test]` above a function. The function will only be used for testing, so it
is best to keep them as private functions (no `public` or `entry`).

```move
module module_addr::guessing_game {

    // ... contract definition ...

    #[test]
    fun test_flow(caller: &signer) acquires Game {}
}
```

Within the `#[test]` annotation, you can add any number of `signer`s to be created for the test. In this example, we'll
only create one `signer` named `caller`. This `signer` will be used to call the functions in the contract and store
state at the associated address `0x1337`.

> Note that you can use either named addresses e.g. `@module_addr` or an address literal `@0x1337`.  `@` denotes that
> the literal is an address.

```move
module module_addr::guessing_game {

    // ... contract definition ...

    #[test(caller = @0x1337)]
    fun test_flow(caller: &signer) acquires Game {}
}
```

Within the test, you can call any move functions that exist, and use assertions similar to in the regular code.

> Note that you can skip the error codes for assertions in tests. Here, we'll test the basic flow of creating a game and
> guessing correctly on the first try. You can see how the game is considered over, and the one guess is recorded.

```move
module module_addr::guessing_game {

    // ... contract definition ...

    #[test(caller = @0x1337)]
    fun test_flow(caller: &signer) acquires Game {
        let caller_addr = signer::address_of(caller);
        create_game(caller, 1);
        assert!(!is_game_over(caller_addr));
        assert!(guesses(caller_addr) == vector[]);

        guess(caller, 1);
        assert!(is_game_over(caller_addr));
        assert!(guesses(caller_addr) == vector[1]);
    }
}
```

You can test this now by running the below command:

```sh
aptos move test --dev
```

And this testing can be added to in order to make it more extensive and include resetting the game:

```move
module module_addr::guessing_game {

    // ... contract definition ...

    #[test(caller = @0x1337)]
    fun test_flow(caller: &signer) acquires Game {
        let caller_addr = signer::address_of(caller);
        create_game(caller, 1);
        assert!(!is_game_over(caller_addr));
        assert!(guesses(caller_addr) == vector[]);

        guess(caller, 1);
        assert!(is_game_over(caller_addr));
        assert!(guesses(caller_addr) == vector[1]);

        reset_game(caller, 2);
        assert!(!is_game_over(caller_addr));
        assert!(guesses(caller_addr) == vector[]);

        guess(caller, 3);
        assert!(!is_game_over(caller_addr));
        assert!(guesses(caller_addr) == vector[3]);

        guess(caller, 4);
        assert!(!is_game_over(caller_addr));
        assert!(guesses(caller_addr) == vector[3, 4]);

        guess(caller, 2);
        assert!(is_game_over(caller_addr));
        assert!(guesses(caller_addr) == vector[3, 4, 2]);
    }
}
```

## Testing failures

Failures can similarly be tested, by checking for abort codes. These can be added by adding the
`#[exepcted_failure(abort_code = ...)]`.

> Note that the abort code can either be a constant e.g. `E_ALREADY_GUESSED` or the number directly `5`.

```move
module module_addr::guessing_game {

    // ... contract definition ...

    #[test(caller = @0x1337)]
    #[expected_failure(abort_code = E_ALREADY_GUESSED)]
    fun test_double_guess(caller: &signer) acquires Game {}
}
```

If you run this test and there is no abort in the test, it will fail. Meanwhile, we can add the actual functionality
into the test. When the below test is run, it will pass with a failure on the second `guess` call.

```move
module module_addr::guessing_game {

    // ... contract definition ...

    #[test(caller = @0x1337)]
    #[expected_failure(abort_code = E_ALREADY_GUESSED)]
    fun test_double_guess(caller: &signer) acquires Game {
        let caller_addr = signer::address_of(caller);
        create_game(caller, 1);
        assert!(!is_game_over(caller_addr));
        assert!(guesses(caller_addr) == vector[]);

        guess(caller, 2);
        guess(caller, 2);
    }
}
```

For more specific abort checking, you can add the location of the abort:

```move
module module_addr::guessing_game {
    #[test(caller = @0x1337)]
    #[expected_failure(abort_code = E_ALREADY_GUESSED, location = module_addr::guessing_game)]
    fun test_double_guess(caller: &signer) acquires Game {
        let caller_addr = signer::address_of(caller);
        create_game(caller, 1);
        assert!(!is_game_over(caller_addr));
        assert!(guesses(caller_addr) == vector[]);

        guess(caller, 2);
        guess(caller, 2);
    }
}
```

## Full Example

The full tests written are here:

```move
module module_addr::guessing_game {

    // ... contract definition ...

    #[test(caller = @0x1337)]
    /// Tests the full flow of the game
    fun test_flow(caller: &signer) acquires Game {
        let caller_addr = signer::address_of(caller);
        create_game(caller, 1);
        assert!(!is_game_over(caller_addr));
        assert!(guesses(caller_addr) == vector[]);

        guess(caller, 1);
        assert!(is_game_over(caller_addr));
        assert!(guesses(caller_addr) == vector[1]);

        reset_game(caller, 2);
        assert!(!is_game_over(caller_addr));
        assert!(guesses(caller_addr) == vector[]);

        guess(caller, 3);
        assert!(!is_game_over(caller_addr));
        assert!(guesses(caller_addr) == vector[3]);

        guess(caller, 4);
        assert!(!is_game_over(caller_addr));
        assert!(guesses(caller_addr) == vector[3, 4]);

        guess(caller, 2);
        assert!(is_game_over(caller_addr));
        assert!(guesses(caller_addr) == vector[3, 4, 2]);
    }

    #[test(caller = @0x1337)]
    #[expected_failure(abort_code = E_ALREADY_GUESSED, location = module_addr::guessing_game)]
    /// Tests guessing the same number
    fun test_double_guess(caller: &signer) acquires Game {
        let caller_addr = signer::address_of(caller);
        create_game(caller, 1);
        assert!(!is_game_over(caller_addr));
        assert!(guesses(caller_addr) == vector[]);

        guess(caller, 2);
        guess(caller, 2);
    }
}
```