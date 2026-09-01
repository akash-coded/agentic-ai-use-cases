# How to · Price an agent feature before you build it

**Time:** 1 hour. **You need:** an estimate of turns per task and tokens per turn. Both are guessable to
within 2×, which is enough.

---

## 1. The formula

```
cost_per_task = calls_per_task × input_tokens_per_call  × input_rate
              + calls_per_task × output_tokens_per_call × output_rate
```

`calls_per_task` is the term people forget, and it is the one that multiplies everything.

## 2. Estimate the inputs

| Term | How to estimate | Typical |
| --- | --- | --- |
| `calls_per_task` | 1 per tool call + 1 for the final answer + 1 per handoff | 3–8 |
| `input_tokens_per_call` | system + tool schemas + history + retrieval | 2k–15k |
| `output_tokens_per_call` | reasoning + answer | 200–1,500 |

Remember that system prompt and tool schemas are charged on **every** call — see
[Token Tax Ledger](../../frameworks/token-tax-ledger.md).

## 3. Worked example

```
System prompt          400 tokens
Tool schemas (4)     1,200
History (avg)        1,500
Retrieval (5 × 400)  2,000
                    ------
Input per call       5,100
Calls per task           4
Input total         20,400 tokens

Output per call        600
Calls per task           4
Output total         2,400 tokens

At $3/M input, $15/M output:
  input   20,400 / 1M × $3   = $0.061
  output   2,400 / 1M × $15  = $0.036
  ─────────────────────────────────────
  cost per task              ≈ $0.097
```

## 4. The number that actually matters

```
cost_per_RESOLVED_task = cost_per_task ÷ autonomous_resolution_rate
```

At 60% resolution, $0.097 per task is **$0.16 per resolved task**. That is the number to compare against
the human cost, and it is the one people forget to divide.

## 5. Sensitivity — where the risk is

Vary each term by ±50% and see what moves:

| Term | −50% | +50% | Sensitivity |
| --- | --- | --- | --- |
| Calls per task | $0.049 | $0.146 | **Highest** |
| Retrieval tokens | $0.079 | $0.115 | High |
| Output tokens | $0.079 | $0.115 | High |
| System prompt | $0.093 | $0.101 | Low |

This tells you where to spend engineering effort — and it is almost never the system prompt, which is
where teams instinctively start.

## 6. Add the costs that are not inference

| Cost | Notes |
| --- | --- |
| Retrieval infrastructure | OpenSearch bills for **existing** |
| Runtime | Same |
| Memory storage | Grows with retention |
| Evaluation | Continuous sampling has a real cost |
| Human review | For any amber-zone action |

## 7. Check for cliffs

Cost is not linear. Ask which of the eight [cost cliffs](../../frameworks/cost-cliff-map.md) apply, and
what guards each. A retry storm or an uncapped loop turns your $0.10 into $0.50 without any traffic change.

## 8. Present it

| | |
| --- | --- |
| Cost per task (modelled) | $0.097 |
| Expected resolution rate | 60% |
| **Cost per resolved task** | **$0.16** |
| At [volume]/day | $—/month |
| Human cost per resolved case | $— |
| Break-even resolution rate | —% |
| Biggest sensitivity | Calls per task |
| Cliffs and guards | [list] |

**The break-even resolution rate is the row a CFO will care about most.** It answers "what if it's worse
than you think" before it is asked.

**Related:** [Token Tax Ledger](../../frameworks/token-tax-ledger.md) ·
[Cost Cliff Map](../../frameworks/cost-cliff-map.md) · [Value Trace](../../frameworks/value-trace.md)
