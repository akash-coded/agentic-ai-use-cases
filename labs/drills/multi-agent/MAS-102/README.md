# MAS-102 · A swarm that does not know how to stop

`multi-agent` · **medium** · `fix` · ~12 min · no AWS account

This swarm works beautifully when the agents converge. When they do not, it is a spending rate with a diagram.

```python
def run_swarm(step, task):
    """step(task, state) -> (state, done, tokens_used). Loops until done."""
    state, spent = {}, 0
    while True:
        state, done, tokens = step(task, state)
        spent += tokens
        if done:
            return {"outcome": "completed", "state": state, "tokens": spent}
```

## Fix it

Add two bounds, both **in code** — a cap in a prompt is a suggestion:

- `max_rounds` (default 8) — stop after this many calls to `step`
- `max_tokens` (default 50_000) — stop once `spent` exceeds it

When a bound binds, return `{"outcome": "stopped", "reason": "<which bound, and the numbers>", "state": state, "tokens": spent, "rounds": n}`. A converged run returns `"completed"` exactly as before, plus `"rounds"`.

````markdown
/drill MAS-102

```python
def run_swarm(step, task, max_rounds=8, max_tokens=50_000):
    ...
```
````

## What this proves

That you never ship a loop whose termination depends on the model's cooperation, and that a stop is reported as an outcome — not a crash, not a fake completion.
