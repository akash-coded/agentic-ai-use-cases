# MAS-101 · Cost this topology by hand

`multi-agent` · **medium** · `predict` · ~10 min · no AWS account

No code. A design review is proposing a delegation topology. Compute its **H×** — total tokens divided by what a single agent would spend — to two decimal places.

## The model

```
delegation total = base_context                             # the orchestrator's own context
                 + orchestrator_turns × base_context        # its reasoning turns
                 + specialists × (handoff_context + result) # the handoffs
                 + base_context + specialists × result      # the MERGE call — carries every result

H× = total ÷ base_context
```

## The proposal

| | |
| --- | --- |
| Specialists | 3 |
| `base_context` | 2 000 tokens |
| `handoff_context` (what crosses each handoff) | 500 |
| `result` (each specialist's output) | 300 |
| `orchestrator_turns` | 3 |

## Your answer

````markdown
/drill MAS-101

```python
answer = 0.00   # H×, two decimal places
```
````

Above the code block, say in one sentence what the 3 specialists are *buying* for that multiple. If you cannot, that is the review's finding.

## What this proves

That you can turn a whiteboard shape into a number a reviewer can argue with — and that you include the two terms the diagram hides: the orchestrator's own reasoning turns, and the merge call that carries every specialist's output.
