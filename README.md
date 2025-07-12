# aptos-book
The Aptos Book - A one stop reference for Aptos

## Setup

### Option 1: Using Mise (Recommended)

This project now supports [Mise](https://mise.jdx.dev/) for managing development tools and dependencies.

1. Install Mise: https://mise.jdx.dev/getting-started.html
2. Run the setup script:
   ```bash
   ./scripts/setup-mise.sh
   ```
3. Use Mise commands:
   ```bash
   mise run build    # Build the book
   mise run serve    # Serve the book locally
   mise run watch    # Watch for changes and rebuild
   mise run clean    # Clean build artifacts
   ```

### Option 2: Traditional Setup

1. Install Rust: https://rustup.rs/
2. Run the setup script:
   ```bash
   ./scripts/setup.sh
   ```
3. Use mdBook commands directly:
   ```bash
   mdbook build
   mdbook serve
   mdbook watch
   mdbook clean
   ```
