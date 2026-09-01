# How to · Size and cost an agent deployment

**Time:** 2 hours. **Output:** a cost model with a named sensitivity and a break-even point.

---

## 1. The four cost drivers

| Driver | Scales with | Controlled by |
| --- | --- | --- |
| Inference | calls × tokens | Turn count, retrieval size, prompt length |
| Retrieval infra | corpus size, **and existing** | Right-sizing, teardown |
| Runtime | deployed time, **not usage** | Teardown, scale-to-zero if available |
| Memory | sessions × retention | **TTL** |

Two of the four bill for **existing**. That is the thing that surprises people.

## 2. Inference — model it

```
cost_per_task = calls × (input_tokens × input_rate + output_tokens × output_rate)
```

Estimate from the [Token Tax Ledger](../../frameworks/token-tax-ledger.md): instruction + schema + history
+ retrieval on the input side. Then divide by resolution rate for
**cost per resolved task** — the only number worth quoting.

## 3. Infrastructure — the fixed drain

| Component | Bills for |
| --- | --- |
| OpenSearch Serverless | Provisioned capacity, continuously |
| AgentCore Runtime | Deployed time |
| AgentCore Memory | Stored volume × retention |
| Knowledge Base + vectors | Storage |
| Lambda | Invocations (negligible at most scales) |

Model these as a **monthly floor** independent of traffic. A pilot with 50 requests a day can be dominated
entirely by this floor, which makes per-request cost look absurd — and makes the pilot look worse than the
production case.

## 4. Capacity

| Question | Determines |
| --- | --- |
| Peak requests per minute | Throttling risk; whether you need a cross-Region profile |
| Concurrency | Runtime sizing |
| p95 latency budget | Model choice, parallelism |
| Burst shape | Whether scale-to-zero is viable |

Load test at 3× expected peak. [Delta 2](../../frameworks/demo-to-production-gap.md) — concurrency — is
where demos and production diverge most sharply.

## 5. The sensitivity table

Vary each ±50%. Present this, not a single number:

| Driver | −50% | Base | +50% |
| --- | --- | --- | --- |
| Calls per task | | | |
| Retrieval tokens | | | |
| Resolution rate | | | |
| Volume | | | |

Calls per task is almost always the highest sensitivity, which tells you where engineering effort belongs.

## 6. The break-even

```
break_even_resolution_rate = (cost_per_task × volume) ÷ (human_cost_per_case × volume)
```

Answer "what if it's worse than you think" **before** it is asked. It is the single most credible number
you can bring to a finance conversation.

## 7. Cliffs and guards

For each of the eight [cost cliffs](../../frameworks/cost-cliff-map.md): can it happen here, what guards
it, and **who notices**. The last column is the one usually left blank, and a guard nobody owns is not a
guard.

## 8. The one-page model

| | |
| --- | --- |
| Cost per task (modelled / measured) | |
| Resolution rate (assumed / measured) | |
| **Cost per resolved task** | |
| Monthly infra floor | |
| At [volume] | $—/month |
| Human baseline per case | |
| **Break-even resolution rate** | |
| Highest sensitivity | |
| Cliffs without guards | |

Workbooks:
[Token cost](../../../modules/00-agentic-foundations/activities/H2-03_Token-Cost_Calculator.xlsx) ·
[Bedrock estimator](../../../modules/06-strands-foundations/activities/Bedrock_Cost_Estimator.xlsx) ·
[AgentCore capacity](../../../modules/11-bedrock-agentcore/activities/AgentCore_Cost_and_Capacity_Workbench.xlsx)

**Related:** [Cost Cliff Map](../../frameworks/cost-cliff-map.md) ·
[Three Clocks](../../frameworks/three-clocks.md)
