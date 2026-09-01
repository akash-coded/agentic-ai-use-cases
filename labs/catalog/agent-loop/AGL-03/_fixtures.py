"""Scripted models for AGL-03. No network, fully deterministic."""

REGISTRY = {
    "get_booking": lambda booking_ref="X": {"ref": booking_ref, "status": "CANCELLED"},
    "get_fare_rules": lambda fare_class="Y": {"class": fare_class, "refundable": True},
}


def _tool(i, name, args=None):
    return {"toolUse": {"toolUseId": i, "name": name, "input": args or {}}}


def tool_turn(*blocks):
    return {"output": {"message": {"role": "assistant", "content": list(blocks)}},
            "stopReason": "tool_use"}


def text_turn(text):
    return {"output": {"message": {"role": "assistant", "content": [{"text": text}]}},
            "stopReason": "end_turn"}


def scripted(*responses):
    """A model that returns each response in turn, then repeats the last one."""
    state = {"i": 0}

    def model(_messages):
        i = min(state["i"], len(responses) - 1)
        state["i"] += 1
        return responses[i]

    model.calls = state
    return model


def always(response):
    def model(_messages):
        return response
    return model


def alternating(a, b):
    state = {"i": 0}

    def model(_messages):
        r = a if state["i"] % 2 == 0 else b
        state["i"] += 1
        return r
    return model


TOOL_A = tool_turn(_tool("a", "get_booking", {"booking_ref": "XY7Q2M"}))
TOOL_B = tool_turn(_tool("b", "get_fare_rules", {"fare_class": "QW7"}))
DONE = text_turn("Yes — the fare is refundable because the carrier cancelled.")
