"""AGL-03 — stop the loop.

Three exits: converged, budget exhausted, oscillating. Only one is an answer.
"""


def run_loop(messages: list, model, registry: dict, max_steps: int = 6) -> dict:
    """Drive the agent loop to a bounded conclusion."""
    history = list(messages)
    steps = 0

    # TODO 1 — loop while steps < max_steps. Count a step per MODEL CALL,
    #          not per tool call.

    # TODO 2 — on end_turn: pull the text out and return outcome="answered".

    # TODO 3 — detect oscillation. Build a signature of the tool calls this turn
    #          (name + arguments). If it matches the previous turn's signature,
    #          stop with outcome="stuck" — do not burn the rest of the budget.

    # TODO 4 — if the budget runs out, return outcome="exhausted" with a reason.
    #          Decide first (see the brief) what the caller should receive.

    # TODO 5 — the model call itself can raise: providers time out, connections drop.
    #          That is outcome="failed", not a traceback. Keep the history and the
    #          step count the caller has already paid for.

    raise NotImplementedError("implement run_loop()")


# --- provided ---------------------------------------------------------------
def advance(messages, response, registry):
    am = response["output"]["message"]
    new = list(messages)
    new.append({**am, "content": list(am.get("content", []))})
    if response.get("stopReason") != "tool_use":
        return new, True
    results = [dispatch(b["toolUse"], registry) for b in am.get("content", []) if "toolUse" in b]
    if results:
        new.append({"role": "user", "content": results})
    return new, False


def dispatch(tool_use, registry):
    tid, name = tool_use.get("toolUseId"), tool_use.get("name")
    args = tool_use.get("input") or {}
    fn = registry.get(name)
    if fn is None or not callable(fn):
        return {"toolResult": {"toolUseId": tid, "status": "error",
                               "content": [{"text": f"No tool named {name!r}."}]}}
    try:
        return {"toolResult": {"toolUseId": tid, "status": "success", "content": [{"json": fn(**args)}]}}
    except BaseException as exc:  # noqa: BLE001
        return {"toolResult": {"toolUseId": tid, "status": "error",
                               "content": [{"text": f"Tool {name!r} failed: {exc}"}]}}


def answer_text(message) -> str:
    return " ".join(b["text"] for b in message.get("content", []) if "text" in b).strip()


def call_signature(message):
    """A hashable fingerprint of the tool calls in one assistant message."""
    calls = [(b["toolUse"]["name"], tuple(sorted((b["toolUse"].get("input") or {}).items())))
             for b in message.get("content", []) if "toolUse" in b]
    return tuple(sorted(calls))
