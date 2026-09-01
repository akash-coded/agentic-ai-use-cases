# MAS-02 · Solution

## Specialist count hits the total twice

The term people model is the handoff: *n* specialists, *n* handoffs. The term they miss is the merge — and
the merge carries **every** specialist's output, so it grows with *n* as well.

```
handoffs = n × (handoff_context + result)
merge    = base_context + n × result        ← the second hit
```

Going from two specialists to four does not double the cost. It roughly doubles the handoffs *and* grows
the single most expensive call in the topology. That is why `t_many_specialists` crosses 4× at six
specialists on entirely reasonable per-agent numbers.

## What crosses a handoff is the biggest lever you control

`handoff_context_tokens` is a separate input from `base_context_tokens` precisely so you can model the
decision.

The Break phase makes it concrete: the same three-specialist delegation, changing only what crosses the
handoff from a 400-token summary to the full 2,400-token context, moves H× by more than 40%. The
architecture diagram is identical. The bill is not.

"Just give each agent everything" is the default when nobody decides, and it is the most expensive
option available.

## Unbounded is not a big number, it is a different category

`rounds <= 0` does not mean cheap or expensive. It means **unknown**, and an unknown you cannot bound is
not an estimate.

The reference warns rather than guessing, because a swarm with no termination condition does not have a
cost — it has a spending rate. The right response at a design review is not a bigger number, it is a stop
rule.

## Why single must return exactly 1.0

It is the denominator. If a single agent's estimate drifts, every H× in every comparison drifts with it,
and the number stops being portable between designs. The hidden check pins it deliberately.

## Using this in a review

H× is useful because it fits in one sentence:

> "Four specialists puts us at 4.8×. The extra 3.8× buys focused context per specialist. The alternative
> is a single agent with a longer prompt at 1.0×, which we measured at eleven points lower on the golden
> set."

That is a defensible trade. "We went multi-agent for separation of concerns" is not, because it has no
number attached and no rejected alternative.

## Field guide

[Handoff Multiplier](../../../../cheatsheets/frameworks/handoff-multiplier.md) ·
[Token Tax Ledger](../../../../cheatsheets/frameworks/token-tax-ledger.md) ·
[Choose a topology](../../../../cheatsheets/how-to/architects/choose-a-topology.md)
