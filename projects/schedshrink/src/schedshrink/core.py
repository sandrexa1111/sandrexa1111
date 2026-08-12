from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Callable, Iterable, Iterator, Mapping, MutableMapping, Sequence

State = MutableMapping[str, int]
Locals = MutableMapping[str, int]
StepFn = Callable[[State, Locals], None]
Invariant = Callable[[Mapping[str, int]], bool]


@dataclass(frozen=True)
class Step:
    name: str
    run: StepFn


@dataclass(frozen=True)
class Task:
    name: str
    steps: tuple[Step, ...]


@dataclass(frozen=True)
class Scenario:
    initial: Mapping[str, int]
    tasks: tuple[Task, ...]
    invariant: Invariant
    name: str = "scenario"


@dataclass(frozen=True)
class TraceEntry:
    index: int
    task: str
    step: str
    shared: Mapping[str, int]
    local: Mapping[str, int]


@dataclass(frozen=True)
class Execution:
    schedule: tuple[str, ...]
    passed: bool
    final_state: Mapping[str, int]
    trace: tuple[TraceEntry, ...]

    @property
    def context_switches(self) -> int:
        return sum(a != b for a, b in zip(self.schedule, self.schedule[1:]))

    @property
    def schedule_id(self) -> str:
        raw = json.dumps(self.schedule, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True)
class Exploration:
    explored: int
    failures: tuple[Execution, ...]
    minimal: Execution | None


def all_schedules(tasks: Sequence[Task]) -> Iterable[tuple[str, ...]]:
    """Enumerate all interleavings while preserving each task's local order."""
    remaining = {task.name: len(task.steps) for task in tasks}
    prefix: list[str] = []

    def visit() -> Iterator[tuple[str, ...]]:
        if not any(remaining.values()):
            yield tuple(prefix)
            return
        for name in sorted(remaining):
            if remaining[name] == 0:
                continue
            remaining[name] -= 1
            prefix.append(name)
            yield from visit()
            prefix.pop()
            remaining[name] += 1

    yield from visit()


def execute(scenario: Scenario, schedule: Sequence[str]) -> Execution:
    tasks = {task.name: task for task in scenario.tasks}
    positions = {task.name: 0 for task in scenario.tasks}
    locals_by_task: dict[str, dict[str, int]] = {task.name: {} for task in scenario.tasks}
    shared: dict[str, int] = dict(scenario.initial)
    trace: list[TraceEntry] = []

    for index, task_name in enumerate(schedule):
        if task_name not in tasks:
            raise ValueError(f"unknown task in schedule: {task_name}")
        task = tasks[task_name]
        position = positions[task_name]
        if position >= len(task.steps):
            raise ValueError(f"task {task_name!r} has no step remaining at schedule index {index}")
        step = task.steps[position]
        local = locals_by_task[task_name]
        step.run(shared, local)
        positions[task_name] += 1
        trace.append(
            TraceEntry(
                index=index,
                task=task_name,
                step=step.name,
                shared=dict(shared),
                local=dict(local),
            )
        )

    unfinished = {name: len(tasks[name].steps) - pos for name, pos in positions.items() if pos != len(tasks[name].steps)}
    if unfinished:
        raise ValueError(f"schedule is incomplete: {unfinished}")

    return Execution(tuple(schedule), bool(scenario.invariant(shared)), dict(shared), tuple(trace))


def explore(scenario: Scenario, limit: int | None = None) -> Exploration:
    failures: list[Execution] = []
    explored = 0
    for schedule in all_schedules(scenario.tasks):
        result = execute(scenario, schedule)
        explored += 1
        if not result.passed:
            failures.append(result)
        if limit is not None and explored >= limit:
            break
    minimal = min(
        failures,
        key=lambda result: (result.context_switches, result.schedule, result.schedule_id),
        default=None,
    )
    return Exploration(explored=explored, failures=tuple(failures), minimal=minimal)


def read(key: str, into: str) -> Step:
    def operation(shared: State, local: Locals) -> None:
        local[into] = shared[key]

    return Step(f"read {key} -> {into}", operation)


def write_from(key: str, source: str, add: int = 0) -> Step:
    def operation(shared: State, local: Locals) -> None:
        shared[key] = local[source] + add

    suffix = f" + {add}" if add else ""
    return Step(f"write {key} <- {source}{suffix}", operation)


def add_atomic(key: str, amount: int) -> Step:
    def operation(shared: State, local: Locals) -> None:
        del local
        shared[key] += amount

    return Step(f"atomic add {amount} to {key}", operation)


def lost_update_scenario() -> Scenario:
    def worker(name: str) -> Task:
        return Task(name, (read("counter", "seen"), write_from("counter", "seen", add=1)))

    return Scenario(
        name="lost-update",
        initial={"counter": 0},
        tasks=(worker("A"), worker("B")),
        invariant=lambda state: state["counter"] == 2,
    )


def atomic_increment_scenario() -> Scenario:
    return Scenario(
        name="atomic-increment",
        initial={"counter": 0},
        tasks=(Task("A", (add_atomic("counter", 1),)), Task("B", (add_atomic("counter", 1),))),
        invariant=lambda state: state["counter"] == 2,
    )
