# The Evidence Ladder

> **One line:** never make a claim above the rung your evidence sits on.

"It works" is a claim. The question is always: how do you know? This ladder gives six rungs of evidence
and the exact claim each one licenses. It is the fastest way to end a circular argument in a design review.

---

| Rung | Evidence | Claim it licenses | Cost | Fools you when |
| --- | --- | --- | --- | --- |
| **E0** | Vibes — "it felt good" | None | 0 | Always |
| **E1** | Anecdote — it worked on my example | "It can do this once" | 0 | Your example was easy |
| **E2** | Demo — a rehearsed run | "It can do this reliably *for these inputs*" | Low | Inputs were chosen |
| **E3** | Benchmark — a public dataset | "It performs like the benchmark's distribution" | Low | Your data differs from the benchmark |
| **E4** | Golden set — your data, your labels | "It performs at X% on inputs like ours" | Medium | The set was built from cases you pass |
| **E5** | Shadow traffic — real inputs, no user impact | "It performs at X% on real traffic" | Medium-high | Behaviour differs when it's live |
| **E6** | Production sample — live, sampled, reviewed | "It performs at X% in production" | Ongoing | Sampling is biased |

## The rule

> **State the rung with the claim.** "92% on our 130-case golden set (E4)" is a sentence nobody can
> misread. "It's about 92% accurate" is a sentence that will be quoted back at you in an incident review.

## The escalation each rung demands

| Going from | Requires |
| --- | --- |
| E1 → E2 | Write the script; run it in front of someone |
| E2 → E3 | Find a benchmark whose distribution resembles yours (usually none does — this is why E3 is weak for agents) |
| E3 → E4 | **Build the golden set.** The highest-value step on the ladder |
| E4 → E5 | Route real traffic to the agent without showing users the output |
| E5 → E6 | Ship, sample, review continuously |

**E3 is usually a detour for agent work.** Public benchmarks measure model capability, not your system's
behaviour on your data with your tools. Skip from E2 to E4.

## The golden-set trap

E4 is the rung most often faked. A golden set built by running your agent and labelling what it got right
is not evidence — it is a mirror.

A valid golden set:
- Is drawn from **real inputs**, sampled, not invented
- Includes cases the agent **currently fails**
- Includes an **abstention slice** (correct answer: "I don't know")
- Includes an **adversarial slice**
- Was **frozen before** the tuning it is used to evaluate

If your set has none of these properties, you are at E2 with more spreadsheets.

## Using it in a review

When someone claims a system is ready, ask one question:

> "What rung is that on?"

If the answer is E2 and the decision is a production release, the conversation is now about the gap rather
than about opinions. This question has saved more projects than any architecture diagram.

## The claims register

Keep this next to your PRD. One row per claim anyone has made about the system.

| Claim | Made by | Rung | Evidence link | Expires |
| --- | --- | --- | --- | --- |
| "Resolves 60% autonomously" | | E4 | golden-set run #— | on next model change |
| | | | | |

Claims expire. A model change, a prompt change or a corpus change invalidates every rung above E1.

## Where this shows up

- [Module 13](../../modules/13-agentic-qa-and-evaluation/) — building an honest golden set
- [Evaluation plan PRD](../../docs/prd/04-evaluation-plan.md) — 130 cases, 50 of which were failing at freeze
- [Module 10 · evaluation gate](../../modules/10-rag-opensearch-litellm/labs/rag-labs/06_evaluation_gate.ipynb)

**Related:** [Demo-to-Production Gap](demo-to-production-gap.md) · [Abstention Budget](abstention-budget.md) ·
[Grounding Triangle](grounding-triangle.md)
