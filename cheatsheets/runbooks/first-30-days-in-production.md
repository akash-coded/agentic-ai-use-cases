# Runbook · First 30 days in production

Launch is not the finish line; it is the point at which you start learning things your golden set could not
tell you. This is a schedule, not a checklist — each window has a different job.

---

## Days 1–3 · Watch closely

**Job: catch the fast failures.**

| Daily | Healthy |
| --- | --- |
| Abstention rate | Within ±30% of shadow-traffic baseline |
| Fallback model share | < 5% |
| Cost per task | Within 20% of projection |
| p95 latency | Within budget |
| Uncited factual answers | **Zero** |

**Read 20 real interactions end to end, by hand.** Not sampled metrics — actual transcripts. This is the
highest-value activity of the entire month, and the only one that catches problems nobody thought to
measure.

## Days 4–10 · Find the distribution gap

**Job: discover what your golden set did not contain.**

- [ ] Sample 50 real inputs. How many resemble golden-set cases?
- [ ] Cluster the ones that do not. Those clusters are your missing slices
- [ ] Add at least 20 real cases to the golden set — prioritise ones you currently fail
- [ ] Check the abstention cases: is it abstaining on the *right* things?

> Expect 20–40% of real traffic to look unlike anything in your golden set. That is normal, and it is why
> [delta 1](../frameworks/demo-to-production-gap.md) exists.

## Days 11–20 · Tune what the data now supports

**Job: make evidence-based changes, one at a time.**

| Question | Action if the answer is bad |
| --- | --- |
| Is retrieval recall holding as the corpus grows? | Re-measure at several k; improve ranking |
| Is abstention too high? | Usually retrieval, not the prompt |
| Is abstention too low? | Check confident-wrong before celebrating |
| Is cost above projection? | Turns first, then retrieval, then schemas |
| Which route is most expensive? | Consider routing it away from the agent |

One change at a time, each with a golden-set run before and after. See
[shipping a prompt change](deploy-prompt-change.md).

## Days 21–30 · Institutionalise

**Job: make this survivable without you.**

- [ ] Alerts have **owners**, not just thresholds
- [ ] Weekly five-minute check is on someone's calendar
- [ ] Runbooks exist for the two failures you actually hit
- [ ] Rollback rehearsed and timed
- [ ] Golden set has grown by at least 20 real cases
- [ ] Gate thresholds reflect reality, not launch-day optimism

## Day 30 · The post-launch review

Run the [post-launch review](../../docs/prd/06-post-launch-review.md). The two sections that matter:

1. **What the golden set missed** — every production failure with no golden-set analogue
2. **What we would tell ourselves at Gate 1** — one or two sentences that would have changed the build

Be uncomfortable. A review that finds nothing wrong found nothing.

## The metric people forget to predict

**Abstention rate.** Nobody predicts it, so nobody notices when it is wrong in either direction. An agent
that abstains on 40% of enquiries meets a "60% autonomous resolution" target while being far less useful
than intended.

Predict it before launch. Compare it on day 30.

## The three questions at day 30

1. **Is it doing what we said?** — against the [Value Trace](../frameworks/value-trace.md), honestly
2. **What have we learned that changes the design?**
3. **What would we need to see to switch it off?** — if you cannot answer, you have no kill criteria

**Related:** [Demo-to-Production Gap](../frameworks/demo-to-production-gap.md) ·
[Silent Degradation Watchlist](../frameworks/silent-degradation-watchlist.md)
