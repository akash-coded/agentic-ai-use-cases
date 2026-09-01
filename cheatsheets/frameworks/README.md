# Frameworks and Mental Models

Seventeen original frameworks for reasoning about agentic systems. Each one is a **procedure with an
output** — a score, a number, a decision — not a concept to nod at. They were built from what actually
goes wrong on real agent projects.

Use them in design reviews, gate reviews, incident post-mortems, and when you inherit somebody else's
agent and need to work out what you are holding.

---

## By question you are trying to answer

### "Should this be an agent, and how autonomous?"

| Framework | Gives you |
| --- | --- |
| 🪜 **[The Autonomy Ladder](autonomy-ladder.md)** | Six rungs, a promotion test for each, and the rule: build the lowest rung that passes your acceptance test |
| 🚧 **[The Scope Fence](scope-fence.md)** | Four posts that stop "just add it to the prompt" scope creep |
| 💷 **[The Value Trace](value-trace.md)** | Five links from model metric to money — and where the trace usually breaks |

### "What will this cost?"

| Framework | Gives you |
| --- | --- |
| 🧾 **[The Token Tax Ledger](token-tax-ledger.md)** | Six taxes, four of them charged every turn, and the formula that exposes the real lever |
| ✖️ **[The Handoff Multiplier](handoff-multiplier.md)** | H× — one number for what a topology costs versus a single agent |
| 📉 **[The Cost Cliff Map](cost-cliff-map.md)** | Eight places cost goes non-linear, with the guard for each |
| ⏱️ **[The Three Clocks](three-clocks.md)** | Latency split into model, tool and orchestration — so you optimise the right one |
| 📐 **[The Context Budget Ledger](context-budget-ledger.md)** | Allocate the window like a budget, with an explicit overflow protocol |

### "Is it safe?"

| Framework | Gives you |
| --- | --- |
| 💥 **[The Blast Radius Grid](blast-radius-grid.md)** | Score every tool on reversibility × reach; keep them green by construction |
| ↩️ **[The Reversibility Test](reversibility-test.md)** | Four questions, five tiers, and the rehearsal that makes rollback real |
| 🔧 **[The Tool Surface Audit](tool-surface-audit.md)** | Six axes per tool — the schema is what the model sees, so it is what you audit |

### "Is it actually working?"

| Framework | Gives you |
| --- | --- |
| 📚 **[The Evidence Ladder](evidence-ladder.md)** | Six rungs of proof and the exact claim each licenses |
| 🔺 **[The Grounding Triangle](grounding-triangle.md)** | Retrieved ≠ cited ≠ verified, and the test for each |
| 🤷 **[The Abstention Budget](abstention-budget.md)** | Your correct "I don't know" rate, and why it is the vital sign |
| 🕳️ **[The Demo-to-Production Gap](demo-to-production-gap.md)** | Nine deltas between a demo and reality, as a pre-mortem |

### "Why is it broken?"

| Framework | Gives you |
| --- | --- |
| 🔍 **[The Failure Signature Catalog](failure-signature-catalog.md)** | Sixteen observable signatures → likely cause → confirm → fix |
| 🔇 **[The Silent Degradation Watchlist](silent-degradation-watchlist.md)** | Twelve things that get worse without raising an error, and the canary for each |

### "Is it ready to ship?"

| Framework | Gives you |
| --- | --- |
| ✅ **[The Agent Readiness Scorecard](agent-readiness-scorecard.md)** | Seven dimensions, 0–3 each — composes all of the above into one page |

---

## By role

| If you are a… | Start with |
| --- | --- |
| **Engineer** | [Autonomy Ladder](autonomy-ladder.md) → [Tool Surface Audit](tool-surface-audit.md) → [Failure Signature Catalog](failure-signature-catalog.md) |
| **Solutions architect** | [Autonomy Ladder](autonomy-ladder.md) → [Handoff Multiplier](handoff-multiplier.md) → [Blast Radius Grid](blast-radius-grid.md) → [Cost Cliff Map](cost-cliff-map.md) |
| **Product manager / PO** | [Scope Fence](scope-fence.md) → [Value Trace](value-trace.md) → [Evidence Ladder](evidence-ladder.md) → [Abstention Budget](abstention-budget.md) |
| **Business analyst** | [Value Trace](value-trace.md) → [Autonomy Ladder](autonomy-ladder.md) → [Demo-to-Production Gap](demo-to-production-gap.md) |
| **QA / test** | [Evidence Ladder](evidence-ladder.md) → [Abstention Budget](abstention-budget.md) → [Grounding Triangle](grounding-triangle.md) → [Failure Signature Catalog](failure-signature-catalog.md) |
| **Engineering manager** | [Agent Readiness Scorecard](agent-readiness-scorecard.md) → [Demo-to-Production Gap](demo-to-production-gap.md) → [Silent Degradation Watchlist](silent-degradation-watchlist.md) |
| **On-call** | [Failure Signature Catalog](failure-signature-catalog.md) → [Silent Degradation Watchlist](silent-degradation-watchlist.md) → [runbooks](../runbooks/) |

---

## The five ideas underneath all of them

1. **Autonomy is a cost, not a virtue.** Build the least autonomous thing that works.
2. **Every token has a payer.** Four of the six taxes are charged on every turn of every loop.
3. **Confident-wrong is the failure that ends projects.** Design abstention deliberately.
4. **A claim needs a rung.** State your evidence level with every number you quote.
5. **If the only guard is a sentence in a prompt, there is no guard.** Enforce in permissions and code.

---

[⬅️ Field guide](../) · [📚 Curriculum](../../modules/) · [🏛️ Architecture](../../docs/architecture/)
