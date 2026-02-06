# The llms.txt Standard and Aptos

The [llms.txt](https://llmstxt.org/) standard provides a way for websites and documentation to be directly consumable by Large Language Models. The Aptos ecosystem embraces this standard to make blockchain development more accessible to AI-assisted workflows.

## What is llms.txt?

The llms.txt standard defines a simple, structured text format that:

- Is easy for LLMs to parse and understand
- Contains all essential information without HTML, JavaScript, or CSS noise
- Follows a consistent hierarchy that maps well to LLM context windows
- Can be directly included in prompts or system messages

## How the Aptos Book Uses llms.txt

This book is built with `mdbook-llms-txt-tools`, which automatically generates llms.txt output alongside the HTML version. The build process creates two LLM-optimized outputs:

### `llms.txt` - Summary Format

A concise overview of the book's structure and key concepts. Useful for giving an LLM a high-level understanding of the Aptos ecosystem.

### `llms-full.txt` - Complete Content

The entire book's content in a flat, LLM-friendly format. Useful for giving an LLM deep knowledge about specific topics.

## Using llms.txt in Your Workflow

### Providing Context to LLMs

When working with an LLM on Aptos development, include relevant sections of the llms.txt output:

```
System prompt:
You are an expert Aptos/Move developer. Use the following reference material:

[paste relevant sections from llms-full.txt]

User prompt:
Write a Move module for a token vesting contract...
```

### Building Custom AI Tools

You can fetch the llms.txt file programmatically to build AI-powered tools:

```typescript
// Fetch the Aptos Book content for LLM context
// This book is hosted at aptos-book.com; the llms-full.txt endpoint
// serves the entire book in a single LLM-friendly text file.
const response = await fetch("https://aptos-book.com/llms-full.txt");
const aptosBookContent = await response.text();

// Include in your LLM prompt
const prompt = `
Reference: ${aptosBookContent}

Task: Generate a Move module for...
`;
```

### IDE Integration

Configure your AI-powered IDE to include Aptos documentation:

1. Add the llms.txt URL to your editor's AI context sources
2. Reference specific chapters when asking for code assistance
3. Use the structured format to provide targeted context

## Making Your Own Documentation LLM-Friendly

If you're building on Aptos and want your documentation to be LLM-consumable:

### 1. Use mdBook with llms-txt-tools

```toml
# book.toml
[output.llms-txt]
[output.llms-txt-full]
```

### 2. Structure Content Hierarchically

```markdown
# Main Topic

## Subtopic

### Concept

Explanation with code examples.

```move
// Code example
```
```

### 3. Write for Both Humans and LLMs

Good documentation for LLMs:

- **Uses clear headings** that describe the content below
- **Includes complete code examples** that can be used as-is
- **Explains concepts before using them** (define before reference)
- **Uses consistent terminology** throughout
- **Provides context** for code examples (what problem they solve)
- **Lists prerequisites** when building on earlier concepts

### 4. Include Structured Data

Tables, lists, and structured examples help LLMs extract information:

```markdown
| Feature | Description | Example |
|---|---|---|
| `key` | Stored in global storage | `struct Token has key { ... }` |
| `store` | Can be nested | `struct Metadata has store { ... }` |
```

## The Broader Aptos AI Ecosystem

The Aptos ecosystem is actively building infrastructure for AI-blockchain integration:

- **llms.txt support**: Documentation optimized for LLM consumption
- **AI agent frameworks**: Tools for building autonomous on-chain agents
- **Smart contract templates**: LLM-friendly templates for common patterns
- **API documentation**: REST and GraphQL APIs documented in LLM-friendly formats

## Benefits for Developers

By using llms.txt-optimized documentation:

1. **Faster onboarding**: LLMs can provide accurate Aptos-specific guidance
2. **Better code generation**: LLMs produce more correct Move code with proper context
3. **Reduced errors**: AI assistants catch common mistakes when given comprehensive documentation
4. **Always up-to-date**: llms.txt files are generated from the latest documentation
5. **Language-agnostic**: LLMs can explain concepts in any natural language, making Aptos accessible globally
