# Package Basics

A Move package is a directory containing a `Move.toml` manifest and one or more Move source files. It is the unit of compilation and deployment on Aptos.

## Package Structure

A typical package looks like this:

```
my_project/
├── Move.toml          # Package manifest
├── sources/           # Move source files
│   ├── token.move
│   └── marketplace.move
└── tests/             # Test files (optional)
    └── token_tests.move
```

## The `Move.toml` File

The `Move.toml` manifest describes your package:

```toml
[package]
name = "MyProject"
version = "1.0.0"
authors = ["developer@example.com"]

[addresses]
my_addr = "_"

[dependencies]
AptosFramework = { git = "https://github.com/aptos-labs/aptos-framework.git", subdir = "aptos-move/framework/aptos-framework", rev = "main" }
```

### Sections

- **`[package]`** -- Metadata about your package (name, version, authors).
- **`[addresses]`** -- Named address definitions. Use `"_"` for addresses that will be provided at deploy time.
- **`[dependencies]`** -- External packages your code depends on.

## Creating a New Package

The Aptos CLI can create a package from a template:

```sh
mkdir my_project
cd my_project
aptos move init --name MyProject
```

This creates the basic directory structure and a `Move.toml` file.

You can also use templates:

```sh
aptos move init --name MyProject --template hello-blockchain
```

## Building a Package

To compile your package:

```sh
aptos move compile --named-addresses my_addr=default
```

The `--named-addresses` flag maps named addresses to actual values. The special value `default` uses your CLI profile's address.

## Source Files

Move source files have the `.move` extension and can contain one or more modules:

```move
// sources/token.move
module my_addr::token {
    struct Token has key {
        balance: u64,
    }
}
```

Multiple modules can exist in a single file, but the convention is one module per file, with the filename matching the module name.

## Test Files

Test files live in the `tests/` directory or alongside source files. Test functions are annotated with `#[test]`:

```move
// tests/token_tests.move
#[test_only]
module my_addr::token_tests {
    use my_addr::token;

    #[test]
    fun test_creation() {
        // ...
    }
}
```

## Best Practices

1. **One module per file**: Keep source files focused and name them after the module they contain.
2. **Use named addresses**: Use named addresses with `"_"` rather than hardcoding addresses.
3. **Version your packages**: Use semantic versioning in `Move.toml`.
4. **Keep `Move.toml` clean**: Only include dependencies you actually use.
