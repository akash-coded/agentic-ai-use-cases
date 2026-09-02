# MEM-101 · The summariser that runs every turn

`memory` · **medium** · `fix` · ~12 min · no AWS account

This history trimmer works. Conversations stay under budget and nothing crashes. It also costs a model call on **every single turn**, forever, and on long conversations it deletes the message the user just sent.

```python
def trim_history(messages, budget_tokens, summarise, keep_recent=4):
    older, recent = messages[:-keep_recent], messages[-keep_recent:]
    summary = summarise(older)                      # collapse the past
    msgs = [summary] + recent
    while sum(m["tokens"] for m in msgs) > budget_tokens:
        msgs.pop()                                  # drop until it fits
    return msgs
```

`summarise(msgs)` is provided by the caller and **costs a model call**. Messages carry a precomputed `tokens` int.

## Find both problems

One is about *when* work happens. The other is about *which end* of the list gets cut. Fix the function so that:

- `summarise` is called **only** when the history is over budget, and at most once
- the newest message is **never** removed
- under budget, the input is returned unchanged

Post the fixed function:

````markdown
/drill MEM-101

```python
def trim_history(messages, budget_tokens, summarise, keep_recent=4):
    ...
```
````

## What this proves

That you can see a permanent tax hiding inside a correct-looking function — and that you know which message in a buffer is the one you must never evict.
