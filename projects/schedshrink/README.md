# interleaving-lab

A deterministic playground for reproducing small concurrency failures by exploring legal cooperative task schedules.

The repository path is still `schedshrink` for compatibility, but the project name is **interleaving-lab**.

## What it does

`interleaving-lab`:

- enumerates legal task interleavings while preserving each task's local order
- executes each schedule against shared state
- evaluates a user-defined invariant
- records a replayable execution trace
- returns a failing schedule with the fewest context switches

The included lost-update example explores all six legal schedules for two read/write workers and isolates a small failing interleaving.

## Install

```bash
cd projects/schedshrink
python -m pip install -e ".[dev]"
```

## Run

```bash
interleaving-lab lost-update
```

## Development

```bash
pytest -q
ruff check src tests
mypy src/schedshrink
```

## Scope

This is cooperative schedule exploration for small modeled systems. It does not instrument arbitrary OS threads or claim exhaustive coverage of production concurrency behavior.
