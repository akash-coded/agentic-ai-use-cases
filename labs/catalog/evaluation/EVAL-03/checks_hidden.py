from harness import check, expect, expect_eq
from _fixtures import THRESHOLDS, reports


@check("a value exactly on the bar passes",
       teaches="Off-by-one on the boundary blocks good builds and erodes trust in the gate.")
def t_boundary(m):
    r = m.evaluate_gate(reports(pass_rate=0.85, cost=0.08, p95=12000), THRESHOLDS)
    expect_eq(r["decision"], "promote", "≥ and ≤ include the bar itself")


@check("an unset threshold is skipped, not failed")
def t_partial_thresholds(m):
    r = m.evaluate_gate(reports(cost=99.0), {"min_pass_rate": 0.85})
    expect_eq(r["decision"], "promote", "a bar nobody set cannot be breached")
    expect_eq(r["checked"], 1)


@check("a None threshold is treated as unset")
def t_none_threshold(m):
    th = dict(THRESHOLDS); th["max_cost_usd"] = None
    r = m.evaluate_gate(reports(cost=99.0), th)
    expect_eq(r["decision"], "promote")


@check("checked counts the bars actually evaluated")
def t_checked(m):
    expect_eq(m.evaluate_gate(reports(), THRESHOLDS)["checked"], 6)


@check("a missing report section blocks every bar that needed it")
def t_missing_section(m):
    bad = reports(); del bad["observability"]
    r = m.evaluate_gate(bad, THRESHOLDS)
    metrics = {b["metric"] for b in r["breaches"]}
    expect(metrics >= {"max_cost_usd", "max_p95_ms"},
           f"both observability bars should breach, got {sorted(metrics)}")
