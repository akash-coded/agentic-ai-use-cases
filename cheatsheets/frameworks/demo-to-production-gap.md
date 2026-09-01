# The Demo-to-Production Gap: Nine Deltas

> **One line:** a demo and a production system differ in nine specific, enumerable ways — and your demo
> was passing because of all nine, not despite them.

Everyone knows "demos lie". Almost nobody can list *how*. Here is the list. Use it as a pre-mortem: for
each delta, say what changes and what you will do about it.

---

| # | In the demo | In production | What breaks first |
| --- | --- | --- | --- |
| 1 | **Inputs you chose** | Inputs that arrive | Cases you never imagined; the long tail is most of the traffic |
| 2 | **One user at a time** | Concurrency | Throttling, rate limits, timeouts under load |
| 3 | **You were watching** | Nobody is watching | Failures are silent until a human complains |
| 4 | **Fresh index** | Index drifting since last sync | Confident answers from withdrawn policy |
| 5 | **Cooperative users** | Confused, adversarial and automated users | Prompt injection, nonsense input, retry storms |
| 6 | **Happy-path data** | Nulls, duplicates, encoding, half-migrated records | Tool errors the agent narrates as facts |
| 7 | **One model version** | Models deprecate and shift | Behaviour changes with no code change |
| 8 | **Cost was invisible** | Cost is a line item someone owns | The bill arrives before the value does |
| 9 | **Failure was a retry** | Failure is an incident with a customer attached | No rollback, no runbook, no on-call |

## The pre-mortem, filled in

For each delta, one sentence. If you cannot fill a row, that row is your risk.

| # | What changes for us | What we will do | Owner |
| --- | --- | --- | --- |
| 1 Inputs | | Sample 100 real inputs into the golden set | |
| 2 Concurrency | | Load test at 3× expected peak | |
| 3 Unwatched | | Trace id + alert on abstention-rate change | |
| 4 Staleness | | Ingestion freshness check in the gate | |
| 5 Adversarial | | Adversarial slice in the golden set | |
| 6 Dirty data | | Tool failure honesty tests | |
| 7 Model drift | | Pin the model; version the manifest | |
| 8 Cost | | Budget alarm + cost per task in the gate | |
| 9 Incident | | Runbook + rehearsed rollback | |

## The three that catch people hardest

**Delta 3 — nobody is watching.** In a demo, you notice a bad answer instantly. In production, a bad answer
looks exactly like a good one until a customer escalates. This is why
[silent degradation](silent-degradation-watchlist.md) deserves its own watchlist.

**Delta 6 — dirty data.** Your tool returns `null` for a field that was always populated in testing. The
model does not error; it narrates around the gap and produces a fluent, wrong answer. Tools must fail
*loudly and honestly*, and the agent must be tested against tool failure.

**Delta 9 — failure is an incident.** In a demo you re-run the cell. In production someone is waiting, the
answer already went out, and the question is whether you can undo it. See the
[Reversibility Test](reversibility-test.md).

## The honest demo

If you must demo, close the gap a little:

- Take three inputs **from the audience**, unrehearsed
- Show one case where the agent **abstains** — this builds more trust than any success
- Show the trace, not just the answer
- Say the cost per interaction out loud

An audience that sees an agent decline to answer trusts the answers it does give. This is
counter-intuitive and reliably true.

## Where this shows up

- [Module 13](../../modules/13-agentic-qa-and-evaluation/) — golden sets built from real traffic
- [Module 14](../../modules/14-end-to-end-production/) — deploy, gate, fail over, roll back
- [Production readiness PRD](../../docs/prd/05-production-readiness.md)

**Related:** [Silent Degradation Watchlist](silent-degradation-watchlist.md) ·
[Evidence Ladder](evidence-ladder.md) · [Reversibility Test](reversibility-test.md)
