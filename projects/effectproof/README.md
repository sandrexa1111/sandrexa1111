# EffectProof

Deterministic verification for **observable side effects**.

A tool call returning `200 OK` does not prove that only the intended state changed. EffectProof compares state before and after an operation, checks the delta against an explicit contract, and returns a reproducible verdict.

It is useful for agent tools, API workflows, automation, migration scripts, or any system where “success” is weaker than “the correct effects occurred.” No model is required.

> **Status:** experimental `v0.1.0`, zero runtime dependencies.

## Example

A calendar action is supposed to rename one event and write an audit field. It succeeds, but also changes a guest permission.

```bash
pip install -e .
effectproof examples/before.json examples/after.json examples/contract.json
```

Output:

```text
EFFECT VERDICT: FAILED
changes: 3
UNEXPECTED  /permissions/guest_can_invite: False -> True
FORBIDDEN   /permissions/guest_can_invite: False -> True
PASS equals     /event/title
PASS unchanged  /event/attendees
```

## Contract

```json
{
  "allowed": ["/event/title", "/audit/updated_by"],
  "forbidden": ["/permissions/*"],
  "required": [
    {"kind": "equals", "path": "/event/title", "value": "Planning - Q3"},
    {"kind": "unchanged", "path": "/event/attendees"}
  ]
}
```

Current rule kinds: `equals`, `exists`, `not_exists`, `unchanged`, and numeric `delta`.

## Design

1. Recursively diff two JSON-compatible state snapshots.
2. Express every changed leaf as a JSON Pointer-like path.
3. Match changes against allowed and forbidden path patterns.
4. Evaluate deterministic postconditions and preserved-state rules.
5. Hash the canonical inputs into a stable `proof_id`.

EffectProof does **not** claim to prove semantic correctness. It verifies the observable state and rules you gave it; omitted state cannot be checked.

## Development

```bash
pip install -e ".[dev]"
pytest -q
ruff check src tests
mypy src/effectproof
```

## License

Apache-2.0.
