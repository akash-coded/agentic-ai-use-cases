# The Agent Readiness Scorecard

> **One line:** one page, seven dimensions, scored 0–3 — bring it to the gate review instead of an opinion.

This composes the other frameworks into a single instrument. Use it at a design review, a go/no-go, or when
inheriting someone else's agent.

---

## Scoring

**0** absent · **1** partial · **2** adequate · **3** strong. Anything at **0 or 1 blocks release**,
regardless of the total.

### 1. Fit — is this the right shape? *(→ [Autonomy Ladder](autonomy-ladder.md))*

| | Criterion |
| --- | --- |
| 0 | Nobody asked whether it should be an agent |
| 1 | It was assumed to be an agent |
| 2 | Classified deliberately; rung chosen |
| 3 | Built at the lowest rung passing the acceptance test; known paths routed away |

### 2. Grounding *(→ [Grounding Triangle](grounding-triangle.md))*

| | Criterion |
| --- | --- |
| 0 | Answers from parametric memory |
| 1 | Retrieves, but citations absent or unchecked |
| 2 | Cites; citations asserted by a contract test |
| 3 | Cited passages verified by sample or entailment |

### 3. Honesty *(→ [Abstention Budget](abstention-budget.md))*

| | Criterion |
| --- | --- |
| 0 | Always answers |
| 1 | Abstains occasionally, by accident |
| 2 | Abstention designed, with a target rate |
| 3 | Abstention measured, gated, with a resolution path |

### 4. Containment *(→ [Blast Radius Grid](blast-radius-grid.md))*

| | Criterion |
| --- | --- |
| 0 | Broad permissions; prompt is the only guard |
| 1 | Some scoping; red tools exist without guards |
| 2 | Tools scored; amber tools have human commit |
| 3 | All tools green by construction; enforced in IAM, not prose |

### 5. Evidence *(→ [Evidence Ladder](evidence-ladder.md))*

| | Criterion |
| --- | --- |
| 0 | Anecdote or demo (E1–E2) |
| 1 | Golden set built from cases it already passes |
| 2 | Honest golden set: real inputs, failing cases, abstention and adversarial slices (E4) |
| 3 | Shadow or production sampling, continuous (E5–E6) |

### 6. Observability *(→ [Silent Degradation Watchlist](silent-degradation-watchlist.md))*

| | Criterion |
| --- | --- |
| 0 | Errors only |
| 1 | Logging, no metrics |
| 2 | The three vital signs: answering model, abstention rate, cost per task |
| 3 | Vital signs plus alerts with owners |

### 7. Reversibility *(→ [Reversibility Test](reversibility-test.md))*

| | Criterion |
| --- | --- |
| 0 | No rollback path |
| 1 | Code rolls back; prompts and models do not |
| 2 | Versioned manifest covering code, prompt and model |
| 3 | Rollback rehearsed this cycle, and timed |

## The scorecard

| Dimension | Score | Evidence | Owner |
| --- | --- | --- | --- |
| Fit | /3 | | |
| Grounding | /3 | | |
| Honesty | /3 | | |
| Containment | /3 | | |
| Evidence | /3 | | |
| Observability | /3 | | |
| Reversibility | /3 | | |
| **Total** | **/21** | | |

## Reading the total

| Total | Meaning |
| --- | --- |
| 18–21 | Ready, assuming no dimension below 2 |
| 14–17 | Ready for shadow traffic, not for users |
| 10–13 | Prototype. Name the two weakest and fix them |
| < 10 | Not a production candidate — and that is a fine thing for it to be |

> **The total is the least useful number on this page.** A 19 with Containment at 1 is more dangerous than
> a flat 14, because the high total buys false confidence. Read the rows.

## Using it well

- Score it **twice**: the builder scores it, then someone who did not build it scores it. Compare. The
  disagreements are the agenda.
- Score it **before** the review, not during. The conversation should be about the gaps.
- Re-score after any model, prompt or corpus change — those invalidate the Evidence row immediately.

## Where this shows up

- [Module 15](../../modules/15-agentic-product-lifecycle/) — gate reviews
- [Production readiness PRD](../../docs/prd/05-production-readiness.md)
- [Design review playbook](../playbooks/agent-design-review.md)

**Related:** every framework in [this folder](./)
