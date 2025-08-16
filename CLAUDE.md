# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is "The Aptos Book" - a comprehensive reference guide for the Aptos blockchain and Move programming language. It's built using mdBook, a static site generator for creating documentation from Markdown files.

## Development Commands

### Using Mise (Recommended)

```bash
mise run build    # Build the book
mise run serve    # Serve the book locally at http://localhost:3000
mise run watch    # Watch for changes and rebuild automatically
mise run clean    # Clean build artifacts
```

### Direct mdBook Commands

```bash
mdbook build      # Build the book
mdbook serve      # Serve the book locally
mdbook watch      # Watch for changes and rebuild
mdbook clean      # Clean build artifacts
```

## Setup Commands

For new development environments:

```bash
# Option 1: Using Mise (recommended)
./scripts/setup-mise.sh

# Option 2: Traditional setup (requires Rust installed first)
./scripts/setup.sh
```

## Architecture

### Source Structure

- `src/` - Main content directory containing all Markdown files
- `book.toml` - mdBook configuration file
- `mise.toml` - Mise tool configuration with tasks and dependencies
- `book/` - Generated output directory (HTML, assets, etc.)

### Content Organization

The book follows a structured learning path:

- Getting Started: Installation and basic concepts
- Common Programming Concepts: Variables, functions, control flow
- Language Features: Structs, enums, generics, ownership
- Advanced Topics: Error handling, testing, gas optimization
- Standard Libraries: Aptos Framework, fungible/non-fungible tokens
- Tools: CLI usage, SDK integration

### Build Process

Uses mdBook with several plugins:

- `mdbook-mermaid` for diagrams
- `mdbook-katex` for mathematical expressions
- `mdbook-linkcheck` for validating links
- `mdbook-llms-txt-tools` for LLM-friendly output formats

### Output Formats

- HTML for web deployment (deployed to aptos-book.com)
- llms-txt format for LLM consumption
- Link checking for quality assurance

## Key Files

- `book.toml:26` - Main configuration with preprocessors and output settings
- `mise.toml:19-22` - Task definitions for common operations
- `src/SUMMARY.md` - Table of contents defining book structure