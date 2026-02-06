# Package Publishing

Publishing a package deploys your compiled Move modules to the Aptos blockchain. Once published, your code is live and callable by anyone.

## Publishing with the Aptos CLI

The most common way to publish is with the `aptos move publish` command (or `aptos move deploy`):

```sh
aptos move publish --named-addresses my_addr=default
```

This will:
1. Compile your package.
2. Show you a summary of the modules being deployed and estimated gas cost.
3. Prompt for confirmation.
4. Submit the publish transaction.

### Specifying a Profile

If you have multiple CLI profiles, specify which to use:

```sh
aptos move publish --profile mainnet --named-addresses my_addr=mainnet
```

### Skipping Confirmation

For scripts or CI/CD:

```sh
aptos move publish --named-addresses my_addr=default --assume-yes
```

## Upgrade Policies

When you publish code for the first time, you can choose an upgrade policy:

- **`compatible`** (default): You can upgrade the package, but changes must be backward-compatible (no removing public functions, no changing function signatures).
- **`immutable`**: The code can never be changed after publication.

For most projects, `compatible` is the right choice. It allows you to fix bugs and add new functionality while preserving existing interfaces.

## Upgrading a Package

To upgrade an already-published package, simply run the publish command again:

```sh
aptos move publish --named-addresses my_addr=default
```

The CLI will detect the existing package and perform an upgrade. The upgrade will fail if the changes are not backward-compatible (e.g., removing a public function).

### What Can Be Changed

- Adding new modules
- Adding new functions (public, entry, etc.)
- Adding new structs
- Changing private function implementations
- Adding new fields to structs (in some cases)

### What Cannot Be Changed

- Removing or renaming public functions
- Changing the signature of existing public functions
- Removing or renaming existing structs
- Removing or renaming existing modules

## Publishing Workflow

A typical workflow for deploying to mainnet:

1. **Develop and test locally**:
   ```sh
   aptos move test --dev
   ```

2. **Deploy to devnet**:
   ```sh
   aptos init --profile devnet --network devnet
   aptos move publish --profile devnet --named-addresses my_addr=devnet
   ```

3. **Test on devnet**:
   Interact with your contract and verify behavior.

4. **Deploy to testnet**:
   ```sh
   aptos init --profile testnet --network testnet
   aptos move publish --profile testnet --named-addresses my_addr=testnet
   ```

5. **Deploy to mainnet**:
   ```sh
   aptos init --profile mainnet --network mainnet
   aptos move publish --profile mainnet --named-addresses my_addr=mainnet
   ```

## Verifying Published Code

After publishing, you can verify your code on the [Aptos Explorer](https://explorer.aptoslabs.com). The source code is uploaded by default during publication, making it easy for others to verify what your contract does.

## Best Practices

1. **Always test before publishing**: Run `aptos move test` before every deployment.
2. **Deploy to devnet first**: Catch issues before they reach mainnet.
3. **Use compatible upgrades**: Allow yourself to fix bugs after deployment.
4. **Document your API**: Once published, your public functions are your contract's interface.
5. **Keep private functions private**: Only expose what external callers need.
