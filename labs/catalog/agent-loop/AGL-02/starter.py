"""AGL-02 — close the loop.

Put the assistant's request and the tool's answer back into history, in the
right roles and the right order.
"""


def advance(messages: list, response: dict, registry: dict) -> tuple[list, bool]:
    """Append one turn of the conversation.

    Returns:
        (new_messages, done)
    """
    assistant_message = response["output"]["message"]
    stop = response.get("stopReason")

    # TODO 1 — work on a copy of the list, and copy the message in too. Mutating
    #          the caller's history is how two loops sharing a list corrupt each
    #          other; aliasing the response lets a retry wrapper rewrite history.

    # TODO 2 — on "end_turn": append the assistant message and finish.

    # TODO 3 — on "tool_use": append the assistant message VERBATIM first.
    #          Skipping this is why the model repeats its request.

    # TODO 4 — dispatch EVERY toolUse block, then append ONE user message
    #          carrying all the results, in request order.

    raise NotImplementedError("implement advance()")


# --- provided, working: this lab is about history, not dispatch -------------
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
