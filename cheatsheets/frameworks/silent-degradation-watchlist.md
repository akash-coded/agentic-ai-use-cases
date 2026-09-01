# The Silent Degradation Watchlist

> **One line:** the failures that will hurt you most are the ones that do not raise an error.

An exception wakes someone up. Silent degradation ships to customers for six weeks. This is the list of
things that get quietly worse, and the signal that catches each one.

---

## The watchlist

| # | Degradation | Why it is silent | Canary signal | Alert on |
| --- | --- | --- | --- | --- |
| 1 | **Model failover to a weaker model** | Fallback works; quality drops | Log the answering model per response | Fallback share > 5% |
| 2 | **Index drifting stale** | Retrieval still returns passages | Age of newest indexed doc | Age > sync interval × 2 |
| 3 | **Abstention rate falling** | Looks like improvement | Daily abstention rate | Change > ±30% week on week |
| 4 | **Citations becoming decorative** | Citations still present | Entailment sample score | Sample pass rate < 90% |
| 5 | **Context silently truncated** | No error; oldest turns vanish | Input tokens vs window limit | p99 > 85% of window |
| 6 | **Retrieval recall decaying as corpus grows** | Same top-k, more competition | Golden-set recall@k, weekly | Any drop |
| 7 | **Tool returning defaults instead of data** | `{}` or `null` treated as an answer | Rate of empty tool results | > 2% of calls |
| 8 | **Prompt edited without version bump** | Nothing errors | Prompt hash in the manifest | Hash change without version change |
| 9 | **Cost creeping per task** | Each request looks normal | Cost per resolved task, daily | > 20% above baseline |
| 10 | **Latency creeping** | Under timeout, so no error | p95 latency, daily | > 20% above baseline |
| 11 | **Guardrail rules drifting out of date** | Guardrail still passes | Guardrail intervention rate | Sudden drop |
| 12 | **Golden set going stale** | It still passes | Age of newest case | No new case in 60 days |

## The three-signal minimum

If you instrument nothing else, instrument these. They catch most of the list:

1. **Which model answered** — catches #1, and is one log line
2. **Abstention rate, daily** — catches #3, #7, #11, and is the single best health signal for an agent
3. **Cost per resolved task, daily** — catches #9, and #1 in reverse (a *cheaper* week may mean fallback)

> **Abstention rate is the vital sign.** It moves before accuracy does, it is cheap to compute, and both
> directions are informative: rising means retrieval or tools are degrading; falling means the agent has
> become bolder without becoming better.

## The weekly five-minute check

| Check | Where | Healthy |
| --- | --- | --- |
| Fallback model share | Response logs | < 5% |
| Abstention rate vs last week | Daily metric | Within ±30% |
| Newest indexed document age | Ingestion job | < 2× sync interval |
| Cost per resolved task | Cost metric | Within 20% of baseline |
| Newest golden-set case | Repo | < 60 days old |

Five minutes. It will catch more real problems than any dashboard nobody opens.

## Anti-pattern: alerting on error rate alone

Error rate is the one thing that is *already* loud. An agent can have a 0% error rate and be wrong most of
the time. If your alerting is error-rate-based, you are monitoring the failure mode you would have noticed
anyway.

## Where this shows up

- [Module 13](../../modules/13-agentic-qa-and-evaluation/) — evaluation and observability
- [CloudWatch filters](../../modules/13-agentic-qa-and-evaluation/src/cloudwatch_filters.md)
- [Model failover](../../modules/14-end-to-end-production/src/model_failover.py) — logging which model answered

**Related:** [Failure Signature Catalog](failure-signature-catalog.md) ·
[Demo-to-Production Gap](demo-to-production-gap.md) · [Abstention Budget](abstention-budget.md)
