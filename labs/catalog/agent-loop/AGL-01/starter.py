"""AGL-01 — dispatch a tool call.

Turn a model's tool request into a result the loop can continue from.
Read the brief first:  python labs/runner/labctl.py show AGL-01
"""


def dispatch(tool_use: dict, registry: dict) -> dict:
    """Execute one tool call and return a toolResult block.

    Args:
        tool_use: {"toolUseId": str, "name": str, "input": dict}
        registry: {tool_name: callable}

    Returns:
        {"toolResult": {"toolUseId": str,
                        "content": [{"json": ...}] or [{"text": ...}],
                        "status": "success" | "error"}}
    """
    tool_use_id = tool_use.get("toolUseId")
    name = tool_use.get("name")
    args = tool_use.get("input") or {}

    # TODO 1 — the tool may not exist. Decide what the model sees, and make sure
    #          the message names the tools that DO exist so it can self-correct.

    # TODO 2 — call the tool with **args and wrap the return value in a success result.

    # TODO 3 — a tool that raises must not kill the loop. Return an error result instead,
    #          with a message the model can act on.

    raise NotImplementedError("implement dispatch()")


def _ok(tool_use_id: str, payload) -> dict:
    """Helper: a success toolResult. Use it or write your own."""
    return {"toolResult": {"toolUseId": tool_use_id,
                           "content": [{"json": payload}],
                           "status": "success"}}


def _err(tool_use_id: str, message: str) -> dict:
    """Helper: an error toolResult. The message is what the model reads next."""
    return {"toolResult": {"toolUseId": tool_use_id,
                           "content": [{"text": message}],
                           "status": "error"}}
