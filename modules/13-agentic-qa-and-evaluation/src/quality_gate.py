"""
quality_gate.py   (Topic 4)
===========================
The gate with teeth. This is the file that turns Topics 1 to 3 into a single
decision: may this build be promoted, yes or no.

What it does, in one breath:
    Read three small JSON reports produced earlier in the pipeline, check each
    number against an agreed threshold, write a human-readable sign-off, and exit
    non-zero if any bar was missed. A non-zero exit is what makes a CI step BLOCK
    a deploy. A gate that only prints a warning is not a gate; teams learn to
    ignore it within a week.

The three inputs (each is produced by an earlier stage):
    test_report.json   from pytest        ->  {"failed": <int>}
    eval_report.json   from Topic 2       ->  {"pass_rate": <float>, "safety_pass_rate": <float>}
    cost_latency.json  from Topic 3       ->  {"cost_usd": <float>, "p95_ms": <int>}

The bars live in config.THRESHOLDS, so tightening a bar is a one-line, reviewed
change committed with the code.

Run it directly (works with no AWS; it only reads files):
    python quality_gate.py \
        --tests test_report.json --evals eval_report.json --obs cost_latency.json \
        --build travelmind-2026.06.11-rc3 --prompt v7
    echo $?        # 0 = passed and promotion proceeds, 1 = failed and CI stops

Or import it from the end-to-end pipeline (run_qa_pipeline.py calls run_gate()).
"""

import argparse
import datetime
import json
import sys

import config


# ---------------------------------------------------------------------------
# Human labels for each check, so the sign-off reads in plain English. Keeping
# this next to the threshold keys means the report and the logic never drift.
# Each entry: internal key -> (label, threshold text, how to read the actual).
# ---------------------------------------------------------------------------
_BAR_LABELS = {
    "tests":  ("Tool + behaviour tests", "0 failures"),
    "eval":   ("Eval pass rate",         f">= {config.THRESHOLDS['eval_pass_rate']:.0%}"),
    "cost":   ("Cost per resolution",    f"<= ${config.THRESHOLDS['max_cost_usd']:.2f}"),
    "p95":    ("p95 latency",            f"<= {config.THRESHOLDS['p95_latency_ms']} ms"),
    "safety": ("Safety and PII",         f">= {config.THRESHOLDS['safety_pass_rate']:.0%}"),
}


def load_report(path: str) -> dict:
    """Read one JSON report. Fail loudly with a clear message if it is missing,
    because a missing report usually means an earlier stage did not run, and a
    silent default would hide that."""
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        sys.exit(f"GATE ERROR: report not found: {path}. Did the earlier stage run?")
    except json.JSONDecodeError as e:
        sys.exit(f"GATE ERROR: {path} is not valid JSON ({e}).")


def evaluate_gate(tests: dict, evals: dict, obs: dict):
    """Compare each report value to its threshold.

    Returns two dicts:
        checks  -> {bar_key: bool}        did this bar pass
        actuals -> {bar_key: str}         the actual value, formatted for the report
    Keeping the booleans and the display values separate keeps the decision logic
    clean and the formatting in one place."""
    t = config.THRESHOLDS

    checks = {
        "tests":  tests["failed"] == 0,
        "eval":   evals["pass_rate"]        >= t["eval_pass_rate"],
        "cost":   obs["cost_usd"]           <= t["max_cost_usd"],
        "p95":    obs["p95_ms"]             <= t["p95_latency_ms"],
        "safety": evals["safety_pass_rate"] >= t["safety_pass_rate"],
    }
    actuals = {
        "tests":  f"{tests['failed']}",
        "eval":   f"{evals['pass_rate']:.0%}",
        "cost":   f"${obs['cost_usd']:.3f}",
        "p95":    f"{obs['p95_ms']} ms",
        "safety": f"{evals['safety_pass_rate']:.0%}",
    }
    return checks, actuals


def write_signoff(checks: dict, actuals: dict, meta: dict, path: str) -> None:
    """Write the sign-off report as Markdown. This is the artifact you hand the
    client: proof that a specific build cleared every bar, with the evidence in a
    table. It is generated, not hand-typed, so it always matches the gate run."""
    passed = all(checks.values())
    decision = ("APPROVED for blue-green promotion."
                if passed else
                "BLOCKED. Do not promote. Fix the failing bars and re-run.")

    lines = []
    lines.append("# TravelMind Release Sign-off")
    lines.append("")
    lines.append(f"- Build: `{meta['build']}`")
    lines.append(f"- Model: `{meta['model']}`")
    lines.append(f"- Prompt: `{meta['prompt']}`")
    lines.append(f"- Generated: {meta['timestamp']}")
    lines.append("")
    lines.append("| Gate | Threshold | Actual | Result |")
    lines.append("|------|-----------|--------|--------|")
    for key, (label, threshold_text) in _BAR_LABELS.items():
        result = "PASS" if checks[key] else "FAIL"
        lines.append(f"| {label} | {threshold_text} | {actuals[key]} | {result} |")
    lines.append("")
    lines.append(f"**Decision:** {decision}")
    lines.append("")
    lines.append("_Signed: QA owner._")
    lines.append("")

    with open(path, "w") as f:
        f.write("\n".join(lines))


def run_gate(tests_path: str, evals_path: str, obs_path: str,
             signoff_path: str = "signoff_report.md", meta: dict = None) -> bool:
    """The reusable entry point. Loads, evaluates, writes the sign-off, prints a
    one-line verdict, and returns True if the gate passed. The pipeline imports
    and calls this; main() wraps it for the command line."""
    tests = load_report(tests_path)
    evals = load_report(evals_path)
    obs = load_report(obs_path)

    checks, actuals = evaluate_gate(tests, evals, obs)

    meta = meta or {}
    meta.setdefault("build", "travelmind-local")
    meta.setdefault("model", config.AGENT_PRICE_KEY)
    meta.setdefault("prompt", "v?")
    meta.setdefault("timestamp", datetime.datetime.now().isoformat(timespec="seconds"))

    write_signoff(checks, actuals, meta, signoff_path)

    passed = all(checks.values())
    if passed:
        print("GATE PASSED ->", signoff_path)
    else:
        failed = [_BAR_LABELS[k][0] for k, ok in checks.items() if not ok]
        print("GATE FAILED ->", failed, "(see", signoff_path + ")")
    return passed


def main():
    parser = argparse.ArgumentParser(description="TravelMind quality gate")
    parser.add_argument("--tests", default="test_report.json")
    parser.add_argument("--evals", default="eval_report.json")
    parser.add_argument("--obs", default="cost_latency.json")
    parser.add_argument("--signoff", default="signoff_report.md")
    parser.add_argument("--build", default="travelmind-local")
    parser.add_argument("--model", default=config.AGENT_PRICE_KEY)
    parser.add_argument("--prompt", default="v?")
    args = parser.parse_args()

    meta = {"build": args.build, "model": args.model, "prompt": args.prompt}
    passed = run_gate(args.tests, args.evals, args.obs, args.signoff, meta)

    # The exit code is the whole point: 0 lets CI proceed, 1 stops the deploy.
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
