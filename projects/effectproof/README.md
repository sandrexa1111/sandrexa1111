# state-delta

A small deterministic tool for checking **observable state changes** against an explicit contract.

The repository path is still `effectproof` for compatibility, but the project name is **state-delta**.

## What it does

Given a state before an operation, a state after it, and an effect contract, `state-delta` reports:

- changed fields
- unexpected mutations
- forbidden mutations
- required postcondition failures
- a stable proof ID for the exact inputs

It does not use a model in the verification path.

## Example

The included calendar fixture models an operation that successfully renames an event but also changes a guest-permission field that was not allowed to change. `state-delta` catches the extra mutation.

## Install

```bash
cd projects/effectproof
python -m pip install -e ".[dev]"
```

## Run

```bash
state-delta examples/calendar/before.json examples/calendar/after.json examples/calendar/contract.json
```

## Development

```bash
pytest -q
ruff check src tests
mypy src/effectproof
```

## Scope

`state-delta` verifies declared observable state transitions. It does not prove arbitrary semantic correctness, infer missing specifications, or inspect hidden provider state.
