# Runbook · Latency has regressed

**Severity:** medium — usually degrades experience before it breaks anything.
**First action:** split the total into [three clocks](../frameworks/three-clocks.md). Optimising the wrong
one is the default failure of this incident.

---

## 0. Split it (5 minutes)

```
fields task_id, model_ms, tool_ms
| stats sum(model_ms) as model, sum(tool_ms) as tool, max(turn) as turns by task_id
| stats avg(model) as model_avg, avg(tool) as tool_avg, avg(turns) as turns_avg by bin(1h)
```

| Dominant clock | Go to |
| --- | --- |
| Turns rose | Step 1 — orchestration |
| Model ms per call rose | Step 2 |
| Tool ms rose | Step 3 |
| All flat, total up | Step 4 — the invisible one |

## 1. Orchestration — turns per task rose

The biggest lever, because turns multiply everything.

| Cause | Fix |
| --- | --- |
| Retries from a flaky tool | Fix the tool; cap retries |
| Loop not converging | Check the tool actually answers the question asked |
| Topology changed | Each handoff is a round trip — [H×](../frameworks/handoff-multiplier.md) |
| Routing regressed | Known paths now going through the agent instead of a workflow |

## 2. Model clock

| Cause | Check | Fix |
| --- | --- | --- |
| Output tokens grew | avg `tokens_out` | Cap `maxTokens`; check the prompt diff |
| Input tokens grew | avg `tokens_in` | Cap history; cap retrieval |
| Failover to a slower model | `stats count() by model_id` | Find the throttling cause |
| Regional capacity pressure | Throttling rate | Cross-Region inference profile |

## 3. Tool clock

```
fields tool, tool_ms | stats avg(tool_ms) as avg_ms, pct(tool_ms,95) as p95 by tool | sort p95 desc
```

| Cause | Fix |
| --- | --- |
| One downstream system slow | Their problem — but your timeout |
| Tools called serially | **Parallelise independent calls** — usually the biggest single win |
| No timeouts | Add them; a hanging tool hangs the whole task |
| Cache removed or cold | Restore caching for idempotent reads |

The parallelism fix:

```python
# serial:   t = a + b + c
# parallel: t = max(a, b, c)
results = await asyncio.gather(*(run(tc) for tc in tool_calls))
```

## 4. All clocks flat, total still up

Look outside the agent:

- Cold starts — is the runtime scaling from zero?
- Queueing — is p95 rising while p50 is flat? That is a concurrency limit
- Network or gateway overhead
- Client-side rendering, if the "latency" is a user report

> p50 flat with p95 rising is almost always queueing, not model slowness.

## 5. Consider perceived latency

If total latency cannot be reduced quickly, reduce *felt* latency:

| Technique | Effect |
| --- | --- |
| Stream the response | Time-to-first-token drops dramatically |
| Show tool progress ("checking booking…") | Waiting feels shorter and more legible |
| Answer partially, refine after | Works when the first fact is the useful one |

A system with 0.4 s to first token and 8 s total feels faster than one with 4 s and 6 s. That is a real
trade, not a trick.

## 6. Before you close it

- [ ] Per-clock budgets set, not just a total — so the next regression is attributable
- [ ] p95 latency in the [quality gate](../../modules/13-agentic-qa-and-evaluation/src/quality_gate.py)
- [ ] Timeouts on every tool
- [ ] Independent tool calls parallelised

## The post-mortem question

> **Did we know which clock it was within ten minutes?**

If not, the per-clock instrumentation is the gap.
