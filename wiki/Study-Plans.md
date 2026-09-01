# Study Plans

The repo's [learning paths](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/docs/learning-paths) are organised **by role**. These are organised **by calendar** — the same material, arranged around a life that already has a job in it.

Pick the one whose time budget you can actually defend to yourself.

---

## 🌙 Four weeks, evenings · ~6 h/week

For a working engineer with an hour most evenings.

| Week | Evenings | Do | Ends with |
| --- | --- | --- | --- |
| **1** | Mon–Thu | [AWS setup](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/docs/setup/aws-account-setup.md) (night 1, then wait for access) · [Module 00](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/modules/00-agentic-foundations) · [PDL-01 lab](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/labs/catalog/product/PDL-01) | A classified use case of your own |
| **2** | Mon–Thu | [Module 02](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/modules/02-bedrock-essentials) — onboarding notebook, Converse masterclass, exercises 1–2 | A working tool-use round trip |
| **3** | Mon–Thu | [AGL-01 → AGL-02 → AGL-03](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/labs/PATHWAY.md) · then [Module 05](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/modules/05-agent-loop-no-framework-to-strands) | The loop, by hand, and then in Strands |
| **4** | Mon–Thu | [Module 06](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/modules/06-strands-foundations) · [TOOL-03 lab](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/labs/catalog/tools/TOOL-03) · your own agent | An agent in your domain |

> **Start setup on night one even though you will not use it until week two.** Model access approval is the only part with a queue.

---

## 🏃 One weekend · ~12 h

The [Weekend Sprint](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/docs/learning-paths/weekend-sprint.md), hour by hour. Do AWS setup the **week before** — a weekend spent waiting on model access is a wasted weekend.

| | Sat AM | Sat PM | Sun AM | Sun PM |
| --- | --- | --- | --- | --- |
| **3 h each** | Model answering: onboarding notebook, Converse masterclass | Tool use: refund agent, exercise 3 | The loop by hand, then Strands | Your own domain; capstone if energy remains |

---

## 📅 Twelve weeks, reading group · 90 min/week

For a team. One session a week, pre-work before, discussion during.

| Wk | Pre-work | Discuss |
| --- | --- | --- |
| 1 | [Module 00](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/modules/00-agentic-foundations) | Bring one candidate use case each. Classify them together |
| 2 | [Autonomy Ladder](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/cheatsheets/frameworks/autonomy-ladder.md), [Scope Fence](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/cheatsheets/frameworks/scope-fence.md) | Which rung does ours need? What would we cut? |
| 3 | [Module 02](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/modules/02-bedrock-essentials) | Everyone runs the Converse notebook beforehand |
| 4 | [Token Tax Ledger](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/cheatsheets/frameworks/token-tax-ledger.md) | Cost our use case. Argue about the assumptions |
| 5 | [Module 05](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/modules/05-agent-loop-no-framework-to-strands) + AGL labs | Everyone writes the loop by hand. No exceptions |
| 6 | [Module 06](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/modules/06-strands-foundations) | Design our tool catalogue together |
| 7 | [Module 07](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/modules/07-strands-multi-agent-patterns) + [Handoff Multiplier](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/cheatsheets/frameworks/handoff-multiplier.md) | Pick a topology and compute its H× |
| 8 | [Module 10](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/modules/10-rag-opensearch-litellm) core labs | Where would our corpus break retrieval? |
| 9 | [Grounding Triangle](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/cheatsheets/frameworks/grounding-triangle.md) | Read five of our own cited answers. Do the passages support them? |
| 10 | [Module 13](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/modules/13-agentic-qa-and-evaluation) | Draft our golden set. Include cases we fail |
| 11 | [Module 11](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/modules/11-bedrock-agentcore) | Who owns the corpus? Who is on call? |
| 12 | [Scorecard](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/cheatsheets/frameworks/agent-readiness-scorecard.md) | Score our system. Two people score independently and compare |

**The week-12 disagreement is the point.** Where two scorers differ is your actual agenda.

---

## 🚪 No AWS account yet · ~20 h, £0

Everything here runs offline. Genuinely useful while access is pending — or if you never enable it.

| | |
| --- | --- |
| [Module 00](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/modules/00-agentic-foundations) · [Module 01](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/modules/01-llm-and-aws-bridge) · [Module 15](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/modules/15-agentic-product-lifecycle) | ~13 h |
| **All 10 [L.A.B. labs](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/labs)** — every one is offline and stdlib-only | ~5 h |
| [`rag_by_hand.py`](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/modules/10-rag-opensearch-litellm/src/rag_by_hand.py) · [`quality_gate.py`](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/modules/13-agentic-qa-and-evaluation/src/quality_gate.py) | ~2 h |
| The whole [field guide](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/cheatsheets) | as long as you like |

---

## 🎯 Interview in two weeks

Ruthless. These four labs plus two guides answer more interview questions than the rest combined.

| Days | Do |
| --- | --- |
| 1–3 | [AGL-01, AGL-02, AGL-03](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/labs/PATHWAY.md) — be able to write the loop from memory |
| 4–5 | [EVAL-03](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/labs/catalog/evaluation/EVAL-03) — and read [`quality_gate.py`](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/modules/13-agentic-qa-and-evaluation/src/quality_gate.py) |
| 6–8 | Your [role's interview guide](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/cheatsheets/interviews) — prepare the three stories it asks for |
| 9–11 | [Autonomy Ladder](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/cheatsheets/frameworks/autonomy-ladder.md), [Evidence Ladder](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/cheatsheets/frameworks/evidence-ladder.md), [Failure Signature Catalog](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/cheatsheets/frameworks/failure-signature-catalog.md) |
| 12–14 | Build one small agent end to end. **Measure its cost per resolved task.** Bring the number |

**The four questions to be able to answer cold:** what does it do when it does not know · how do you know it works, and on what evidence rung · what did you decide *not* to build · what did you get wrong and what changed.

---

## Using these

Nobody finishes a plan exactly. The value is having a next action rather than a 16-module directory.

**Share yours.** If you invented a schedule that worked around your constraints, add it — this page is editable by anyone. Real plans from real people beat designed ones.
