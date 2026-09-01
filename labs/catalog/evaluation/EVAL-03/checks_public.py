from harness import check, expect, expect_eq
from _fixtures import THRESHOLDS, reports


@check("a clean build is promoted with exit code 0")
def t_promote(m):
    r = m.evaluate_gate(reports(), THRESHOLDS)
    expect_eq(r["decision"], "promote")
    expect_eq(r["exit_code"], 0)
    expect_eq(r["breaches"], [])


@check("a breached bar blocks with exit code 1",
       "Exit code 1 is what makes CI stop.",
       teaches="A gate that returns 0 on failure is a report, and teams stop reading reports.")
def t_block(m):
    r = m.evaluate_gate(reports(pass_rate=0.60), THRESHOLDS)
    expect_eq(r["decision"], "block")
    expect_eq(r["exit_code"], 1)


@check("every breach is reported, not just the first",
       "You want one CI run to tell you everything that is wrong.")
def t_all_breaches(m):
    r = m.evaluate_gate(reports(failed=3, pass_rate=0.5, cost=0.5), THRESHOLDS)
    metrics = {b["metric"] for b in r["breaches"]}
    expect(metrics >= {"max_test_failures", "min_pass_rate", "max_cost_usd"},
           f"expected three breaches, got {sorted(metrics)}")


@check("a safety breach is marked absolute and listed first",
       "CI output is read top-down under pressure.",
       teaches="A safety failure buried at position four is a safety failure nobody read.")
def t_absolute_first(m):
    r = m.evaluate_gate(reports(safety=0.99, cost=0.5, p95=99999), THRESHOLDS)
    expect(r["breaches"], "a 0.99 safety rate must breach a 1.0 bar")
    first = r["breaches"][0]
    expect_eq(first["kind"], "absolute", "absolutes sort before averages")
    expect_eq(first["metric"], "min_safety_rate")


@check("a missing metric blocks rather than passing",
       "An absent number is not a satisfied bar.",
       teaches="Treating a missing report as a pass is how a broken eval stage ships a build.")
def t_missing(m):
    bad = reports(); del bad["evals"]["safety_pass_rate"]
    r = m.evaluate_gate(bad, THRESHOLDS)
    expect_eq(r["decision"], "block")
    expect(any(b["metric"] == "min_safety_rate" for b in r["breaches"]),
           "the missing metric must appear as a breach")


@check("the summary names the blocking reason")
def t_summary(m):
    r = m.evaluate_gate(reports(safety=0.5), THRESHOLDS)
    expect("safety" in r["summary"].lower(), f"summary should name the breach: {r['summary']!r}")
