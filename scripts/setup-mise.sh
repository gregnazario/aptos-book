#!/bin/sh

# Mise setup script for aptos-book
# This script sets up the development environment using Mise

echo "Setting up aptos-book development environment with Mise..."

# Check if mise is installed
if ! command -v mise >/dev/null 2>&1; then
    echo "Error: Mise is not installed. Please install Mise first."
    echo "Visit https://mise.jdx.dev/getting-started.html for installation instructions."
    exit 1
fi

# Install all tools defined in mise.toml
echo "Installing tools with Mise..."
mise install

# Install mdBook and plugins with specific versions
echo "Installing mdBook and plugins..."
cargo install mdbook --version 0.4.52
cargo install mdbook-mermaid --version 0.15.0
cargo install mdbook-katex --version 0.9.4
cargo install mdbook-linkcheck --version 0.7.7
cargo install mdbook-llms-txt-tools --version 0.1.1

echo "Setup complete! You can now use the following commands:"
echo "  mise run build    - Build the book"
echo "  mise run serve    - Serve the book locally"
echo "  mise run watch    - Watch for changes and rebuild"
echo "  mise run clean    - Clean build artifacts" 
