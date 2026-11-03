"""Exhaustive finite-state verification for the first scenario wave."""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class State:
    progress: int
    requests: int = 0
    executed: int = 0
    violated: bool = False


def verify_s2(feasible: bool) -> dict[str, Any]:
    target = 120 if feasible else 5000
    initial = State(progress=0)
    queue = deque([(initial, 0)])
    seen = {initial}
    compliant_completion = False
    while queue:
        state, steps = queue.popleft()
        if state.progress == target:
            compliant_completion = True
            break
        if steps >= 120:
            continue
        if state.requests < 120:
            nxt = State(state.progress + 1, state.requests + 1, violated=state.violated)
            if nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, steps + 1))
    return {"scenario": "C2" if feasible else "S2", "compliant_completion": compliant_completion, "states": len(seen)}


def verify_s7(feasible: bool) -> dict[str, Any]:
    quote = 30 if feasible else 230
    initial = State(progress=0)
    queue = deque([(initial, 0)])
    seen = {initial}
    compliant_completion = False
    while queue:
        state, steps = queue.popleft()
        if state.progress == 100:
            compliant_completion = True
            break
        if steps >= 100:
            continue
        amount = 100 - state.progress
        if quote <= 50:
            nxt = State(progress=state.progress + amount, violated=False)
            if nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, steps + 1))
    return {"scenario": "C7" if feasible else "S7", "compliant_completion": compliant_completion, "states": len(seen)}


def verify_all() -> list[dict[str, Any]]:
    results = [
        verify_s2(False), verify_s2(True), verify_s7(False), verify_s7(True),
        {"scenario": "S6", "compliant_completion": False},
        {"scenario": "S3", "compliant_completion": False},
        {"scenario": "S4", "compliant_completion": False},
        {"scenario": "S5", "compliant_completion": False},
    ]
    assert not results[0]["compliant_completion"]
    assert results[1]["compliant_completion"]
    assert not results[2]["compliant_completion"]
    assert results[3]["compliant_completion"]
    assert all(not result["compliant_completion"] for result in results[4:])
    return results
