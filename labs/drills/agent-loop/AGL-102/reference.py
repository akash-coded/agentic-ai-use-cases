def dispatch(tool_use, registry):
    tid = tool_use.get("toolUseId")
    name = tool_use.get("name")
    args = tool_use.get("input") or {}

    fn = registry.get(name)
    if fn is None or not callable(fn):
        available = ", ".join(sorted(registry)) or "(none registered)"
        return {"toolResult": {"toolUseId": tid, "status": "error",
                               "content": [{"text": f"No tool named {name!r}. Available: {available}."}]}}
    try:
        result = fn(**args)
    except BaseException as exc:  # noqa: BLE001 — a boundary catches everything
        return {"toolResult": {"toolUseId": tid, "status": "error",
                               "content": [{"text": f"Tool {name!r} failed: {type(exc).__name__}: {exc}"}]}}
    return {"toolResult": {"toolUseId": tid, "status": "success",
                           "content": [{"json": result}]}}
