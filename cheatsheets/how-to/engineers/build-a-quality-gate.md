# How to · Build a quality gate that actually blocks

**Time:** half a day. **You need:** a golden set, or 30 minutes to start one.

A gate that warns is not a gate. Teams learn to ignore it within a week. This one exits non-zero.

---

## 1. Three reports in, one decision out

```
test_report.json    ← pytest        {"failed": 0}
eval_report.json    ← golden set    {"pass_rate": 0.87, "safety_pass_rate": 1.0}
cost_latency.json   ← observability {"cost_usd": 0.031, "p95_ms": 5400}
                              ↓
                        quality_gate.py
                              ↓
                    exit 0 (promote) | exit 1 (BLOCK)
```

Keeping the reports separate means each stage can run independently and the gate stays a pure function of
its inputs.

## 2. Thresholds live in code, reviewed

```python
# config.py
THRESHOLDS = {
    "max_test_failures":  0,
    "min_pass_rate":      0.85,
    "min_safety_rate":    1.00,   # not 0.99 — a policy-contradicting answer is not a rounding error
    "max_cost_usd":       0.08,
    "max_p95_ms":         12_000,
}
```

Changing a bar is a commit, reviewed by someone who did not write it, and **never in the same commit as
the code it would let through**.

## 3. The gate

```python
import json, sys

def gate(tests, evals, obs, th):
    checks = [
        ("tests failed",   tests["failed"],        "<=", th["max_test_failures"]),
        ("pass rate",      evals["pass_rate"],     ">=", th["min_pass_rate"]),
        ("safety rate",    evals["safety_pass_rate"], ">=", th["min_safety_rate"]),
        ("cost per task",  obs["cost_usd"],        "<=", th["max_cost_usd"]),
        ("p95 latency ms", obs["p95_ms"],          "<=", th["max_p95_ms"]),
    ]
    failures = []
    for name, actual, op, bar in checks:
        ok = actual <= bar if op == "<=" else actual >= bar
        print(f"{'PASS' if ok else 'FAIL'}  {name}: {actual} {op} {bar}")
        if not ok:
            failures.append(f"{name}: {actual} vs {bar}")
    return failures

failures = gate(*[json.load(open(f)) for f in sys.argv[1:4]], THRESHOLDS)
if failures:
    print("\nBLOCKED:\n  " + "\n  ".join(failures))
    sys.exit(1)          # ← the whole point
print("\nPromote.")
```

Reference implementation:
[`quality_gate.py`](../../../modules/13-agentic-qa-and-evaluation/src/quality_gate.py).

## 4. Wire it so it can say no

```yaml
- name: Quality gate
  run: python quality_gate.py --tests test_report.json --evals eval_report.json --obs cost_latency.json
```

No `continue-on-error`. No `|| true`. If the job cannot block the deploy, you have built a report.

## 5. Prove it blocks

**Do this before you trust it.** Deliberately regress the agent — remove a tool, break retrieval, weaken
the prompt — and confirm the gate fails.

A gate that has never fired is a gate nobody has tested.

## 6. Add the checks specific to agents

Beyond the five above, these catch agent-specific failures:

| Check | Blocks |
| --- | --- |
| Index freshness (`index_age < 2 × sync_interval`) | Stale-knowledge incidents |
| Uncited factual answers = 0 | Grounding regressions |
| Abstention rate within a band | Bolder-not-better prompt changes |
| Turns per task ≤ baseline + 1 | Cost cliffs from loops and retries |

## Anti-patterns

| Anti-pattern | Why it fails |
| --- | --- |
| Gate warns instead of failing | Ignored within a week |
| Safety averaged into the headline number | Hides the failure that matters most |
| Threshold edited to pass a build | You have edited the test |
| Golden set is a mirror of agent output | Measures nothing |
| Gate takes 40 minutes | Gets skipped under pressure |

**Related:** [Evidence Ladder](../../frameworks/evidence-ladder.md) ·
[Module 13](../../../modules/13-agentic-qa-and-evaluation/) ·
[QA interview guide](../../interviews/qa-engineer.md)

**Runnable:** [`release_gate.py`](https://gist.github.com/akash-coded/908a2f096a89de29d3b3221244773a1b) — the whole gate in forty lines: exits non-zero, absolutes first, never raises. Its demo deliberately feeds it a build that a headline score would promote, so running it ends with exit code 1 — that is the gate working.
