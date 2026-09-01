# Cost Log

Real measured costs, contributed by people who ran the material. Not estimates.

> **Why this is a wiki page.** [`docs/setup/cost-controls.md`](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/docs/setup/cost-controls.md) is the *guidance* — where money goes, and the teardown checklist. It deliberately quotes no prices, because stale numbers are worse than none. This page is the *observed data*, with dates attached so you can judge how stale it is.

---

## The two things that dominate

Before any table: cost here is not mostly inference.

1. **Inference is cheap.** Cents per exercise, a few dollars per module.
2. **Idle infrastructure is not.** OpenSearch Serverless collections and AgentCore runtimes bill for **existing**, not for use. A collection created on Tuesday and forgotten is still charging on Friday.

Almost every "this cost far more than expected" report traces to #2, not #1. [Teardown checklist](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/docs/setup/cost-controls.md#teardown-checklist).

---

## Reported costs, by module

| Module | Reported | Torn down same day? | Region | Date | By |
| --- | --- | --- | --- | --- | --- |
| 02 Bedrock Essentials | — | — | — | — | — |
| 03 Bedrock Agents | — | — | — | — | — |
| 10 RAG / OpenSearch | — | — | — | — | — |
| 11 AgentCore | — | — | — | — | — |
| 14 End-to-end | — | — | — | — | — |

**Add a row after you finish a module.** The "torn down same day" column is the most informative one — the same module costs wildly different amounts depending on it.

---

## Full-curriculum reports

| Approach | Total | Period | Notes | By |
| --- | --- | --- | --- | --- |
| — | — | — | — | — |

Useful to state: whether you tore down as you went, which modules you skipped, and whether anything was left running by accident (that one is the most useful of all).

---

## £0 while you decide

Genuinely free, no account needed: Modules 00, 01 and 15, **every [L.A.B. lab](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/labs)**, `rag_by_hand.py`, `quality_gate.py`, and the whole [field guide](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/cheatsheets). Roughly 20 hours of real work.

---

## Before you start anything

- [ ] Budget alarm at 50/80/100%. It does not stop spending — it tells you
- [ ] A sandbox account, not production
- [ ] The teardown checklist somewhere you will actually see it
- [ ] Know that Modules 10, 11 and 14 create infrastructure that bills for existing

---

## Where costs go, and what controls them

| Driver | Controlled by | Depth |
| --- | --- | --- |
| Tokens per turn | Prompt and schema discipline | [Token Tax Ledger](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/cheatsheets/frameworks/token-tax-ledger.md) |
| Turns per task | Topology — every handoff re-sends context | [Handoff Multiplier](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/cheatsheets/frameworks/handoff-multiplier.md) |
| Non-linear jumps | Eight named cliffs | [Cost Cliff Map](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/cheatsheets/frameworks/cost-cliff-map.md) |
| Idle infrastructure | The teardown checklist | [Cost controls](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/docs/setup/cost-controls.md) |

**Turns per task is almost always the highest-sensitivity term.** It multiplies four of the six token taxes at once, which is why cost surprises are usually topology surprises.

---

## A note on honesty

If you got a surprise bill, please add it. A row saying *"left an OpenSearch collection up for three weeks, £—"* is more useful to the next person than every carefully-torn-down row on this page. No judgement — it is the most common mistake here and the whole reason the checklist exists.
