"""
run_qa_pipeline.py   (end to end - the file that brings it all together)
=======================================================================
This is the one file to read if you want to see the whole QA flow at once. It is
what a release should actually DO before it ships: run the tests, score the
build, check the traces and cost, then gate on all of it and produce a sign-off.

The flow, four stages, in order:

    STAGE 1  Tool-contract tests        (Topic 1)  ->  test_report.json
    STAGE 2  Evaluation, golden set     (Topic 2)  ->  eval_report.json
    STAGE 3  Observability and cost     (Topic 3)  ->  cost_latency.json
    STAGE 4  Quality gate and sign-off  (Topic 4)  ->  signoff_report.md, exit code

Each stage writes a small JSON report. The gate in stage 4 reads those reports
and makes the promote-or-block decision. The stages are deliberately decoupled
through files: in real CI they might run on different machines or at different
times, and a file is the simplest contract between them.

Two ways to run:

    python run_qa_pipeline.py                 # ONLINE: stages 2 and 3 call Bedrock
                                              # (needs AWS credentials)

    python run_qa_pipeline.py --offline       # OFFLINE: stages 2 and 3 use sample
                                              # numbers so the FULL flow runs with
                                              # no AWS. Stage 1 (tests) and stage 4
                                              # (gate) are real either way.

Use --offline to see the pipeline work without cloud access, then switch to the
online path once credentials are in place.
"""

import argparse
import json
import subprocess
import sys
import time

import config


# ---------------------------------------------------------------------------
# STAGE 1 - tool-contract tests
# These are the deterministic, no-model tests from Topic 1. We shell out to
# pytest and use its exit code: 0 means all passed. This stage is real in both
# online and offline modes, because it needs no cloud.
# ---------------------------------------------------------------------------
def stage_1_tests() -> dict:
    print("\nSTAGE 1  tool-contract tests (deterministic, no AWS)")
    returncode = subprocess.call(
        [sys.executable, "-m", "pytest", "test_contracts.py", "-q", "--tb=no"]
    )
    # pytest exit code 0 = all passed, non-zero = at least one failed.
    # For an exact failure count, add the pytest-json-report plugin; we keep deps
    # minimal here and record the binary outcome the gate actually checks.
    failed = 0 if returncode == 0 else 1
    report = {"failed": failed}
    with open("test_report.json", "w") as f:
        json.dump(report, f, indent=2)
    print(f"  -> test_report.json  {report}")
    return report


# The same pure substring rules as eval_harness.ipynb Layer 1. It is repeated
# here on purpose: the notebook stays self-contained for teaching, and the
# pipeline stays runnable on its own. A 6-line pure function in two well-marked
# places is a smaller cost than a shared module that couples them.
def _substring_check(reply: str, case: dict) -> bool:
    text = reply.lower()
    if not all(p.lower() in text for p in case.get("must", [])):
        return False
    any_of = case.get("any_of", [])
    if any_of and not any(p.lower() in text for p in any_of):
        return False
    if any(p.lower() in text for p in case.get("must_not", [])):
        return False
    return True


# ---------------------------------------------------------------------------
# STAGE 2 - evaluation (golden set, deterministic layer)
# In a pipeline you run the cheap, deterministic eval layer automatically. The
# heavier judge and RAGAS layers (see eval_harness.ipynb) run on a schedule, not
# on every promote, because they cost model calls. Online: call the agent on the
# substring cases. Offline: use representative numbers.
# ---------------------------------------------------------------------------
def stage_2_eval(offline: bool) -> dict:
    print("STAGE 2  evaluation (golden set)")
    if offline:
        report = {"pass_rate": 0.94, "safety_pass_rate": 1.0, "note": "offline sample"}
    else:
        from travelmind_agent import get_agent
        cases = [json.loads(l) for l in open("golden_set.jsonl") if l.strip()]
        substring_cases = [c for c in cases if c["check"] == "substring"]
        agent = get_agent()

        results = []
        for case in substring_cases:
            reply = str(agent(case["input"]))                 # model call (AWS)
            results.append({"id": case["id"],
                            "passed": _substring_check(reply, case),
                            "type": case["type"]})

        rate = sum(r["passed"] for r in results) / len(results)
        safety = [r for r in results if r["type"] == "safety"]
        safety_rate = sum(r["passed"] for r in safety) / len(safety) if safety else 1.0
        report = {"pass_rate": round(rate, 4),
                  "safety_pass_rate": round(safety_rate, 4),
                  "by_case": results}

    with open("eval_report.json", "w") as f:
        json.dump(report, f, indent=2)
    print(f"  -> eval_report.json  pass {report['pass_rate']:.0%}  "
          f"safety {report['safety_pass_rate']:.0%}")
    return report


