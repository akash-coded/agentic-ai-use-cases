"""EVAL-03 · Break phase — the builds a naive gate lets through."""
from harness import check, expect, expect_eq
from _fixtures import THRESHOLDS, reports


@check("excellent on average, one safety failure — still blocked",
       "The exact build a headline score would promote.",
       teaches="Averaging safety into an overall number is how the failure the gate exists for gets through.")
def t_good_average_bad_safety(m):
    r = m.evaluate_gate(reports(pass_rate=0.99, safety=0.995, cost=0.01, p95=900), THRESHOLDS)
    expect_eq(r["decision"], "block", "0.995 safety against a 1.0 bar is a block, whatever else is true")
    expect_eq(r["breaches"][0]["kind"], "absolute")


@check("one uncited claim blocks",
       "Absolute means one is too many.",
       teaches="'Only one uncited claim in 130' is still an ungrounded answer reaching a user.")
def t_uncited(m):
    r = m.evaluate_gate(reports(uncited=1), THRESHOLDS)
    expect_eq(r["decision"], "block")


@check("an empty reports dict blocks everything it was asked to check",
       "A crashed pipeline stage must not read as a pass.",
       teaches="This is the failure where the eval job dies and the deploy job promotes anyway.")
def t_empty_reports(m):
    r = m.evaluate_gate({}, THRESHOLDS)
    expect_eq(r["decision"], "block")
    expect_eq(len(r["breaches"]), 6, "every set bar is unmet when nothing was reported")


@check("the gate never raises, whatever it is handed",
       "It has to run in CI on a bad day.",
       teaches="A gate that crashes is a gate whose exit code is ambiguous — and someone will rerun it.")
def t_never_raises(m):
    hostile = [
        ({"tests": None, "evals": [], "observability": "nope"}, THRESHOLDS),
        ({"evals": {"pass_rate": "high"}}, {"min_pass_rate": 0.85}),
        (reports(), {}),
    ]
    for rep, th in hostile:
        try:
            out = m.evaluate_gate(rep, th)
        except Exception as e:  # noqa: BLE001
            raise AssertionError(
                f"gate raised {type(e).__name__} on {rep!r} — return a block instead") from None
        expect(out["decision"] in ("promote", "block"), "still a valid decision")
        expect(out["exit_code"] in (0, 1), "still a valid exit code")
