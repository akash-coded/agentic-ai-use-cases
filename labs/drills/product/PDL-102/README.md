# PDL-102 · Derive the abstention target from real traffic

`product` · **easy** · `blank` · ~8 min · no AWS account

Nobody sets a target for how often an agent should say "I don't know", so nobody notices when it declines never (dangerous) or always (useless). The target is a property of **your inputs**, not your model. Fill the blanks.

```python
def abstention_target(counts: dict) -> dict:
    """counts: classified real inputs, e.g.
       {"answerable": 58, "ambiguous": 14, "out_of_scope": 9, "unretrievable": 11, "adversarial": 8}
    """
    should_abstain = counts["____1____"] + counts["____2____"] + counts["____3____"]
    total = ____4____
    rate = should_abstain / total
    return {"target": round(rate, 3),
            "band": (round(rate - 0.05, 3), round(rate + 0.05, 3)),   # ±5 points
            "n": total}
```

| | What goes here |
| --- | --- |
| `____1____` `____2____` `____3____` | The three classes whose correct behaviour is to abstain |
| `____4____` | The denominator — every classified input |

````markdown
/drill PDL-102

```python
def abstention_target(counts):
    ...
```
````

## What this proves

That you can put a number on the vital sign before launch — so that a week-two drop in abstentions reads as "bolder, not better" instead of "improvement".
