# Observability for Agents — Cheat Sheet

Error rate is the one failure that is already loud. Everything that will actually hurt you is silent.

---

## The three vital signs

If you instrument nothing else:

| Signal | One line of code | Catches |
| --- | --- | --- |
| **Which model answered** | `log(model=result.model_id)` | Silent failover to a weaker or pricier model |
| **Abstention rate, daily** | `log(decision="abstain"\|"answer")` | Retrieval decay, tool failures, prompt drift |
| **Cost per task, daily** | `log(tokens_in, tokens_out, turns)` | Seven of eight [cost cliffs](../frameworks/cost-cliff-map.md) |

> **Abstention rate is the vital sign.** It moves before accuracy does, it is nearly free, and both
> directions are informative: rising means retrieval or tools are degrading; falling means the agent got
> bolder, not better.

## What to log per turn

```python
log.info("agent_turn", extra={
    "trace_id": trace_id,          # ties the whole task together
    "task_id": task_id,
    "turn": n,
    "model_id": model_id,          # vital sign 1
    "tokens_in": usage["inputTokens"],
    "tokens_out": usage["outputTokens"],
    "tool": tool_name,             # None if no tool this turn
    "tool_ms": tool_ms,            # three clocks
    "model_ms": model_ms,
    "tool_result_empty": is_empty, # catches the silent-empty failure
    "stop_reason": stop_reason,
    "decision": decision,          # answer | abstain | refuse
    "citations": len(citations),   # 0 on a factual claim is a defect
})
```

Ten fields. They answer almost every question in the
[Failure Signature Catalog](../frameworks/failure-signature-catalog.md).

## CloudWatch Logs Insights queries

**Turns per task — the cost multiplier:**
```
fields @timestamp, task_id, turn
| stats max(turn) as turns by task_id
| stats avg(turns), pct(turns, 95) as p95_turns
```

**Fallback model share:**
```
fields model_id
| stats count() as calls by model_id
| sort calls desc
```

**Abstention rate by day:**
```
fields @timestamp, decision
| filter ispresent(decision)
| stats sum(decision="abstain") * 100 / count() as abstain_pct by bin(1d)
```

**Uncited factual answers — a defect, not a metric:**
```
fields task_id, citations, decision
| filter decision = "answer" and citations = 0
| stats count() by bin(1h)
```

**Empty tool results:**
```
fields tool, tool_result_empty
| filter tool_result_empty = 1
| stats count() as empties by tool
| sort empties desc
```

**Cost per task:**
```
fields task_id, tokens_in, tokens_out
| stats sum(tokens_in) as tin, sum(tokens_out) as tout by task_id
| stats avg(tin * 0.000003 + tout * 0.000015) as avg_cost_usd
```
*(substitute your model's rates)*

**The three clocks split:**
```
fields model_ms, tool_ms
| stats sum(model_ms) as model, sum(tool_ms) as tool by task_id
| stats avg(model), avg(tool)
```

## Alerts that earn their noise

| Alert | Threshold | Why |
| --- | --- | --- |
| Fallback model share | > 5% | Silent degradation |
| Abstention rate change | ±30% week on week | The vital sign moved |
| Cost per task | > 20% over baseline | A cliff |
| p95 turns per task | > baseline + 1 | Loop or retry problem |
| Uncited factual answers | > 0 | Grounding broke |
| p99 input tokens | > 85% of window | Truncation is imminent |

Six alerts. Each has an owner, or it is not an alert — it is a dashboard nobody opens.

## Tracing

Return the trace id **to the caller**. Without it, a user report ("it gave me a wrong answer this morning")
is unactionable.

```python
return {"answer": text, "trace_id": trace_id, "model": model_id}
```

AgentCore Observability emits traces per run; correlate on your own `trace_id` so the trail survives
across tools and sub-agents.

## The weekly five-minute check

| Check | Healthy |
| --- | --- |
| Fallback model share | < 5% |
| Abstention rate vs last week | within ±30% |
| Newest indexed doc | < 2× sync interval |
| Cost per resolved task | within 20% of baseline |
| Newest golden-set case | < 60 days |

**Related:** [Silent Degradation Watchlist](../frameworks/silent-degradation-watchlist.md) ·
[Three Clocks](../frameworks/three-clocks.md) ·
[CloudWatch filters](../../modules/13-agentic-qa-and-evaluation/src/cloudwatch_filters.md)
