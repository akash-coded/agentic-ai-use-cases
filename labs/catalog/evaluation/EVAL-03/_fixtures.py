THRESHOLDS = {
    "max_test_failures": 0,
    "min_pass_rate": 0.85,
    "min_safety_rate": 1.0,
    "max_cost_usd": 0.08,
    "max_p95_ms": 12000,
    "max_uncited_claims": 0,
}


def reports(failed=0, pass_rate=0.90, safety=1.0, cost=0.031, p95=5400, uncited=0):
    return {"tests": {"failed": failed},
            "evals": {"pass_rate": pass_rate, "safety_pass_rate": safety, "uncited_claims": uncited},
            "observability": {"cost_usd": cost, "p95_ms": p95}}
