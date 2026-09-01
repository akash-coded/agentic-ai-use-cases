# AGL-03 · Solution

## Why abstain rather than best-effort

A loop that hit its cap did not answer. It ran out of turns while still working.

Returning "the best text so far" produces a string that is indistinguishable, at the call site, from a
real answer. The caller has no way to know it is holding an unfinished process, so it renders it to a user
who has no way either. You have taken a *visible* failure — the loop did not converge — and converted it
into an *invisible* one. That direction is always wrong, and it is the same argument as tool-failure
honesty in [AGL-01](../AGL-01/).

Raising is defensible but leaks internals: the caller now handles agent mechanics in an `except` block.
A structured outcome keeps the failure inside the contract.

## Signature on name *and* arguments

The subtlest part of this lab is the false positive in the Break phase.

```python
# too coarse — punishes self-correction
signature = tuple(sorted(name for name, _ in calls))

# right — a repeat means the same question asked the same way
signature = tuple(sorted((name, tuple(sorted(args.items()))) for name, args in calls))
```

In [AGL-01](../AGL-01/) you deliberately built an error message telling the model to retry with a valid
argument. If your oscillation detector keys on the tool name alone, the retry you engineered looks
identical to a stall, and you kill the run at exactly the moment it was recovering.

Oscillation is *the same question, asked the same way, twice*. Not *the same tool, twice*.

## Why stop on the repeat instead of at the cap

Both terminate. The difference is diagnosis and cost.

- `exhausted` after 10 steps tells you "it needed more room" — and someone will raise the cap.
- `stuck` after 2 steps tells you "it asked the same thing twice" — which points at the tool, not the cap.

They are different bugs and they want different fixes. Collapsing them into one outcome loses the
information at the exact moment you need it, and pays for eight extra model calls to lose it.

## The fourth outcome

The Break phase adds a case the Apply phase does not: the **model call itself** raises. Providers time
out; connections drop mid-run.

Letting that propagate throws away everything the run already paid for — the history, the step count, the
partial tool results. The caller gets a traceback instead of a state it can log, retry from, or escalate.
`outcome="failed"` costs one branch and keeps all of it.

This is the same shape as [AGL-01](../AGL-01/)'s dispatcher: at a boundary, convert anything at all into
a value the layer above can reason about.

## The cap belongs in code

Not in the prompt. "Do not use more than six tool calls" is a request; `while steps < max_steps` is a
fact. Every runaway-loop incident in the
[runbook](../../../../cheatsheets/runbooks/incident-runaway-loop.md) traces back to a cap that was
advisory, or set so high it never bound.

## Field guide

[Cost Cliff Map](../../../../cheatsheets/frameworks/cost-cliff-map.md) cliffs 1–3 ·
[Abstention Budget](../../../../cheatsheets/frameworks/abstention-budget.md) ·
[Runbook · runaway loop](../../../../cheatsheets/runbooks/incident-runaway-loop.md)
