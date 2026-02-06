# Package Dependencies

Move packages can depend on other packages, including the Aptos framework, standard libraries, and third-party packages.

## Adding Dependencies

Dependencies are declared in the `[dependencies]` section of `Move.toml`.

### Git Dependencies

The most common type of dependency for Aptos projects:

```toml
[dependencies]
AptosFramework = {
    git = "https://github.com/aptos-labs/aptos-framework.git",
    subdir = "aptos-move/framework/aptos-framework",
    rev = "main"
}
```

- **`git`** -- The repository URL.
- **`subdir`** -- The subdirectory within the repo that contains the Move package.
- **`rev`** -- The git revision (branch, tag, or commit hash). Using a specific commit hash is recommended for reproducible builds.

### Local Dependencies

For packages on your local filesystem:

```toml
[dependencies]
MyLibrary = { local = "../my-library" }
```

### Pinning a Specific Version

For reproducible builds, pin to a specific commit hash:

```toml
[dependencies]
AptosFramework = {
    git = "https://github.com/aptos-labs/aptos-framework.git",
    subdir = "aptos-move/framework/aptos-framework",
    rev = "abc123def456"
}
```

## The Aptos Framework Dependencies

Most Aptos projects need the Aptos Framework, which provides standard modules for accounts, coins, objects, and more. The framework includes three layers:

```toml
[dependencies]
# Includes MoveStdlib, AptosStdlib, and AptosFramework
AptosFramework = {
    git = "https://github.com/aptos-labs/aptos-framework.git",
    subdir = "aptos-move/framework/aptos-framework",
    rev = "main"
}
```

Importing `AptosFramework` automatically includes `MoveStdlib` and `AptosStdlib` as transitive dependencies.

## Address Mapping for Dependencies

If a dependency uses named addresses, you may need to provide them. The Aptos Framework standard addresses are typically set automatically.

```toml
[addresses]
my_addr = "_"
std = "0x1"
aptos_std = "0x1"
aptos_framework = "0x1"
```

## Dependency Resolution

When you run `aptos move compile`, the CLI:

1. Downloads all git dependencies to a local cache.
2. Resolves transitive dependencies.
3. Checks for version conflicts.
4. Compiles all dependencies before your package.

## Best Practices

1. **Pin dependency versions**: Use specific commit hashes rather than `main` for production code.
2. **Minimize dependencies**: Only include what you need.
3. **Use the framework**: The Aptos Framework provides battle-tested implementations of common patterns.
4. **Test with the same dependencies**: Ensure your tests use the same dependency versions as your production code.
