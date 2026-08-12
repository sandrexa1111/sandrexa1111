from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from .core import Exploration, atomic_increment_scenario, explore, lost_update_scenario


def _result_dict(result: Exploration) -> dict[str, Any]:
    if result.minimal is None:
        return {"explored": result.explored, "failures": 0, "minimal": None}
    minimal = result.minimal
    return {
        "explored": result.explored,
        "failures": len(result.failures),
        "minimal": {
            "schedule": list(minimal.schedule),
            "context_switches": minimal.context_switches,
            "schedule_id": minimal.schedule_id,
            "final_state": dict(minimal.final_state),
            "trace": [
                {
                    "index": entry.index,
                    "task": entry.task,
                    "step": entry.step,
                    "shared": dict(entry.shared),
                    "local": dict(entry.local),
                }
                for entry in minimal.trace
            ],
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="interleaving-lab",
        description=(
            "Explore deterministic cooperative schedules and minimize "
            "failing interleavings."
        ),
    )
    parser.add_argument("scenario", choices=["lost-update", "atomic-increment"])
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)

    if args.scenario == "lost-update":
        scenario = lost_update_scenario()
    else:
        scenario = atomic_increment_scenario()

    result = explore(scenario)
    payload = _result_dict(result)
    if args.as_json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"scenario: {scenario.name}")
        print(f"schedules explored: {result.explored}")
        print(f"failing schedules: {len(result.failures)}")
        if result.minimal is None:
            print("minimal failure: none")
        else:
            minimal = result.minimal
            print(f"minimal failing schedule: {' '.join(minimal.schedule)}")
            print(f"context switches: {minimal.context_switches}")
            print(f"final state: {dict(minimal.final_state)}")
            for entry in minimal.trace:
                shared = dict(entry.shared)
                local = dict(entry.local)
                print(
                    f"  {entry.index}: {entry.task} | {entry.step} | "
                    f"shared={shared} local={local}"
                )
    return 1 if result.minimal is not None else 0


if __name__ == "__main__":
    sys.exit(main())
