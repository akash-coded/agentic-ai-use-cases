# AGL-103 · Detect a loop that is stuck, not slow

`agent-loop` · **medium** · `implement` · ~12 min · no AWS account

A step cap turns a runaway into an *expensive* runaway. Detecting a repeat turns it into a cheap, diagnosable one. The trick is fingerprinting what the model asked for — and getting the fingerprint exactly right.

```python
def call_signature(message: dict) -> tuple:
    """A hashable fingerprint of the tool calls in one assistant message.

    - One entry per toolUse block: (name, sorted (key, value) pairs of its input)
    - Order-insensitive across calls: the same set of calls in a different order
      is the same signature
    - A message with no toolUse blocks → ()
    """

def is_oscillating(previous: tuple, current: tuple) -> bool:
    """True when the model asked for the same thing twice in a row.
    An empty signature never counts as oscillation."""
```

## The subtle part

`get_booking("WRONG")` followed by `get_booking("XY7Q2M")` is **not** oscillation — that is the model correcting itself, which is exactly what you asked it to do when your dispatcher named the valid arguments. Fingerprint on name **and** arguments, or your detector kills the run at the moment it recovers.

````markdown
/drill AGL-103

```python
def call_signature(message):
    ...
def is_oscillating(previous, current):
    ...
```
````

## What this proves

That you can distinguish *the same question asked the same way twice* from *the same tool used twice* — and that you know why the difference matters.
