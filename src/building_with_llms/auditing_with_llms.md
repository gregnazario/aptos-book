# Using LLMs to Audit Smart Contracts

LLMs can serve as a valuable first line of defense in smart contract security review. While they don't replace professional auditors, they can catch common vulnerabilities and improve code quality before a formal audit.

## The AI Audit Workflow

### Step 1: Initial Scan

Feed your entire contract to the LLM with a structured audit prompt:

```
Perform a security audit of this Move smart contract. Check for:

1. Access control issues (missing signer checks, unauthorized state changes)
2. Resource safety (potential for resource duplication or loss)
3. Integer overflow/underflow
4. Reentrancy or cross-module interaction issues
5. Missing input validation
6. Incorrect use of abilities
7. Missing or incorrect error codes
8. Event emission completeness
9. Gas optimization opportunities
10. Upgrade safety (backward compatibility)

For each issue found, provide:
- Severity (Critical / High / Medium / Low / Informational)
- Location (function name and line)
- Description of the issue
- Recommended fix

[paste your contract]
```

### Step 2: Focused Analysis

Drill into specific areas:

```
Analyze the access control model of this contract:
- Who can call each entry function?
- What state can each caller modify?
- Are there any privilege escalation paths?
- Is the admin role properly protected?

[paste your contract]
```

### Step 3: Test Gap Analysis

Identify missing test coverage:

```
Given this contract and its test suite, identify:
- Which functions lack test coverage?
- Which error paths are not tested?
- Which edge cases are missing?
- What interaction patterns between functions should be tested?

Contract:
[paste contract]

Tests:
[paste tests]
```

## Common Vulnerabilities LLMs Can Detect

### Missing Signer Authorization

```move
// VULNERABLE: No signer check -- anyone can call this
public entry fun set_admin(new_admin: address) acquires Config {
    let config = &mut Config[@my_addr];
    config.admin = new_admin;
}

// FIXED: Requires signer authorization
public entry fun set_admin(current_admin: &signer, new_admin: address) acquires Config {
    let config = &mut Config[@my_addr];
    assert!(signer::address_of(current_admin) == config.admin, E_NOT_ADMIN);
    config.admin = new_admin;
}
```

### Unchecked Arithmetic

```move
// VULNERABLE: Could overflow
public fun add_balance(account: &mut Account, amount: u64) {
    account.balance = account.balance + amount;
}

// FIXED: Check for overflow
public fun add_balance(account: &mut Account, amount: u64) {
    let new_balance = account.balance + amount;
    assert!(new_balance >= account.balance, E_OVERFLOW);
    account.balance = new_balance;
}
```

### Missing Existence Checks

```move
// VULNERABLE: Will abort with an unhelpful error if resource doesn't exist
public fun get_balance(addr: address): u64 acquires Balance {
    Balance[addr].amount
}

// FIXED: Explicit existence check with descriptive error
public fun get_balance(addr: address): u64 acquires Balance {
    assert!(exists<Balance>(addr), E_NO_BALANCE);
    Balance[addr].amount
}
```

## Limitations of LLM Auditing

LLMs have important limitations as auditors:

1. **No execution**: LLMs reason about code statically -- they cannot run it.
2. **Context window**: Very large contracts may exceed the LLM's context window.
3. **Novel vulnerabilities**: LLMs may miss novel attack vectors not present in training data.
4. **False positives**: LLMs may flag correct code as vulnerable.
5. **No formal proofs**: LLMs provide heuristic analysis, not mathematical proofs.

## Combining AI and Human Auditing

The most effective approach combines AI and human review:

| Stage | Tool | Purpose |
|---|---|---|
| Development | LLM-assisted coding | Generate initial code with best practices |
| Self-review | LLM audit | Catch obvious issues before submission |
| Compiler | `aptos move compile` | Type checking and ability verification |
| Testing | `aptos move test` | Runtime correctness verification |
| Formal verification | `aptos move prove` | Mathematical guarantees for critical properties |
| Professional audit | Human auditors | Deep analysis of business logic and novel attacks |

## Best Practices

1. **Use LLMs as a first pass**: Run AI audits before spending on professional auditors.
2. **Don't rely solely on AI**: Always have human review for production contracts.
3. **Provide full context**: Give the LLM all related modules, not just the one being audited.
4. **Iterate on findings**: Fix issues the LLM identifies, then re-audit.
5. **Document assumptions**: Ask the LLM to list all assumptions it made during the audit.
6. **Check against known patterns**: Ask the LLM to verify your contract follows established design patterns.
