"""AGL-01 — reference solution.

Policy chosen: return an error result naming the available tools.
Rationale: the loop stays alive and the model is given what it needs to correct
itself on the next turn. Raising kills a recoverable situation; skipping silently
leaves the model with no reply to a question it asked, which it will paper over.
"""


def dispatch(tool_use: dict, registry: dict) -> dict:
    tool_use_id = tool_use.get("toolUseId")
    name = tool_use.get("name")
    args = tool_use.get("input") or {}

    fn = registry.get(name)
    if fn is None or not callable(fn):
        available = ", ".join(sorted(registry)) or "(none registered)"
        return _err(tool_use_id,
                    f"No tool named {name!r}. Available tools: {available}. "
                    f"Choose one of these or answer without a tool.")

    try:
        result = fn(**args)
    except BaseException as exc:  # noqa: BLE001 - a tool must never kill the loop
        return _err(tool_use_id,
                    f"Tool {name!r} failed: {type(exc).__name__}: {exc}. "
                    f"Do not assume a value — say you could not check.")

    return _ok(tool_use_id, result)


def _ok(tool_use_id: str, payload) -> dict:
    return {"toolResult": {"toolUseId": tool_use_id,
                           "content": [{"json": payload}],
                           "status": "success"}}


def _err(tool_use_id: str, message: str) -> dict:
    return {"toolResult": {"toolUseId": tool_use_id,
                           "content": [{"text": message}],
                           "status": "error"}}
