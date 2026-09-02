# BED-101 · Predict the roles after two tool round trips

`bedrock` · **easy** · `predict` · ~8 min · no AWS account

No code to write. A correctly written loop runs this conversation:

1. The user asks *"Is XY7Q2M refundable?"*
2. The model requests `get_booking`. The loop appends the model's message, runs the tool, appends the result.
3. The model requests `get_fare_rules`. Same again.
4. The model answers.

## Your answer

What is the **sequence of `role` values** in `messages` when the loop finishes? One list, in order.

````markdown
/drill BED-101

```python
answer = ["user", "..."]
```
````

## What this proves

That you can see why the most common loop bug produces `['user', 'user']` — and why the API rejects it — before you have written a line.
