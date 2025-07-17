# Guessing Game Contract

## Creating a module

First, we need to create a *module*.  A *module*, in Move is a collection of related code (structs, functions, constants) that is published at a specific address. Modules provide encapsulation and organization for your smart contract logic.

```move
module module_addr::guessing_game {

}
```

---

## Contract Explanation and Breakdown

### Creating a Module

A *module* in Move is a collection of related code (structs, functions, constants) that is published at a specific address. Modules provide encapsulation and organization for your smart contract logic.

```move
module module_addr::guessing_game {
    // Module contents go here
}
```
Here, `module_addr` is a named address (set at compile/deploy time), and `guessing_game` is the module's name.

---

### Error Codes

The contract defines error constants to provide clear, descriptive error messages for different failure conditions:

```move
const E_NO_GAME: u64 = 1;         // No game initialized for this account
const E_GAME_OVER: u64 = 2;       // Game is over, must reset
const E_GAME_NOT_OVER: u64 = 3;   // Game is not over, must finish guessing
const E_GAME_INITIALIZED: u64 = 4;// Game already initialized
const E_ALREADY_GUESSED: u64 = 5; // Number already guessed
```

---

### Game State

The `Game` struct stores all state for a single game:

```move
struct Game has key {
    number: u8,             // The number to guess
    guesses: vector<u8>,    // All previous guesses
    game_over: bool,        // Whether the game is over
}
```
- The `key` ability allows this struct to be stored in global storage under an account address.

---

### Game Functions

#### Creating a Game

```move
entry fun create_game(caller: &signer, number: u8) {
    let caller_addr = signer::address_of(caller);
    assert!(!exists<Game>(caller_addr), E_GAME_INITIALIZED);
    move_to(caller, Game {
        number,
        guesses: vector[],
        game_over: false,
    })
}
```
- Only one game per account is allowed at a time.
- Stores the new game in the caller's account.

#### Making a Guess

```move
public entry fun guess(caller: &signer, number: u8) acquires Game {
    let caller_addr = signer::address_of(caller);
    assert!(exists<Game>(caller_addr), E_NO_GAME);
    let game = &mut Game[caller_addr];
    assert!(!game.game_over, E_GAME_OVER);
    assert!(!game.guesses.contains(&number), E_ALREADY_GUESSED);
    game.guesses.push_back(number);
    if (number == game.number) {
        game.game_over = true;
    }
}
```
- Checks that the game exists and is not over.
- Prevents duplicate guesses.
- Marks the game as over if the guess is correct.

#### Resetting the Game

```move
entry fun reset_game(caller: &signer, new_num: u8) acquires Game {
    let caller_addr = signer::address_of(caller);
    assert!(exists<Game>(caller_addr), E_NO_GAME);
    let game = &mut Game[caller_addr];
    assert!(game.game_over, E_GAME_NOT_OVER);
    game.game_over = false;
    game.guesses = vector[];
    game.number = new_num;
}
```
- Only allowed if the game is over.
- Resets guesses and sets a new number.

#### Removing the Game State

```move
entry fun remove_state(caller: &signer) acquires Game {
    let caller_addr = signer::address_of(caller);
    assert!(exists<Game>(caller_addr), E_NO_GAME);
    let Game { .. } = move_from<Game>(caller_addr);
}
```
- Deletes the game from storage for the caller.

---

### View Functions

These functions allow anyone to query the game state without modifying it:

```move
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
```
- `is_game_over`: Returns whether the game is over.
- `number`: Returns the answer, but only if the game is over (prevents cheating).
- `guesses`: Returns all guesses made so far.

---

### Key Concepts Demonstrated

- **State Management**: Uses a struct with the `key` ability for on-chain state.
- **Access Control**: Only the account owner can modify their game.
- **Error Handling**: Uses clear error codes and assertions.
- **Resource Safety**: Ensures proper creation, update, and deletion of game state.
- **View Functions**: Provides read-only access to game state.
- **Game Logic**: Implements a simple, fair guessing game with validation.

This contract is a practical example of how to build a stateful, interactive Move smart contract on Aptos, and demonstrates best practices for error handling, state management, and user interaction.

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
