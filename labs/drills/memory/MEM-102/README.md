# MEM-102 · Predict which turns survive the trim

`memory` · **medium** · `predict` · ~10 min · no AWS account

The policy, in order:

1. If the total fits the budget, return the history unchanged.
2. Otherwise protect the last `keep_recent` messages; summarise everything older into **one** message `S` placed at the front. `S` costs **80** tokens.
3. If it *still* does not fit, evict from the **front** until it does — never the newest message.

## The input

| id | t1 | t2 | t3 | t4 | t5 | t6 |
| --- | --- | --- | --- | --- | --- | --- |
| tokens | 100 | 100 | 100 | 100 | 150 | 100 |

`budget = 500`, `keep_recent = 2`.

## Your answer

The ids that remain, in order (use `"S"` for the summary):

````markdown
/drill MEM-102

```python
answer = ["...", "..."]
```
````

Then the real question, in a sentence above the block: **t5 is the message where the user stated their wheelchair requirement.** Did it survive? Would it have survived with `keep_recent = 1`?

## What this proves

That you can trace an eviction policy and see, before it runs, which user statement it will forget.
