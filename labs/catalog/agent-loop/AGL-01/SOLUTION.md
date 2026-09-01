# AGL-01 · Solution

Read this after you have a working answer, not before.

## The decision, and why

Three options were on the table for an unknown tool. The reference returns an **error result naming the
available tools**.

**Why not raise.** An unknown tool is not an exceptional condition — it is a normal, expected consequence
of giving a language model a menu. It will occasionally order something that is not on it. Raising
converts a recoverable turn into a dead run, and in production it converts a bad answer into an outage
page.

**Why not skip silently.** This is the option that looks harmless. It is the worst of the three. From the
model's side, it asked a question and received nothing back. Models handle that badly: the two usual
outcomes are repeating the identical call (a loop that never converges) or answering from nothing while
sounding exactly as confident as when it had data. You have converted a visible failure into an invisible
one, which is the wrong direction.

**Why the error result works.** It keeps the loop alive, it costs exactly one turn, and — provided you
name the available tools — it gives the model everything it needs to correct itself. This is the same
principle as tool failure honesty: the loop should always be able to continue, and the model should always
be told the truth about what happened.

## The bit almost everyone gets wrong

```python
except Exception:
```

Three of the four Break checks exist because of that line.

- `SystemExit` and `KeyboardInterrupt` inherit from `BaseException`, not `Exception`. A dependency that
  calls `sys.exit()` on a config problem — and several do — takes your agent down with it.
- A registry entry that is a string passes a `None` check and fails at call time.
- A hallucinated parameter name raises `TypeError` from `**args`, not from inside the tool.

`except BaseException` is normally a smell. In a dispatcher it is the point: this function's entire job is
to convert *anything at all* into a block the loop can continue from. It is the boundary, and boundaries
catch everything.

## What the error text should say

Compare:

```
"Tool failed."
"Tool 'get_refund' failed: TimeoutError: upstream took too long.
 Do not assume a value — say you could not check."
```

The second is longer and it is worth the tokens. It tells the model what happened, and it tells it what
*not* to do — which is the failure you are actually trying to prevent. An agent that is told a tool timed
out will frequently answer anyway unless you tell it not to.

## Where this shows up next

- [AGL-02](../AGL-02/) — the result you just built has to go back into history in the right order
- `AGL-04` (specified, [not yet built](../../../PATHWAY.md#-agent-loop)) — what the agent should *say* when dispatch returns an error
- [TOOL-03](../../tools/TOOL-03/) — why `[]` is more dangerous than an exception

## Field guide

[Tool Surface Audit](../../../../cheatsheets/frameworks/tool-surface-audit.md) · failure honesty is one of
the six axes · [Failure Signature Catalog](../../../../cheatsheets/frameworks/failure-signature-catalog.md)
rows 1 and 13
