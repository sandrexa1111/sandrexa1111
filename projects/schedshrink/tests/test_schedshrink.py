import json

import pytest

from schedshrink import (
    Task,
    all_schedules,
    atomic_increment_scenario,
    execute,
    explore,
    lost_update_scenario,
    read,
    write_from,
)
from schedshrink.cli import main


def test_two_two_step_tasks_have_six_interleavings():
    scenario = lost_update_scenario()
    schedules = list(all_schedules(scenario.tasks))
    assert len(schedules) == 6
    assert len(set(schedules)) == 6


def test_sequential_schedule_passes():
    result = execute(lost_update_scenario(), ("A", "A", "B", "B"))
    assert result.passed
    assert result.final_state == {"counter": 2}


def test_racy_schedule_fails():
    result = execute(lost_update_scenario(), ("A", "B", "B", "A"))
    assert not result.passed
    assert result.final_state == {"counter": 1}
    assert result.context_switches == 2


def test_explorer_finds_minimum_context_switch_counterexample():
    result = explore(lost_update_scenario())
    assert result.explored == 6
    assert len(result.failures) == 4
    assert result.minimal is not None
    assert result.minimal.context_switches == 2
    assert result.minimal.schedule in {("A", "B", "B", "A"), ("B", "A", "A", "B")}


def test_atomic_increment_has_no_failure():
    result = explore(atomic_increment_scenario())
    assert result.explored == 2
    assert not result.failures
    assert result.minimal is None


def test_trace_captures_state_after_every_step():
    result = execute(lost_update_scenario(), ("A", "B", "B", "A"))
    assert [entry.shared["counter"] for entry in result.trace] == [0, 0, 1, 1]
    assert result.trace[0].local == {"seen": 0}


def test_incomplete_schedule_is_rejected():
    with pytest.raises(ValueError, match="incomplete"):
        execute(lost_update_scenario(), ("A", "A"))


def test_unknown_task_is_rejected():
    with pytest.raises(ValueError, match="unknown task"):
        execute(lost_update_scenario(), ("X", "A", "A", "B"))


def test_cli_json_exposes_minimal_counterexample(capsys):
    assert main(["lost-update", "--json"]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["failures"] == 4
    assert payload["minimal"]["context_switches"] == 2


def test_custom_task_steps_preserve_local_order():
    tasks = (Task("A", (read("x", "v"), write_from("x", "v", 1))), Task("B", (read("x", "v"), write_from("x", "v", 1))))
    for schedule in all_schedules(tasks):
        assert schedule.index("A") < len(schedule)
        assert schedule.count("A") == 2
        assert schedule.count("B") == 2
