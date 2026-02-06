# Using LLMs to Write Move Code

LLMs can significantly accelerate Move development when used effectively. This section covers best practices for prompting LLMs to generate correct, secure, and idiomatic Move code.

## Providing Context

The most important factor for high-quality Move code generation is giving the LLM sufficient context about the Aptos ecosystem and Move language.

### Using llms.txt

The Aptos Book and Aptos developer documentation are published in the [llms.txt](https://llmstxt.org/) format. You can provide this content directly to an LLM:

```
# In your prompt or system message, include:
# - The relevant chapter of the Aptos Book (e.g., the structs or events chapter)
# - The Aptos Framework documentation for modules you plan to use
# - Your existing code for context
```

### Structuring Your Prompts

A well-structured prompt for Move code generation includes:

1. **Goal**: What the contract should do
2. **Context**: Relevant Aptos/Move concepts
3. **Constraints**: Security requirements, gas considerations
4. **Examples**: Similar code patterns from the Aptos ecosystem

#### Example Prompt

```
Write a Move module for a simple escrow contract on Aptos.

Requirements:
- Seller deposits an item (represented as a u64 token ID)
- Buyer deposits APT as payment
- Either party can cancel before both sides deposit
- When both sides deposit, the swap executes automatically
- Use the Aptos object model for the escrow
- Emit events for all state changes
- Include comprehensive error codes
- Follow the naming conventions from the Aptos Book

Use these Aptos framework modules:
- aptos_framework::object for the escrow object
- aptos_framework::event for events
- aptos_framework::fungible_asset for APT transfers
```

## Effective Prompt Patterns

### Pattern 1: Incremental Development

Build contracts step by step:

```
Step 1: "Define the struct and error codes for a voting contract"
Step 2: "Add the create_proposal entry function"
Step 3: "Add the vote entry function with duplicate vote prevention"
Step 4: "Add view functions for proposal status"
Step 5: "Add unit tests for the happy path"
Step 6: "Add unit tests for error cases"
```

### Pattern 2: Code Review

Ask the LLM to review generated code:

```
Review this Move module for:
1. Security vulnerabilities
2. Missing error handling
3. Gas optimization opportunities
4. Incorrect use of abilities
5. Missing events

[paste your code]
```

### Pattern 3: Test Generation

LLMs excel at generating comprehensive tests:

```
Write unit tests for this Move module. Include:
- Happy path tests for each entry function
- Error case tests with #[expected_failure]
- Edge case tests (zero values, max values, empty collections)
- Multi-user interaction tests

[paste your module]
```

### Pattern 4: Explain and Refactor

Use LLMs to understand existing code:

```
Explain what this Move module does, including:
- The purpose of each struct and its abilities
- What each function does and when it should be called
- The security model (who can call what)
- Any potential issues

[paste existing code]
```

## Common Pitfalls

### 1. Outdated Syntax

LLMs may generate Move code using outdated syntax. Key things to watch for:

- **Resource indexing**: Modern Move uses `Resource[addr]` instead of `borrow_global<Resource>(addr)`
- **Vector methods**: Modern Move supports `v.push_back(x)` instead of `vector::push_back(&mut v, x)`
- **Event emission**: Use `#[event]` with `event::emit()` instead of legacy event handles

### 2. Missing Abilities

LLMs sometimes forget or misapply abilities. Always check:

- Does the struct need `key` for global storage?
- Does the struct need `store` to be embedded in other stored types?
- Should the struct lack `copy` to prevent duplication (for assets)?
- Should the struct lack `drop` to prevent accidental loss (for receipts)?

### 3. Incorrect Error Handling

LLMs may use generic error codes or forget error conditions. Ensure:

- Every abort has a descriptive error constant
- Error constants follow the `E_` naming convention
- Doc comments describe the error condition
- All preconditions are checked

### 4. Security Assumptions

LLMs may make incorrect security assumptions. Always verify:

- Signer authorization is required for state changes
- View functions don't modify state
- Entry function parameters are validated
- Access control is enforced

## Workflow: LLM-Assisted Development

A recommended workflow for using LLMs in Move development:

1. **Spec**: Describe what you want to build in natural language
2. **Generate**: Use an LLM to generate the initial code
3. **Review**: Manually review the generated code for correctness
4. **Compile**: Run `aptos move compile` to check for compilation errors
5. **Test**: Generate and run tests with `aptos move test`
6. **Audit**: Use the LLM to review the code for security issues
7. **Iterate**: Refine based on test results and review feedback

## LLM Tool Integration

Several development tools integrate LLMs with Move development:

- **Cursor / VS Code with AI**: Use the Aptos Move Analyzer extension alongside an AI assistant
- **GitHub Copilot**: Provides inline Move code suggestions (ensure you have Aptos context loaded)
- **Claude / GPT with documentation**: Feed llms.txt content for context-aware code generation

## Best Practices Summary

1. **Always provide Aptos-specific context**: Don't assume the LLM knows the latest Move syntax.
2. **Review all generated code**: LLMs are assistants, not replacements for developer judgment.
3. **Compile and test**: Always verify generated code compiles and passes tests.
4. **Use incremental prompts**: Build complex contracts step by step.
5. **Cross-reference with documentation**: Verify LLM suggestions against official Aptos docs.
6. **Keep the LLM updated**: Provide the latest llms.txt content for current API information.
