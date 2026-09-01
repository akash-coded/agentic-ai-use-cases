"""EVAL-03 — reference solution.

Absolutes are listed first because CI output is read top-down under time
pressure, and a safety breach must not be the fourth line.
"""

BARS = [
    ("max_test_failures", "tests",         "failed",           "max", "absolute"),
    ("min_pass_rate",     "evals",         "pass_rate",        "min", "average"),
    ("min_safety_rate",   "evals",         "safety_pass_rate", "min", "absolute"),
    ("max_cost_usd",      "observability", "cost_usd",         "max", "average"),
    ("max_p95_ms",        "observability", "p95_ms",           "max", "average"),
    ("max_uncited_claims", "evals",        "uncited_claims",   "max", "absolute"),
]


def evaluate_gate(reports: dict, thresholds: dict) -> dict:
    breaches, checked = [], 0

    for key, section, field, direction, kind in BARS:
        if key not in thresholds or thresholds[key] is None:
            continue
        bar = thresholds[key]
        checked += 1

        data = reports.get(section)
        if not isinstance(data, dict) or field not in data or data[field] is None:
            breaches.append({"metric": key, "actual": None, "bar": bar, "kind": kind,
                             "detail": f"{section}.{field} missing — an absent number is not a met bar"})
            continue

        actual = data[field]
        if isinstance(actual, bool) or not isinstance(actual, (int, float)):
            breaches.append({"metric": key, "actual": actual, "bar": bar, "kind": kind,
                             "detail": f"{section}.{field} is {type(actual).__name__}, not a number — "
                                       f"an unreadable metric is an unmet bar"})
            continue

        ok = actual <= bar if direction == "max" else actual >= bar
        if not ok:
            breaches.append({"metric": key, "actual": actual, "bar": bar, "kind": kind,
                             "detail": f"{actual} vs {'≤' if direction == 'max' else '≥'} {bar}"})

    breaches.sort(key=lambda b: 0 if b["kind"] == "absolute" else 1)

    if breaches:
        worst = breaches[0]
        summary = (f"BLOCKED on {len(breaches)} breach(es); "
                   f"first is {worst['metric']} ({worst['kind']}): {worst.get('detail', '')}")
        return {"decision": "block", "exit_code": 1, "breaches": breaches,
                "checked": checked, "summary": summary}

    return {"decision": "promote", "exit_code": 0, "breaches": [], "checked": checked,
            "summary": f"All {checked} bars met — promote."}
