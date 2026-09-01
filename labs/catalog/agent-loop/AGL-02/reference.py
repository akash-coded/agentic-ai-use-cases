"""AGL-02 — reference solution.

Tool results are a `user` turn: roles describe which side of the exchange the
content came from, and everything returning to the model is input.
"""


def advance(messages: list, response: dict, registry: dict) -> tuple[list, bool]:
    assistant_message = response["output"]["message"]
    stop = response.get("stopReason")

    new = list(messages)                      # never mutate the caller's history
    # copy the message in: a caller that mutates its response later must not
    # be able to rewrite what we have already recorded as history
    new.append({**assistant_message,
                "content": list(assistant_message.get("content", []))})

    if stop != "tool_use":
        return new, True

    results = [dispatch(block["toolUse"], registry)
               for block in assistant_message.get("content", [])
               if "toolUse" in block]

    if results:                                # one user turn, every result, in order
        new.append({"role": "user", "content": results})
    return new, False


def dispatch(tool_use: dict, registry: dict) -> dict:
    tid, name = tool_use.get("toolUseId"), tool_use.get("name")
    args = tool_use.get("input") or {}
    fn = registry.get(name)
    if fn is None or not callable(fn):
        available = ", ".join(sorted(registry)) or "(none registered)"
        return {"toolResult": {"toolUseId": tid, "status": "error",
                               "content": [{"text": f"No tool named {name!r}. Available: {available}."}]}}
    try:
        return {"toolResult": {"toolUseId": tid, "status": "success",
                               "content": [{"json": fn(**args)}]}}
    except BaseException as exc:  # noqa: BLE001
        return {"toolResult": {"toolUseId": tid, "status": "error",
                               "content": [{"text": f"Tool {name!r} failed: {type(exc).__name__}: {exc}"}]}}
