# EVAL-101 · Which bars are absolute?

`evaluation` · **medium** · `blank` · ~10 min · no AWS account

A release gate compares metrics against bars. Some bars are **averages** — a few misses are acceptable, that is what the number means. Some are **absolutes** — one miss is a defect. Mixing them is how a build at 99% overall with a single policy-contradicting answer gets promoted.

Fill in the four blanks.

```python
BARS = [
    # (threshold key,        section, field,             direction, kind)
    ("min_pass_rate",        "evals", "pass_rate",        "min",  ____1____),
    ("min_safety_rate",      "evals", "safety_pass_rate", "min",  ____2____),
    ("max_uncited_claims",   "evals", "uncited_claims",   "max",  ____3____),
    ("max_cost_usd",         "obs",   "cost_usd",         "max",  "average"),
]

def evaluate_gate(reports, thresholds):
    breaches = []
    for key, section, field, direction, kind in BARS:
        if key not in thresholds: continue
        bar = thresholds[key]; actual = reports.get(section, {}).get(field)
        if actual is None:
            breaches.append({"metric": key, "kind": kind, "actual": None, "bar": bar}); continue
        ok = actual <= bar if direction == "max" else actual >= bar
        if not ok: breaches.append({"metric": key, "kind": kind, "actual": actual, "bar": bar})
    breaches.sort(key=lambda b: ____4____)        # absolutes must come FIRST
    return {"decision": "block" if breaches else "promote", "breaches": breaches}
```

| | What goes here |
| --- | --- |
| `____1____` | `"average"` or `"absolute"` — a pass rate of 0.85 explicitly permits misses |
| `____2____` | `"average"` or `"absolute"` — is one policy-contradicting answer a rounding error? |
| `____3____` | `"average"` or `"absolute"` — is one uncited factual claim acceptable? |
| `____4____` | A sort key so absolute breaches are listed before averages |

Post the completed code (both `BARS` and the function):

````markdown
/drill EVAL-101

```python
BARS = [...]
def evaluate_gate(reports, thresholds):
    ...
```
````

## What this proves

That you can classify a metric by what a miss *means*, and that you know CI output is read top-down under pressure — so the line that matters cannot be fourth.
