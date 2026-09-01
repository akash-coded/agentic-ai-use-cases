# EVAL-03 · Solution

## Absolutes are not strict averages

The reflex is to treat `min_safety_rate = 1.0` as just a demanding average. It is a different kind of
number, and conflating them produces the failure in the Break phase.

An average says: *some failures are acceptable, and here is how many.* A pass rate of 0.85 is an explicit
statement that roughly one in seven answers may be wrong, and that this is fine for the job.

An absolute says: *this failure is never acceptable.* Not rare — never. A policy-contradicting answer that
reaches an ops agent is a defect regardless of how good the other 129 cases were.

Once you see them as different types, the ordering falls out. A build that is 0.99 on everything and 0.995
on safety is not "nearly perfect". It is blocked, and the safety line is the first thing the CI log should
show.

## Missing is not passing

```python
actual = reports.get("evals", {}).get("safety_pass_rate", 1.0)   # the bug
```

That default looks defensive and is the opposite. When the eval stage crashes, its report is absent, every
metric silently reads as perfect, and the gate promotes a build nobody measured. The stage failed loudly
and the gate converted it into a pass.

An absent number is not a met bar. It is an unmeasured bar, which is a block.

## Report every breach

Stopping at the first breach means each CI run reveals one problem. Three problems become three round
trips through the pipeline, and the third one is found an hour later. Evaluate everything, report
everything, sort by severity.

## Why it must never raise

The last Break check is the least obvious and the most practical. A gate that raises on malformed input
produces an ambiguous CI failure — did the build fail, or did the gate? The usual next move is a rerun,
and the one after that is `continue-on-error: true`.

The gate's contract is that it always returns a decision. Garbage in means `block`, with a reason. That is
the answer that is both safe and unambiguous.

## The governance point that outlives the code

The thresholds live in a reviewed file. Changing one is a commit, reviewed by someone who did not write
it, and **never in the same commit as the code it would let through**.

Without that rule, the gate degrades into a formality within a quarter: the first time a bar blocks an
urgent release, someone edits the bar. The code in this lab cannot prevent that. The convention can.

## Field guide

[Evidence Ladder](../../../../cheatsheets/frameworks/evidence-ladder.md) ·
[Build a quality gate](../../../../cheatsheets/how-to/engineers/build-a-quality-gate.md) ·
[`quality_gate.py`](../../../../modules/13-agentic-qa-and-evaluation/src/quality_gate.py) — the real one
