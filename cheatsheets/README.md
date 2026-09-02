<div align="center">

# 🗺️ The Agentic AI Field Guide

### Frameworks, cheat sheets, runbooks, playbooks and role-based how-tos

**Everything that is not a lesson.** The [curriculum](../modules/) teaches you to build agents. This is
what you reach for once you are building them — in a design review, at 2 a.m. during an incident, in a
budget meeting, or in an interview.

**17 frameworks · 10 quick references · 9 runbooks · 4 playbooks · 6 interview guides · 17 how-tos**

</div>

---

## The five sections

| Section | What it is | Open it when |
| --- | --- | --- |
| 🧠 **[Frameworks](frameworks/)** | 17 original mental models, each with a procedure and an output | You are making a decision and want a defensible basis |
| 📖 **[Quick reference](quick-reference/)** | Syntax, APIs and the mistakes each causes | You are building and need the shape of something |
| 🚨 **[Runbooks](runbooks/)** | Incident and operational procedures | Something is broken, right now |
| 📋 **[Playbooks](playbooks/)** | Reviews, build-vs-buy, scoping, stopping | You have a decision meeting |
| 💼 **[Interviews](interviews/)** | Five roles, both sides of the table | You are hiring, or being hired |
| 🎓 **[How-to by role](how-to/)** | Practical recipes for six roles | You have a specific job to do |

---

## Copy-paste

Four runnable gists, each one file, each a framework reduced to the code you would actually paste:

| Gist | What it is | From |
| --- | --- | --- |
| [`agent_history_invariant.py`](https://gist.github.com/akash-coded/12cd36b5e5ced3e0c5414af3abffa221) | Two lines that catch the most common agent-loop bug at the cause | [Failure Signature Catalog](frameworks/failure-signature-catalog.md) |
| [`honest_tool_result.py`](https://gist.github.com/akash-coded/e3748d8f0accfedf0a2509ee16195d51) | A tool return the model cannot misread — and a router that proves it | [Tool Surface Audit](frameworks/tool-surface-audit.md) |
| [`release_gate.py`](https://gist.github.com/akash-coded/908a2f096a89de29d3b3221244773a1b) | A 40-line gate that exits non-zero, puts safety first, and never raises | [Build a quality gate](how-to/engineers/build-a-quality-gate.md) |
| [`handoff_multiplier.py`](https://gist.github.com/akash-coded/407c5e9ddcca84afe7099439591d3ec2) | H× with the merge call everyone forgets, for common shapes | [Handoff Multiplier](frameworks/handoff-multiplier.md) |

---

## Start here, by role

| You are a… | Read these three first |
| --- | --- |
| **Engineer** | [Autonomy Ladder](frameworks/autonomy-ladder.md) · [Failure Signature Catalog](frameworks/failure-signature-catalog.md) · [Add a tool properly](how-to/engineers/add-a-tool-properly.md) |
| **Solutions architect** | [Handoff Multiplier](frameworks/handoff-multiplier.md) · [Blast Radius Grid](frameworks/blast-radius-grid.md) · [Cost Cliff Map](frameworks/cost-cliff-map.md) |
| **Product manager / PO** | [Scope Fence](frameworks/scope-fence.md) · [Value Trace](frameworks/value-trace.md) · [Write acceptance criteria](how-to/product/write-acceptance-criteria.md) |
| **Business analyst** | [Value Trace](frameworks/value-trace.md) · [Build a golden set](how-to/business-analysts/build-a-golden-set.md) · [Abstention Budget](frameworks/abstention-budget.md) |
| **QA / test** | [Evidence Ladder](frameworks/evidence-ladder.md) · [Grounding Triangle](frameworks/grounding-triangle.md) · [Validate an LLM judge](how-to/qa-and-test/validate-an-llm-judge.md) |
| **Engineering manager** | [Agent Readiness Scorecard](frameworks/agent-readiness-scorecard.md) · [Staff an agent team](how-to/engineering-managers/staff-an-agent-team.md) · [Set up on-call](how-to/engineering-managers/set-up-on-call.md) |
| **On-call, right now** | [Runbook triage table](runbooks/#the-triage-table) |

---

## The ideas that run through all of it

**1. Autonomy is a cost, not a virtue.**
Build the lowest rung that passes your acceptance test. Most projects build a planner where a loop with a
tool menu would have worked. → [Autonomy Ladder](frameworks/autonomy-ladder.md)

**2. Four of the six token taxes are charged on every turn.**
Which is why turn count — not prompt length — is the lever that moves your bill.
→ [Token Tax Ledger](frameworks/token-tax-ledger.md)

**3. Confident-wrong is the failure that ends projects.**
An agent that never says "I don't know" is not confident. Abstention is a designed rate.
→ [Abstention Budget](frameworks/abstention-budget.md)

**4. A claim needs a rung.**
"It works" is not a claim. "87% on a 130-case golden set, 20 of which are abstention cases" is.
→ [Evidence Ladder](frameworks/evidence-ladder.md)

**5. If the only guard is a sentence in a prompt, there is no guard.**
An agent cannot issue a refund if it does not have a refund tool. Enforce in permissions, not prose.
→ [Blast Radius Grid](frameworks/blast-radius-grid.md)

---

## The four questions worth memorising

They work in a design review, a vendor evaluation, an interview and an incident:

1. **"What does it do when it doesn't know?"**
2. **"How do you know it works — what rung is that evidence on?"**
3. **"What's the H× of this topology, measured?"**
4. **"If the only guard is a sentence in the prompt, what happens when someone edits that sentence?"**

---

## How this relates to the curriculum

The [16 modules](../modules/) are where you **learn** by building. This field guide is the **reference
layer** on top: distilled, cross-linked, and written to be opened at the moment you need it rather than
read front to back.

Every page links back to the module that teaches the underlying skill, and to the
[LLD](../docs/architecture/lld/) that explains the mechanism.

---

<div align="center">

[🏠 Repository](../) · [📚 Curriculum](../modules/) · [🗺️ Learning paths](../docs/learning-paths/) ·
[🏛️ Architecture](../docs/architecture/) · [💬 Discussions](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions)

</div>
