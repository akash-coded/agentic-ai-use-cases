# How to · Set up on-call for an agent

**Time:** a day to set up, ongoing to maintain. **The gap:** agents fail *silently*, so standard on-call —
built around alerts firing on errors — misses almost everything that matters.

---

## 1. Accept the difference

| Normal service | Agent |
| --- | --- |
| Fails loudly (5xx, exceptions) | Fails **fluently** — a wrong answer looks like a right one |
| Error rate is the signal | Error rate can be 0% while it is wrong most of the time |
| Users report outages | Users report "it seemed off", days later |
| Rollback restores state | Rollback cannot un-send an answer |

Your alerting must be built around **quality drift**, not availability.

## 2. Alert on the three vital signs

| Alert | Threshold | Means |
| --- | --- | --- |
| Fallback model share | > 5% | Silent failover; quality may have dropped |
| Abstention rate change | ±30% week on week | Retrieval, tools or prompt drifted |
| Cost per task | > 20% over baseline | A [cost cliff](../../frameworks/cost-cliff-map.md) fired |

Plus three that are pass/fail:

| Alert | Threshold |
| --- | --- |
| Uncited factual answers | > 0 |
| Index age | > 2 × sync interval |
| p95 turns per task | > baseline + 1 |

Six alerts. Each needs an owner or it is a dashboard, not an alert.

## 3. Write the runbooks before you need them

Link them **from the alert**, so the on-call person does not have to search at 2 a.m.:

| Alert | Runbook |
| --- | --- |
| Quality complaints | [Wrong answers](../../runbooks/incident-wrong-answers.md) |
| Cost | [Cost spike](../../runbooks/incident-cost-spike.md) |
| Latency | [Latency regression](../../runbooks/incident-latency-regression.md) |
| Turns climbing | [Runaway loop](../../runbooks/incident-runaway-loop.md) |
| Index age | [Stale knowledge](../../runbooks/incident-stale-knowledge.md) |

## 4. Give on-call the authority to roll back

Rollback criteria are agreed **in advance**, in the
[production readiness artefact](../../../docs/prd/05-production-readiness.md), so nobody is making a
judgement call under pressure at 2 a.m.:

> Roll back without escalation if: a policy-contradicting answer reaches a user; resolution drops below
> X%; cost per task exceeds $Y; or p95 latency exceeds Z.

**On-call must be able to roll back without waking anyone.** If they cannot, your MTTR is however long it
takes to find someone.

## 5. Rehearse it

Once per release cycle, in a non-production environment: deploy A, deploy B, roll back to A using only the
manifest, time it, write the time down. See [rollback](../../runbooks/rollback.md).

If rollback requires a rebuild, you do not have rollback.

## 6. The user-report path

Most agent incidents arrive as "it gave me a weird answer", not as an alert. Make that reportable:

- A one-click "this was wrong" in the interface
- The **trace id** captured automatically with the report
- A triage rota — someone reads these daily
- Confirmed cases go into the golden set

> Without the trace id, a user report is unactionable. With it, it is a five-minute investigation. This is
> the single highest-return piece of plumbing you can build.

## 7. Handover template

```
Agent:            [name]         Owner: [team]
What it does:     [one line]
Blast radius:     [what it can and cannot change]
Vital signs:      [dashboard link]
Rollback:         [command] — last rehearsed [date], takes [N] minutes
Rollback authority: on-call, without escalation, per criteria in [link]
Runbooks:         [links]
Escalate to:      [person] if [condition]
Known issues:     [list]
```

## 8. The weekly five-minute check

Someone's calendar, not "when we remember":

| Check | Healthy |
| --- | --- |
| Fallback model share | < 5% |
| Abstention rate vs last week | ±30% |
| Newest indexed document | < 2× sync interval |
| Cost per resolved task | within 20% |
| Newest golden-set case | < 60 days |

Five minutes weekly catches more real problems than any dashboard nobody opens.

**Related:** [Silent Degradation Watchlist](../../frameworks/silent-degradation-watchlist.md) ·
[Observability](../../quick-reference/observability.md) · [Runbooks](../../runbooks/)
