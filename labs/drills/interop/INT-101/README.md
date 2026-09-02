# INT-101 · Predict the A2A task lifecycle

`interop` · **easy** · `predict` · ~8 min · no AWS account

Agent A reads Agent B's card, sees `refund.assess`, and sends a task: *"Assess refund eligibility for booking XY7Q2M."*

B accepts it. B starts work, then realises it needs the fare class, which A did not include. A supplies it. B finishes and returns a result.

A2A task states: `submitted` · `working` · `input-required` · `completed` · `failed` · `canceled`.

## Your answer

The sequence of states the task passes through, in order:

````markdown
/drill INT-101

```python
answer = ["submitted", "..."]
```
````

Above the block, one sentence: what should A do if B stays in `working` for ten minutes?

## What this proves

That you see a remote agent as a state machine with an *interactive* state in the middle — the one that a naïve client treats as a hang — and that you have a timeout policy before you need one.
