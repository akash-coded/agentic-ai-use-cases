# Exercise 2 solution — Complete the decision tree

## Answer

**1-q** Autonomy spec  ·  **2-s** Statistical acceptance plan  ·  **3-p** Open-decisions log.

## Teaching point

Each conditional artefact is tied to one specific trigger. Reading the tree is matching a leaf to its condition, never guessing.

## The completed tree

| Blank | Condition above it | Artefact |
|---|---|---|
| Blank 1 | agent ACTS | q. Autonomy spec |
| Blank 2 | output is PROBABILISTIC | s. Statistical acceptance plan |
| Blank 3 | decisions still OPEN | p. Open-decisions log |
| (shown) | runs with OTHER agents | Registry entry |

## The trap

**t, Tool contract** is a real artefact, but it is *mandatory*, not conditional, so it never hangs off a trigger in this tree. Placing it means confusing a mandatory artefact for a conditional one, which is the distinction the whole session turns on.

**r, Rollback runbook** is the unused bank option. It is optional and tied to high-impact actions, not to any of these three conditions.
