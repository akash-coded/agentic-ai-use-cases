# The Three Clocks

> **One line:** agent latency is three separate clocks, and optimising the wrong one is the default.

"The agent is slow" is not actionable. Decompose it into three clocks and the bottleneck names itself.

---

## The clocks

| Clock | What it measures | Typical share | You control it by |
| --- | --- | --- | --- |
| ⏱️ **Model clock** | Time inside model inference | 40–70% | Model choice, output length, streaming |
| 🔧 **Tool clock** | Time in your tools and their downstream systems | 20–50% | Parallelism, caching, timeouts |
| 🔁 **Orchestration clock** | Turns × round-trips + framework overhead | 10–30% | Fewer turns, better routing |

```
total ≈ Σ(model calls × model latency)
      + Σ(tool calls × tool latency)
      + orchestration overhead
```

The multiplier is `turns`. It sits in front of two of the three clocks, which is why turn count is almost
always the highest-leverage lever — and almost never the first one people reach for.

## Measuring the split

Instrument once, at the boundary of each:

```python
t0 = perf_counter()
resp = converse(...)                 # model clock
t1 = perf_counter()
result = dispatch(tool_call)         # tool clock
t2 = perf_counter()
log(model_ms=(t1-t0)*1000, tool_ms=(t2-t1)*1000, tool=tool_call.name, turn=n)
```

Then sum per task and take the split. Do this before optimising anything.

## The optimisation order

| If the split says | Do this | Not this |
| --- | --- | --- |
| Model clock dominates | Cap `maxTokens`; stream first token; try a faster model on easy routes | Rewriting tools |
| Tool clock dominates | Parallelise independent tools; cache; set aggressive timeouts | Changing models |
| Orchestration dominates | Cut turns — route known paths away from the agent | Micro-optimising anything |

## The parallelism win most teams miss

When the model requests several independent tools in one turn, dispatch them concurrently:

```python
# serial:   t = a + b + c
# parallel: t = max(a, b, c)
results = await asyncio.gather(*(run(tc) for tc in tool_calls))
```

On a three-tool turn this is often the largest single latency win available, and it changes no behaviour
at all.

## Perceived vs actual latency

Users experience time-to-first-token, not total time. Two systems with identical totals feel completely
different:

| | Time to first token | Total | Feels |
| --- | --- | --- | --- |
| A | 4.0 s | 6 s | Slow |
| B | 0.4 s | 8 s | Fast |

Stream. Show the tool being called ("checking booking…"). Perceived latency is a design problem as much as
an engineering one — and B is a legitimate trade if your p95 budget allows it.

## The budget

Set it per clock, not just in total, so a regression is attributable:

| Clock | Budget (p95) | Alert |
| --- | --- | --- |
| Model | | > 20% over baseline |
| Tool | | any tool > its own timeout ×0.8 |
| Orchestration | | turns per task > baseline + 1 |
| **Total** | | > agreed p95 |

A total-only budget tells you that something regressed. A per-clock budget tells you what.

## Where this shows up

- [Module 13](../../modules/13-agentic-qa-and-evaluation/) — cost and latency in the gate
- [Module 07](../../modules/07-strands-multi-agent-patterns/) — topology drives the orchestration clock
- [Latency regression runbook](../runbooks/incident-latency-regression.md)

**Related:** [Handoff Multiplier](handoff-multiplier.md) · [Cost Cliff Map](cost-cliff-map.md)
