# PROD-02 · Solution

## One boolean is the whole lab

Everything here is plumbing around `degraded`. Without it, failover is a feature that quietly lowers
answer quality and produces no signal at all — the request succeeded, latency was fine, error rate stayed
at zero.

With it, you get a metric: **fallback share**. Alert above 5% and the six-week quality drop becomes a
Tuesday-morning question instead of a customer escalation.

That is the first row of the
[Silent Degradation Watchlist](../../../../cheatsheets/frameworks/silent-degradation-watchlist.md), and
it costs one field on the response.

## Retryable versus fatal

Retrying a throttle is sensible: capacity comes back, and a different model has different capacity.

Retrying a malformed request is not. The request will be malformed on the fallback too, so you have paid
twice the latency and twice the tokens to produce the same failure — and you have hidden the real cause
behind a longer attempt chain.

The classification belongs outside this function, because it is provider-specific and changes more often
than the failover logic does.

## An unclassifiable error is fatal, not retryable

The Break phase makes `classify_error` itself raise. The instinct is to default to `retryable` — be
generous, try the next one.

That is backwards. An error you cannot classify is an error you do not understand, and walking a chain of
five models on something you do not understand costs five times as much to learn nothing. Fail fast, and
put the unclassified error in the attempt record where someone will see it and add a rule.

## `failed` and `degraded` are independent

A failed chain reports `degraded=False`, and the hidden check pins it. Nothing answered, so nothing was
degraded.

Conflating them corrupts the metric in the direction that hurts: fallback share spikes during an outage,
which is exactly when you need it to mean what it normally means. Outages are already loud. Keep
`degraded` measuring the quiet thing.

## `except BaseException`, again

Same reasoning as [AGL-01](../../agent-loop/AGL-01/). This function is a boundary, and a boundary's job is
to convert anything at all into a value the layer above can reason about. A dependency calling `sys.exit()`
on a config problem should not take the request with it.

## Field guide

[Silent Degradation Watchlist](../../../../cheatsheets/frameworks/silent-degradation-watchlist.md) ·
[Observability](../../../../cheatsheets/quick-reference/observability.md) ·
[`model_failover.py`](../../../../modules/14-end-to-end-production/src/model_failover.py)
