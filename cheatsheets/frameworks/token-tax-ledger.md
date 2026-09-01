# The Token Tax Ledger

> **One line:** every token has a payer and a reason — and four of the six taxes are charged on *every turn*.

Teams estimate cost by counting the user's question and the agent's answer. That is the small part.
This ledger accounts for the rest.

---

## The six taxes

| # | Tax | What it is | Charged | Typical share |
| --- | --- | --- | --- | --- |
| 1 | **Instruction tax** | System prompt, persona, rules | **Every turn** | 5–25% |
| 2 | **Schema tax** | Tool definitions sent with every request | **Every turn** | 10–40% |
| 3 | **History tax** | Prior conversation turns | **Every turn**, growing | 10–50% |
| 4 | **Retrieval tax** | Passages injected into context | **Every grounded turn** | 15–60% |
| 5 | **Reasoning tax** | Tokens the model produces to think | Per turn | 5–30% |
| 6 | **Format tax** | JSON scaffolding, markdown, boilerplate | Per turn | 2–10% |

> **The compounding insight:** taxes 1–3 are paid on *every model call in the loop*. An agent that makes
> six calls to answer one question pays the instruction and schema tax six times. Your 400-token system
> prompt is a 2,400-token line item.

## The formula

```
cost_per_task = calls_per_task
              × (instruction + schema + history + retrieval) × input_rate
              + (reasoning + answer + format)                × output_rate
```

Note what this exposes: **reducing `calls_per_task` cuts four taxes at once.** Shortening the system prompt
cuts one. Teams usually do the second and wonder why the bill barely moved.

## Where the money actually is

| If your bill is high, check in this order | Because |
| --- | --- |
| 1. `calls_per_task` | It multiplies four taxes simultaneously |
| 2. Retrieval tax | Top-k and chunk size are usually set by habit, not measurement |
| 3. Schema tax | Ten tools you never prune cost you on every single turn |
| 4. History tax | Unbounded buffers grow until they overflow or bankrupt you |
| 5. Instruction tax | Real, but the smallest lever of the five |

## The audit

Run one representative task and fill this in. Estimates do not count — read the `usage` block.

| Tax | Tokens/turn | × turns | Total | % |
| --- | --- | --- | --- | --- |
| Instruction | | | | |
| Schema | | | | |
| History | | | | |
| Retrieval | | | | |
| Reasoning | | | | |
| Answer + format | | | | |
| **Total** | | | | 100% |

Anything above 40% in a single row is your optimisation target. Anything below 10% is not worth your time.

## Three cuts that usually work

1. **Prune the tool menu per route.** An agent handling refunds does not need the rebooking tools in
   context. Route first, then attach only the relevant schemas.
2. **Cap retrieval, then measure.** Going from top-10 to top-5 often costs nothing in quality and halves
   the largest tax. Prove it on the golden set.
3. **Summarise history at a threshold, not every turn.** Summarising costs a call; do it when the buffer
   crosses a bound, not on a schedule.

## Where this shows up

- [Module 00 · token-cost calculator](../../modules/00-agentic-foundations/activities/H2-03_Token-Cost_Calculator.xlsx)
- [Module 03 · the verbosity tax exercise](../../modules/03-bedrock-agents/exercises/verbosity_tax_exercise.md)
- [Module 10 · tokens and cost lab](../../modules/10-rag-opensearch-litellm/labs/rag-labs/07_tokens_cost.ipynb)

**Related:** [Handoff Multiplier](handoff-multiplier.md) · [Context Budget Ledger](context-budget-ledger.md) ·
[Cost Cliff Map](cost-cliff-map.md)
