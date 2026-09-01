# TOOL-03 · Solution

## Why an exception is safer than `[]`

An exception cannot be mistaken for data. `[]` can, and is.

This is the counter-intuitive centre of the lab: the *most dangerous* tool return is not the one that
fails loudly, it is the one that succeeds quietly with a value that reads as an answer. Ranked by risk:

| Return | Risk |
| --- | --- |
| `raise TimeoutError(...)` | Low — impossible to misread |
| `{"status": "no_matches", "advice": "..."}` | Low — explicit, and it says what to do |
| `{"status": "no_matches"}` | Medium — honest, but the model still has to interpret it |
| `[]` | **High** — reads as "nothing applies" |
| `{}` | **High** — reads as "no constraints" |

## Why `advice` earns its tokens

`{"status": "no_matches"}` is honest and passive. The model must decide what an absence means, and its
default is to produce something.

```json
{"status": "no_matches",
 "advice": "The corpus was searched and held nothing relevant. Do NOT conclude that no policy applies —
            say you could not find one, and escalate."}
```

That is maybe twenty extra tokens on a path that fires rarely. It replaces a judgement call the model gets
wrong with an instruction it follows. Note it is phrased as **what not to conclude** as well as what to do:
the failure mode is specific, so the instruction is specific.

## `searched_count` is evidence

Including it lets a downstream consumer — and a human reading logs — tell the difference between "searched
3 passages, found nothing" and "searched 0 passages because the corpus never loaded". Both are
`no_matches` by status; only one is a real result.

## The Break phase tests the consumer, not the search

The `_route()` function in the Break checks is deliberately dumb: it branches on `status` and nothing else.
That is the point. **If a five-line router cannot classify your return value, the model is your router** —
and unlike the router, it will not fall through to `"unknown"`. It will pick something.

The serialisation check is the sharpest one. Two outcomes that produce byte-identical JSON are, from the
model's side, the same outcome. Whatever distinction you did not encode in the payload does not exist
downstream, no matter how clear it was in your head when you wrote the function.

## Where this shows up next

- [AGL-01](../../agent-loop/AGL-01/) — the dispatcher wraps this; both must be honest for either to matter
- [RET-05](../../retrieval/RET-05/) — an uncited claim has the same root cause
- `EVAL-02` (specified, [not yet built](../../../PATHWAY.md#-evaluation)) — this is what makes correct abstention measurable

## Field guide

[Tool Surface Audit](../../../../cheatsheets/frameworks/tool-surface-audit.md) — failure honesty is one of
six axes · [Failure Signature Catalog](../../../../cheatsheets/frameworks/failure-signature-catalog.md)
row 13 · [Grounding Triangle](../../../../cheatsheets/frameworks/grounding-triangle.md)