# ---------------------------------------------------------------------------
# STAGE 3 - observability and cost
# Online: run one probe, read its tokens, compute cost, time it. Offline: sample.
# Note the honest label on p95: a single probe is one latency sample, not a true
# 95th percentile. Real p95 comes from your metrics over many runs; we keep the
# field so the gate has something to check and label what it really is.
# ---------------------------------------------------------------------------
def stage_3_observability(offline: bool) -> dict:
    print("STAGE 3  observability / cost")
    if offline:
        report = {"cost_usd": 0.011, "p95_ms": 3120, "note": "offline sample"}
    else:
        from travelmind_agent import get_agent
        agent = get_agent()

        start = time.perf_counter()
        result = agent("My flight on PNR JX48Q2 was cancelled. What are my options?")
        elapsed_ms = int((time.perf_counter() - start) * 1000)

        # Read tokens defensively (attribute names vary by Strands version).
        m = getattr(result, "metrics", None)
        usage = getattr(m, "accumulated_usage", None) or {}
        in_tok = usage.get("inputTokens") or usage.get("input_tokens") or 0
        out_tok = usage.get("outputTokens") or usage.get("output_tokens") or 0

        price_in, price_out = config.PRICES[config.AGENT_PRICE_KEY]
        cost = in_tok / 1e6 * price_in + out_tok / 1e6 * price_out

        report = {"cost_usd": round(cost, 5),
                  "p95_ms": elapsed_ms,                       # single-sample stand-in
                  "note": "p95_ms is one sample; use your metrics pipeline for true p95"}

    with open("cost_latency.json", "w") as f:
        json.dump(report, f, indent=2)
    print(f"  -> cost_latency.json  {report}")
    return report


# ---------------------------------------------------------------------------
# STAGE 4 - quality gate and sign-off
# Reuse run_gate from quality_gate.py. The gate reads the three reports the
# stages above wrote, checks them against config.THRESHOLDS, writes the sign-off,
# and returns whether the build passed.
# ---------------------------------------------------------------------------
def stage_4_gate(build: str, prompt: str) -> bool:
    print("STAGE 4  quality gate")
    from quality_gate import run_gate
    meta = {"build": build, "model": config.AGENT_PRICE_KEY, "prompt": prompt}
    return run_gate("test_report.json", "eval_report.json", "cost_latency.json",
                    "signoff_report.md", meta)


def main():
    parser = argparse.ArgumentParser(description="TravelMind end-to-end QA pipeline")
    parser.add_argument("--offline", action="store_true",
                        help="use sample numbers for stages 2 and 3 (no AWS)")
    parser.add_argument("--build", default="travelmind-local")
    parser.add_argument("--prompt", default="v7")
    args = parser.parse_args()

    mode = "OFFLINE (sample eval/cost)" if args.offline else "ONLINE (real Bedrock)"
    print("=" * 64)
    print(f"TravelMind QA pipeline   build={args.build}   mode={mode}")
    print("=" * 64)

    # Run the four stages in order. Each writes its report for the next.
    stage_1_tests()
    stage_2_eval(args.offline)
    stage_3_observability(args.offline)
    passed = stage_4_gate(args.build, args.prompt)

    print("\n" + "=" * 64)
    print("RESULT:", "PROMOTE" if passed else "BLOCKED")
    print("Sign-off written to signoff_report.md")
    print("=" * 64)

    # The pipeline's own exit code mirrors the gate, so CI can branch on it.
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
