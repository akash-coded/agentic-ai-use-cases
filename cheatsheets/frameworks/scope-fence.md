# The Scope Fence

> **One line:** agentic scope creeps because "the agent could also…" is always true — the fence is a
> pre-agreed rule for what crosses.

For product managers, POs and anyone who owns a roadmap. Agents invite scope creep more than any other
software, because their capability boundary is genuinely fuzzy and every stakeholder can imagine one more
thing.

---

## Why agents creep worse than normal software

| Normal feature | Agentic feature |
| --- | --- |
| "Can it do X?" has a clear no | "Can it do X?" is usually "sort of, sometimes" |
| Adding X means building X | Adding X means adding a sentence to a prompt — *apparently free* |
| Cost of X is estimable | Cost of X is a token multiplier nobody computes |
| X either works or does not | X works in the demo and fails on the long tail |

**The "just add it to the prompt" fallacy is the engine of agentic scope creep.** It looks like a
one-line change. It is a new capability with a new failure mode, a new evaluation slice, and a permanent
[instruction tax](token-tax-ledger.md).

## The fence: four posts

Agree these before the build, and hold them.

**Post 1 — The outcome fence.**
Every request must map to the one outcome in the [idea brief](../../docs/prd/00-idea-brief.md). Not "it's
related to travel". The specific outcome: *resolve refund enquiries without human handoff*.

**Post 2 — The evidence fence.**
Anything new needs golden-set cases before it needs prompt text. No cases, no capability. This converts
"just add it" into visible work.

**Post 3 — The blast-radius fence.**
No new capability may move a tool from green to amber on the
[Blast Radius Grid](blast-radius-grid.md) without a separate approval. Capability creep and
permission creep travel together; separate them.

**Post 4 — The cost fence.**
Every addition states its effect on cost per task. If it adds a turn, it multiplies
[four taxes](token-tax-ledger.md). "Negligible" needs a number.

## The intake question set

When a request arrives, four questions in order. Most requests stop at question 1 or 2.

1. **Which outcome does this serve?** *(If none: parking lot.)*
2. **What would prove it works?** *(If unanswerable: not ready, not rejected.)*
3. **What is the cost delta per task?** *(If it adds a turn, say so.)*
4. **Does it need a new tool or permission?** *(If yes: separate approval.)*

Note none of these is "no". A fence is not a wall — it converts vague enthusiasm into a specifiable
request, which is what you actually want.

## The parking lot, used properly

A parking lot only works if things come back out of it. Review it at each gate and sort into:

| Bucket | Meaning |
| --- | --- |
| **Next increment** | Serves the outcome; evidence definable; costed |
| **Needs a new outcome** | Real value, different product. Its own idea brief |
| **Declined** | With the reason recorded — so it does not return every month |

Recording the reason is what stops the same request cycling forever.

## The phrases, and what to say instead

| When you hear | Say |
| --- | --- |
| "Can't we just add it to the prompt?" | "What would prove it works? Let's write two test cases and see." |
| "The agent should be smart enough to…" | "Which outcome does that serve, and how would we measure it?" |
| "It already sort of does this" | "Sort of' means untested. Shall we test it properly and see?" |
| "Competitors have it" | "What outcome does it serve for *our* users? Let's brief it separately." |
| "It's only one more tool" | "That's a permission change. Different approval — let's do it properly." |

## Where this shows up

- [Module 00](../../modules/00-agentic-foundations/) — PRD builder and scoping
- [Module 15](../../modules/15-agentic-product-lifecycle/) — artefacts, gates, and the cost-cut ultimatum
- [Idea brief](../../docs/prd/00-idea-brief.md) — "what we are not building"

**Related:** [Autonomy Ladder](autonomy-ladder.md) · [Evidence Ladder](evidence-ladder.md) ·
[Value Trace](value-trace.md)
