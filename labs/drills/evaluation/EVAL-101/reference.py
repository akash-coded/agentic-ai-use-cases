BARS = [
    ("min_pass_rate",      "evals", "pass_rate",        "min", "average"),
    ("min_safety_rate",    "evals", "safety_pass_rate", "min", "absolute"),
    ("max_uncited_claims", "evals", "uncited_claims",   "max", "absolute"),
    ("max_cost_usd",       "obs",   "cost_usd",         "max", "average"),
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
    breaches.sort(key=lambda b: 0 if b["kind"] == "absolute" else 1)
    return {"decision": "block" if breaches else "promote", "breaches": breaches}
