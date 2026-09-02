# AGL-102 · Two bugs in a working dispatcher

`agent-loop` · **medium** · `fix` · ~12 min · no AWS account

This dispatcher passes its unit tests. It has run in production. It has two bugs, and both have ended real runs.

```python
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
```

## Find them

Both bugs are in what the function lets *escape* — one is a value that escapes, one is an exception that does. Read the code as the loop that calls it: what happens next, on the very next turn, in each case?

Fix the code so that **every** path returns a well-formed `toolResult` block, and the unknown-tool message names the tools that do exist.

Post the fixed function:

````markdown
/drill AGL-102

```python
def dispatch(tool_use, registry):
    ...
```
````

## What this proves

That you think about a dispatcher as a *boundary* — the one place whose entire job is to convert anything at all into a value the loop can continue from. The two bugs here are the two most common ways a boundary leaks.
