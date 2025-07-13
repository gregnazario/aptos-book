# Extending the Contract

## Adding Randomness

Providing the number to guess is kind of silly, let's add a function to generate a random number and insert it into the
contract. The backwards compatibility rules say that we cannot remove existing functions, so we will just abort on the
existing functions. This should keep it clean to remove warnings, and allow for upgrading.

```move
module module_addr::guessing_game {

    // ... contract ...

    /// Manual inputs are no longer supported
    const E_NO_LONGER_SUPPORTED: u64 = 6;

    entry fun create_game(_caller: &signer, _num: u8) {
        abort E_NO_LONGER_SUPPORTED
    }

    entry fun reset_game(_caller: &signer, _num: u8) {
        abort E_NO_LONGER_SUPPORTED
    }
}
```

We will then add new functions `create_game_random` and `reset_game_random` which mirror the original functions but only
use random inputs.

```move
module module_addr::guessing_game {
    use aptos_framework::randomness;

    #[randomness]
    entry fun create_game_random(caller: &signer) {
        let caller_addr = signer::address_of(caller);
        assert!(!exists<Game>(caller_addr), E_GAME_INITIALIZED);
        let number = randomness::u8_integer();
        move_to(caller, Game {
            number,
            guesses: vector[],
            game_over: false,
        })
    }

    #[randomness]
    entry fun reset_game_random(caller: &signer) acquires Game {
        let caller_addr = signer::address_of(caller);

        // Check that the game exists
        assert!(exists<Game>(caller_addr), E_NO_GAME);

        let game = &mut Game[caller_addr];

        // Check that the game is over
        assert!(game.game_over, E_GAME_NOT_OVER);

        game.game_over = false;
        game.guesses = vector[];
        game.number = randomness::u8_integer();
    }
}
```

But, of course the tests now fail!  We will need to update the existing tests given our expectations. This can be done
by either adding a `#[test_only]` function, or by setting the seed for the randomness in tests.

TODO: Code example updating the tests

Once this is done, we can simply upgrade the contract by deploying again.

```sh
aptos move deploy --named-addresses module_addr=default
```