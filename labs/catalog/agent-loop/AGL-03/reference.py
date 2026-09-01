"""AGL-03 — reference solution.

Cap bound => abstain with a reason. A loop that stopped did not answer, and the
caller must be able to tell those apart without parsing prose.
"""


def run_loop(messages: list, model, registry: dict, max_steps: int = 6) -> dict:
    history = list(messages)
    steps = 0
    previous_signature = None

    while steps < max_steps:
        try:
            response = model(history)
        except BaseException as exc:  # noqa: BLE001 - a provider fault is an outcome, not a crash
            return {"outcome": "failed", "answer": None, "steps": steps, "messages": history,
                    "reason": f"The model call failed: {type(exc).__name__}: {exc}. "
                              f"History and step count are preserved for the caller."}
        steps += 1
        assistant = response["output"]["message"]

        if response.get("stopReason") != "tool_use":
            history, _ = advance(history, response, registry)
            return {"outcome": "answered", "answer": answer_text(assistant),
                    "steps": steps, "messages": history, "reason": None}

        signature = call_signature(assistant)
        if signature and signature == previous_signature:
            history, _ = advance(history, response, registry)
            names = ", ".join(sorted({n for n, _ in signature}))
            return {"outcome": "stuck", "answer": None, "steps": steps, "messages": history,
                    "reason": f"Repeated the same tool call(s) ({names}) twice in a row without "
                              f"progressing; stopped rather than spending the remaining budget."}
        previous_signature = signature

        history, _ = advance(history, response, registry)

    return {"outcome": "exhausted", "answer": None, "steps": steps, "messages": history,
            "reason": f"Reached the {max_steps}-step budget without the model finishing. "
                      f"No answer was produced; escalate rather than reporting a partial result."}


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
    calls = [(b["toolUse"]["name"], tuple(sorted((b["toolUse"].get("input") or {}).items())))
             for b in message.get("content", []) if "toolUse" in b]
    return tuple(sorted(calls))
