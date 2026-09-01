# MEM-01 · Solution

## Threshold, not schedule

The first check that catches people is `t_no_call`. Summarising every turn is simpler to write and costs a
model call on every single turn, forever — a permanent tax on a path that rarely needs to fire.

Check the total, act only when it is exceeded. On most conversations that means never.

## Summarising is not guaranteed to be enough

The naive shape is:

```python
if over_budget:
    summarise_the_old_stuff()
return history          # ← assumes it fits now
```

It might not. The protected `keep_recent` block plus the summary can still exceed the budget, and if you
return without checking, you have shipped silent truncation to whatever calls you next.

The fallback loop is the actual lab. And the fallback loop is where the Break phase lives, because
`while total > budget: pop()` does not terminate when one message alone is bigger than the budget.

```python
while total > budget_tokens and len(msgs) > 1:   # the guard is the whole fix
```

## Report the truth when it does not fit

For an oversized single message the reference returns it and reports the real token count, over budget.
That is deliberate. The alternatives are to return nothing (you have deleted the user's question) or to
truncate the text (you have silently changed what they asked). Returning it with an honest number lets the
caller decide — reject, split, or escalate — with the information it needs.

A function that cannot satisfy its contract should say so, not pretend.

## The invariant worth stating out loud

> **The newest message is never evicted.**

`keep_recent=0` should not be able to delete the message you are answering. Configuration values arrive
from environments, feature flags and hurried edits; an invariant that depends on one being sensible is not
an invariant.

## What "deliberate eviction" buys you

Every buffer has an eviction policy. The difference is whether anyone chose it.

An accidental policy drops the oldest turn — reliably the one where the user stated their constraint. A
deliberate one summarises it, so the constraint survives in compressed form, and counts what it dropped so
you can see the cost in a log line rather than in a complaint.

## Field guide

[Context Budget Ledger](../../../../cheatsheets/frameworks/context-budget-ledger.md) — the overflow
protocol · [Token Tax Ledger](../../../../cheatsheets/frameworks/token-tax-ledger.md) — the history tax
