# How to · Validate an LLM judge before you trust it

**Time:** half a day. **The problem:** an unvalidated judge is a measurement instrument nobody calibrated,
and every number downstream inherits its error.

---

## 1. Why this matters more than it seems

If your judge has 80% agreement with human labels, then a reported "90% pass rate" could be anywhere in a
wide band. You are not measuring the agent; you are measuring the agent through an unknown lens.

Worse, judges have **systematic** biases, not random noise — they tend to prefer longer answers, answers
that echo the question, and answers that sound confident. Those biases align exactly with the failure mode
you are trying to catch.

## 2. Build the calibration set

Take **100 agent outputs** spanning the quality range — not just good and terrible, but the ambiguous
middle where judges actually fail.

| Slice | Count |
| --- | --- |
| Clearly correct | 25 |
| Clearly wrong | 25 |
| **Borderline** | 30 |
| Correct abstentions | 10 |
| Confident-wrong (fluent, plausible, false) | 10 |

The last two slices are where judges fail hardest, and they are the two most teams omit.

## 3. Get human labels — from two people

Two independent labellers. Measure their agreement first:

```
human_agreement = matching_labels / total
```

If humans agree less than ~85%, your **rubric** is the problem, not the judge. Fix the rubric before
touching the judge — you cannot ask a model to be more consistent than your definition of correct.

Where they disagree, that case is genuinely ambiguous. Those cases belong in the abstention slice of your
golden set.

## 4. Measure the judge against the humans

```python
from collections import Counter

def evaluate_judge(cases, human, judge):
    m = Counter()
    for c in cases:
        h, j = human[c["id"]], judge[c["id"]]
        m["agree" if h == j else "disagree"] += 1
        if h == "fail" and j == "pass": m["false_pass"] += 1   # the dangerous one
        if h == "pass" and j == "fail": m["false_fail"] += 1
    n = len(cases)
    return {"agreement": m["agree"] / n,
            "false_pass_rate": m["false_pass"] / n,
            "false_fail_rate": m["false_fail"] / n}
```

| Metric | Bar | Why |
| --- | --- | --- |
| Agreement | ≥ 85% | Below this the judge is noise |
| **False-pass rate** | ≤ 5% | The judge waving through a bad answer |
| False-fail rate | ≤ 10% | Annoying, not dangerous |

**False-pass is the one that matters.** A judge that is generous is worse than no judge, because it
manufactures confidence.

## 5. Fix a judge that disagrees

| Symptom | Fix |
| --- | --- |
| Generous on fluent-but-wrong answers | Require it to quote the supporting passage before deciding |
| Inconsistent on borderline cases | Sharpen the rubric; add explicit examples of both sides |
| Prefers longer answers | Score against the rubric only; strip length cues |
| Cannot judge abstention | Add abstention as an explicit rubric category |

The single most effective change is usually forcing the judge to **cite its evidence before judging**,
which is the same fix as for the agent itself.

## 6. Re-validate on every change

A judge is a dependency:

- [ ] Judge model changed → re-validate
- [ ] Judge prompt changed → re-validate
- [ ] Rubric changed → re-validate humans first, then the judge
- [ ] Quarterly, regardless

## 7. Report honestly

```
Pass rate: 87% (LLM judge, agreement 0.91 with human labels on a 100-case
calibration set, false-pass rate 0.03, last validated 2026-07-14)
```

That parenthetical is what makes the 87% a real number rather than a hopeful one.

## The checklist

- [ ] 100-case calibration set, including borderline and confident-wrong
- [ ] Two human labellers; inter-human agreement measured first
- [ ] Judge agreement ≥85%, false-pass ≤5%
- [ ] Judge required to cite evidence before deciding
- [ ] Re-validation triggers written down
- [ ] Judge quality quoted alongside every number it produces

**Related:** [Evidence Ladder](../../frameworks/evidence-ladder.md) ·
[Grounding Triangle](../../frameworks/grounding-triangle.md) ·
[QA interview guide](../../interviews/qa-engineer.md)
