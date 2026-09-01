# How-to · QA and Test

Testing non-deterministic systems is a different discipline, not the same discipline applied harder.

| How-to | Time | Catches |
| --- | --- | --- |
| 🔌 **[Test tool failure honesty](test-tool-failure-honesty.md)** | 2 h | The agent inventing an answer around an empty tool result |
| ⚖️ **[Validate an LLM judge](validate-an-llm-judge.md)** | half day | Every number downstream inheriting an uncalibrated instrument |

Also directly relevant: **[Build a quality gate that actually blocks](../engineers/build-a-quality-gate.md)**
and **[Build a golden set from real tickets](../business-analysts/build-a-golden-set.md)**.

## The three things to internalise

1. **You test properties and rates, not outputs.** Contract tests for shape, invariance across paraphrases,
   rate-based assertions on a named set.
2. **A gate that warns is not a gate.** Exit non-zero, or you have built a report.
3. **"Wrong" and "correctly declined" are different results.** A suite that cannot tell them apart cannot
   measure the thing that matters.

## Your frameworks

[Evidence Ladder](../../frameworks/evidence-ladder.md) ·
[Abstention Budget](../../frameworks/abstention-budget.md) ·
[Grounding Triangle](../../frameworks/grounding-triangle.md) ·
[Failure Signature Catalog](../../frameworks/failure-signature-catalog.md)

## Where to start

[Module 13](../../../modules/13-agentic-qa-and-evaluation/) — especially
[`quality_gate.py`](../../../modules/13-agentic-qa-and-evaluation/src/quality_gate.py). It is short, and it
is the file that decides whether a build ships.

---

[⬅️ All how-tos](../) · [💼 QA interview guide](../../interviews/qa-engineer.md)
