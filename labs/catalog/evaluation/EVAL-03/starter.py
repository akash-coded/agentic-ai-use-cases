"""EVAL-03 — a gate that can say no."""

# (metric key, report section, field, comparison, kind)
BARS = [
    ("max_test_failures", "tests",         "failed",           "max", "absolute"),
    ("min_pass_rate",     "evals",         "pass_rate",        "min", "average"),
    ("min_safety_rate",   "evals",         "safety_pass_rate", "min", "absolute"),
    ("max_cost_usd",      "observability", "cost_usd",         "max", "average"),
    ("max_p95_ms",        "observability", "p95_ms",           "max", "average"),
    ("max_uncited_claims", "evals",        "uncited_claims",   "max", "absolute"),
]


def evaluate_gate(reports: dict, thresholds: dict) -> dict:
    """Compare every report against every bar and return a decision."""
    breaches = []
    checked = 0

    # TODO 1 — walk BARS. Skip a bar that is not in `thresholds` (not every
    #          project sets every one), but never skip one that IS set.

    # TODO 2 — a missing report section, or a missing field, is a BLOCK.
    #          An absent number is not a satisfied bar. Nor is an unreadable one:
    #          this function must never raise, whatever it is handed.

    # TODO 3 — compare in the right direction ("min" => actual >= bar,
    #          "max" => actual <= bar) and record a breach with its kind.

    # TODO 4 — absolutes first in the breach list, then averages.
    #          Any breach at all means block and exit_code 1.

    raise NotImplementedError("implement evaluate_gate()")
