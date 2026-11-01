"""Phase 0 check: one tool-call round trip through OpenRouter."""
import json
import os
import sys

try:
    from openai import OpenAI
except ImportError:
    sys.exit("Missing dependency. Run: pip install -r requirements.txt")

key = os.environ.get("OPENROUTER_API_KEY")
model = os.environ.get("HELLO_MODEL")
if not key or not model:
    sys.exit("Set OPENROUTER_API_KEY and HELLO_MODEL (a tool-capable model slug) first.")

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=key)

tools = [{
    "type": "function",
    "function": {
        "name": "add",
        "description": "Add two integers and return the sum.",
        "parameters": {
            "type": "object",
            "properties": {"a": {"type": "integer"}, "b": {"type": "integer"}},
            "required": ["a", "b"],
        },
    },
}]

messages = [{"role": "user", "content": "What is 17 + 25? Use the add tool."}]

first = client.chat.completions.create(model=model, messages=messages, tools=tools)
msg = first.choices[0].message
if not msg.tool_calls:
    sys.exit(f"FAIL: the model did not call a tool. It said: {msg.content!r}")

# Rebuild the assistant turn by hand: this is the same pattern the real harness will use.
messages.append({
    "role": "assistant",
    "content": msg.content or "",
    "tool_calls": [
        {
            "id": c.id,
            "type": "function",
            "function": {"name": c.function.name, "arguments": c.function.arguments},
        }
        for c in msg.tool_calls
    ],
})

for call in msg.tool_calls:
    args = json.loads(call.function.arguments)
    result = args["a"] + args["b"]
    print(f"tool call: {call.function.name}({args}) -> {result}")
    messages.append({"role": "tool", "tool_call_id": call.id, "content": str(result)})

second = client.chat.completions.create(model=model, messages=messages, tools=tools)
print("final answer:", second.choices[0].message.content)

tokens = sum(u.total_tokens for u in (first.usage, second.usage) if u)
print(f"tokens used: {tokens}")
print("OK: tool-call round trip works.")
