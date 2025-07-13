# Guessing Game Contract

TODO: Walk through the contract part by part

Here is the full contract at the end:

```move
/// Guessing game
///
/// - Call `create_game` to start the game
/// - Guess with `guess`
/// - When the number is guessed correctly, the game is over
/// - Can be reset with `reset_game`
/// - Can be cleaned up with `remove_state`
///
module module_addr::guessing_game {
    use std::signer;

    /// No game initialized for this account, please call create_game first
    const E_NO_GAME: u64 = 1;

    /// Game is over, please call reset_game
    const E_GAME_OVER: u64 = 2;

    /// Game is not over,  please guess until the game is over
    const E_GAME_NOT_OVER: u64 = 3;

    /// Game is already initialized, please guess until the game is over
    const E_GAME_INITIALIZED: u64 = 4;

    /// Number is already guessed, please guess a different number
    const E_ALREADY_GUESSED: u64 = 5;

    /// State of the game
    struct Game has key {
        number: u8,
        guesses: vector<u8>,
        game_over: bool,
    }

    /// Creates a game
    entry fun create_game(caller: &signer, number: u8) {
        let caller_addr = signer::address_of(caller);
        assert!(!exists<Game>(caller_addr), E_GAME_INITIALIZED);
        move_to(caller, Game {
            number,
            guesses: vector[],
            game_over: false,
        })
    }

    /// Guesses on the game
    public entry fun guess(caller: &signer, number: u8) acquires Game {
        let caller_addr = signer::address_of(caller);

        // Check that the game exists
        assert!(exists<Game>(caller_addr), E_NO_GAME);

        let game = &mut Game[caller_addr];

        // Check that the game isn't over
        assert!(!game.game_over, E_GAME_OVER);

        // Check that I haven't guessed already
        assert!(!game.guesses.contains(&number), E_ALREADY_GUESSED);

        game.guesses.push_back(number);
        
        // Check win condition
        if (number == game.number) {
            game.game_over = true;
        }
    }

    /// Resets the game when it's done
    entry fun reset_game(caller: &signer, new_num: u8) acquires Game {
        let caller_addr = signer::address_of(caller);

        // Check that the game exists
        assert!(exists<Game>(caller_addr), E_NO_GAME);

        let game = &mut Game[caller_addr];

        // Check that the game is over
        assert!(game.game_over, E_GAME_NOT_OVER);

        game.game_over = false;
        game.guesses = vector[];
        game.number = new_num;
    }

    /// Deletes the game state
    entry fun remove_state(caller: &signer) acquires Game {
        let caller_addr = signer::address_of(caller);
        assert!(exists<Game>(caller_addr), E_NO_GAME);
        let Game {
            ..
        } = move_from<Game>(caller_addr);
    }

    #[view]
    public fun is_game_over(addr: address): bool acquires Game {
        assert!(exists<Game>(addr), E_NO_GAME);

        Game[addr].game_over
    }

    #[view]
    public fun number(addr: address): u8 acquires Game {
        assert!(exists<Game>(addr), E_NO_GAME);
        assert!(is_game_over(addr), E_GAME_NOT_OVER);

        Game[addr].number
    }

    #[view]
    public fun guesses(addr: address): vector<u8> acquires Game {
        assert!(exists<Game>(addr), E_NO_GAME);

        Game[addr].guesses
    }
}
```