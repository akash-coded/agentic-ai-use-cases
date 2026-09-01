"""Shared fixtures for AGL-02."""

REGISTRY = {
    "get_booking": lambda booking_ref: {"ref": booking_ref, "status": "CANCELLED"},
    "get_disruption": lambda flight_no, date: {"flight": flight_no, "date": date, "cause": "weather"},
}


def assistant_tool_turn(*calls):
    """calls: (id, name, input) tuples -> a tool_use response."""
    return {
        "output": {"message": {"role": "assistant",
                               "content": [{"toolUse": {"toolUseId": i, "name": n, "input": a}}
                                           for i, n, a in calls]}},
        "stopReason": "tool_use",
    }


def assistant_text_turn(text):
    return {
        "output": {"message": {"role": "assistant", "content": [{"text": text}]}},
        "stopReason": "end_turn",
    }


def roles(messages):
    return [m["role"] for m in messages]


def tool_results(message):
    return [b["toolResult"] for b in message.get("content", []) if "toolResult" in b]
