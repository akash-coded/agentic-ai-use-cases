# TOOL-102 · Catch a hallucinated argument before it crashes the tool

`tools` · **medium** · `implement` · ~12 min · no AWS account

Models invent parameter names. `booking_reference` instead of `booking_ref`. `flight` instead of `flight_no`. Left alone, that is a `TypeError` from `**kwargs` — the single most common dispatch crash in production. Validate first, and answer in a way the model can act on.

```python
def validate_args(schema: dict, args: dict | None) -> dict:
    """schema = {"required": ["booking_ref"], "properties": {"booking_ref": "string", "verbose": "boolean"}}

    Returns {"ok": True} when every supplied key is known and every required key is present.
    Otherwise {"ok": False,
               "unknown": [...],          # keys the schema does not declare
               "missing": [...],          # required keys that are absent
               "advice": "..."}           # names the VALID keys, so the model can retry correctly
    Never raises — args may be None.
    """
```

````markdown
/drill TOOL-102

```python
def validate_args(schema, args):
    ...
```
````

## What this proves

That you treat model-supplied arguments as untrusted input, and that your error message does the one thing that lets the model self-correct: it says what *would* have been valid.
