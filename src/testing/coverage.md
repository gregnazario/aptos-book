# Coverage

Test coverage measures how much of your code is exercised by tests. The Aptos CLI supports generating coverage reports for your Move packages.

## Generating Coverage

Run tests with coverage enabled:

```sh
aptos move test --dev --coverage
```

This runs your tests and generates a coverage report.

## Viewing Coverage

After running tests with coverage, view the summary:

```sh
aptos move coverage summary --dev
```

This shows the percentage of code covered by tests for each module.

For a detailed source-level report:

```sh
aptos move coverage source --module counter --dev
```

This shows which lines of code were covered (marked) and which were not.

## Interpreting Coverage

- **High coverage** (>80%) indicates that most code paths are tested.
- **Low coverage** means there are untested code paths that could contain bugs.
- **100% coverage** does not guarantee correctness -- it only means every line was executed.

Focus on testing:
1. All public entry points
2. All error conditions
3. Edge cases and boundary values
4. State transitions

## Best Practices

1. **Aim for high coverage**: Target at least 80% coverage for production code.
2. **Cover error paths**: Ensure all `assert!` and `abort` conditions are tested.
3. **Don't chase 100%**: Some code is trivial and doesn't need dedicated tests.
4. **Use coverage to find gaps**: Review uncovered lines to identify missing tests.
5. **Run coverage in CI**: Make coverage checks part of your continuous integration pipeline.
