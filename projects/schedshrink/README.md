# SchedShrink

Deterministic concurrency schedule exploration for small, explicit state machines.

SchedShrink enumerates legal interleavings while preserving each task's local order, replays every schedule against an invariant, and returns the failing interleaving with the fewest context switches.

The goal is not to replace production race detectors. It is to make a concurrency failure **small, replayable, and explainable** once a problem can be represented as cooperative steps.

> **Status:** experimental `v0.1.0`, zero runtime dependencies.

## Lost-update demo

Two workers both implement `counter += 1` as a read followed by a write.

```bash
pip install -e .
schedshrink lost-update
```

Example output:

```text
scenario: lost-update
schedules explored: 6
failing schedules: 4
minimal failing schedule: A B B A
context switches: 2
final state: {'counter': 1}
```

The sequential schedules pass. SchedShrink finds the smallest-preemption counterexample that loses an update and emits the state after every step.

Compare with an atomic increment:

```bash
schedshrink atomic-increment
```

No failing schedules are found.

## Python API

```python
from schedshrink import Scenario, Task, explore, read, write_from

worker_a = Task("A", (read("counter", "seen"), write_from("counter", "seen", add=1)))
worker_b = Task("B", (read("counter", "seen"), write_from("counter", "seen", add=1)))

scenario = Scenario(
    initial={"counter": 0},
    tasks=(worker_a, worker_b),
    invariant=lambda state: state["counter"] == 2,
)

result = explore(scenario)
print(result.minimal.schedule)
```

## Scope and limitations

- Cooperative explicit steps, not arbitrary Python thread instrumentation.
- Exhaustive enumeration grows combinatorially; v0.1 is intended for small scenarios.
- “Minimal” currently means the failing full schedule with the fewest context switches; steps are not deleted from the program.
- It finds counterexamples to the invariant you provide. An omitted invariant cannot be inferred.

Those limits are deliberate: the first release keeps the scheduler deterministic and the claims checkable.

## Development

```bash
pip install -e ".[dev]"
pytest -q
ruff check src tests
mypy src/schedshrink
```

## License

Apache-2.0.
