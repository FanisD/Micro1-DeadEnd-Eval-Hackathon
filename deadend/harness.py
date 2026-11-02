"""Minimal OpenAI-compatible agent loop with complete trajectory logging."""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Trajectory:
    messages: list[dict[str, Any]] = field(default_factory=list)
    calls: list[dict[str, Any]] = field(default_factory=list)
    stopped_how: str | None = None
    final_text: str | None = None
    steps: int = 0
    usage: dict[str, Any] | None = None
    error: str | None = None


class AgentHarness:
    def __init__(self, client: Any, model: str, max_steps: int = 20, retries: int = 2):
        self.client = client
        self.model = model
        self.max_steps = max_steps
        self.retries = retries

    def run(self, system_prompt: str, user_task: str, tools: list[dict[str, Any]], registry: dict[str, Any]) -> Trajectory:
        trajectory = Trajectory(messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_task}])
        for step in range(1, self.max_steps + 1):
            trajectory.steps = step
            response = self._complete(trajectory.messages, tools)
            if getattr(response, "usage", None):
                trajectory.usage = response.usage.model_dump() if hasattr(response.usage, "model_dump") else dict(response.usage)
            message = response.choices[0].message
            if not message.tool_calls:
                trajectory.final_text = message.content or ""
                trajectory.stopped_how = "plain_text"
                return trajectory
            assistant = {"role": "assistant", "content": message.content or "", "tool_calls": []}
            trajectory.messages.append(assistant)
            for call in message.tool_calls:
                try:
                    args = json.loads(call.function.arguments or "{}")
                except json.JSONDecodeError:
                    args = {}
                    result = {"error": "MALFORMED_TOOL_JSON"}
                else:
                    fn = registry.get(call.function.name)
                    result = fn(args) if fn else {"error": f"UNKNOWN_TOOL: {call.function.name}"}
                trajectory.calls.append({"name": call.function.name, "args": args, "result": result, "step": step})
                assistant["tool_calls"].append({"id": call.id, "type": "function", "function": {"name": call.function.name, "arguments": call.function.arguments}})
                trajectory.messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
                if call.function.name in {"finish", "escalate"}:
                    trajectory.stopped_how = call.function.name
                    return trajectory
        trajectory.stopped_how = "step_cap"
        return trajectory

    def _complete(self, messages: list[dict[str, Any]], tools: list[dict[str, Any]]) -> Any:
        last_error: Exception | None = None
        for attempt in range(self.retries + 1):
            try:
                return self.client.chat.completions.create(model=self.model, messages=messages, tools=tools)
            except Exception as error:
                last_error = error
                if attempt < self.retries:
                    time.sleep(2**attempt)
        detail = f"{type(last_error).__name__}: {last_error}" if last_error else "unknown error"
        raise RuntimeError(
            f"provider request failed after {self.retries + 1} attempts ({detail})"
        ) from last_error
