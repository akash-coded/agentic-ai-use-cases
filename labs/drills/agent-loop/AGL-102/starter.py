def dispatch(tool_use, registry):
    tid = tool_use.get("toolUseId")
    name = tool_use.get("name")
    args = tool_use.get("input") or {}

    fn = registry.get(name)
    if fn is None:
        return None                                   # unknown tool

    try:
        result = fn(**args)
    except Exception as exc:
        return {"toolResult": {"toolUseId": tid, "status": "error",
                               "content": [{"text": f"{type(exc).__name__}: {exc}"}]}}

    return {"toolResult": {"toolUseId": tid, "status": "success",
                           "content": [{"json": result}]}}
