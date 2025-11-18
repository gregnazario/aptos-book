# Interacting with the Contract

Now that the guessing game contract is deployed, we can interact with it using the Aptos CLI.
We'll assume you're using the `default` profile created earlier with `aptos init`.

The guessing game module was published under your account's address, so all function calls can be made using:

```
--function-id default::guessing_game::<function_name>
```

The `default` profile automatically provides the signer argument, so we only need to supply the non-signer parameters.

## Creating a Game

To start a new game, call the `create_game` entry function and provide a number (0–255) that players must guess:

```sh
aptos move run \
  --profile default \
  --function-id default::guessing_game::create_game \
  --args 'u8:5'
```

This initializes a new game for the signer with the answer set to `5`.

## Making a Guess

Once a game is created, you can make guesses by calling the `guess` function:

```sh
aptos move run \
  --profile default \
  --function-id default::guessing_game::guess \
  --args 'u8:3'
```

You can continue guessing with different values:

```sh
aptos move run \
  --profile default \
  --function-id default::guessing_game::guess \
  --args 'u8:5'
```

If the guess matches the stored answer, the game is marked as over.

## Viewing Game State

The contract provides several view functions, which allow anyone to inspect the game state without modifying it.

### Is the game over?

```sh
aptos move view \
  --profile default \
  --function-id default::guessing_game::is_game_over \
  --args address:default
```

### View the answer (only allowed when the game is over)

```sh
aptos move view \
  --profile default \
  --function-id default::guessing_game::number \
  --args address:default
```

### View all guesses made so far

```sh
aptos move view \
  --profile default \
  --function-id default::guessing_game::guesses \
  --args address:default
```

Here, `address:default` automatically resolves to the signer’s on-chain account address.

## Resetting or Removing the Game

Once a game has been completed, it can be reset with a new number:

```sh
aptos move run \
  --profile default \
  --function-id default::guessing_game::reset_game \
  --args 'u8:7'
```

To remove the game state entirely from your account:

```sh
aptos move run \
  --profile default \
  --function-id default::guessing_game::remove_state
```

This clears the `Game` resource from storage and allows a completely new game to be created.
