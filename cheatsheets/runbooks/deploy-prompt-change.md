# Runbook · Shipping a prompt change

**Why this needs a runbook:** a prompt change is a behaviour change with no compiler, no type check and no
stack trace. It is the most ungoverned change in most agent systems.

---

## The rule

> **A prompt change is a code change.** Same review, same versioning, same evaluation, same rollback path.

## Before

- [ ] Golden set run **on the current prompt**, numbers recorded (this is your baseline)
- [ ] The change is **one thing**. Bundled prompt changes cannot be bisected
- [ ] You can state what behaviour should change, and what should not

## The change

- [ ] Prompt lives in a version-controlled file, not embedded in a framework object
- [ ] Diff is reviewed by someone who did not write it
- [ ] **Check for contradiction** with existing rules — the model picks one, unpredictably
- [ ] Prompt version bumped in the [manifest](../../modules/14-end-to-end-production/src/version_manifest.json)

## After — run the golden set and compare five things

| Metric | Watch for |
| --- | --- |
| Pass rate | The obvious one |
| **Abstention rate** | A **drop** usually means bolder, not better |
| **Safety slice** | Must stay at 1.0. No exceptions |
| **Output tokens per turn** | A rise is [reasoning blow-up](../frameworks/cost-cliff-map.md) — a cost cliff |
| **Turns per task** | A rise multiplies four taxes |

> Rows 2 and 4 are the ones people skip, and they are where prompt regressions actually live. A prompt
> change that improves pass rate by 2 points while dropping abstention by 15 points has made the system
> worse, not better.

## The forbidden move

> **Never edit the prompt to make a failing golden-set case pass, in the same change that discovers it.**

That is editing the test. If a case is genuinely wrong, fix the case in its own commit, reviewed
separately, with the reason recorded.

## Rollout

| Stage | Gate |
| --- | --- |
| Local | Golden set passes; five metrics compared |
| Shadow | Real traffic, output not shown to users |
| Canary | Small share of live traffic; watch abstention and cost |
| Full | All five metrics within tolerance for 24h |

For a low-risk wording change, local + full is defensible. For anything touching abstention, evidence
rules or tool selection, do not skip shadow.

## Rollback

Because the prompt is versioned in the manifest, rollback is a manifest change, not a rebuild. If it is
not — see [reversibility](../frameworks/reversibility-test.md) — fix that before shipping anything else.

## After 24 hours

- [ ] Abstention rate stable
- [ ] Cost per task stable
- [ ] No new failure signatures in logs
- [ ] Baseline numbers updated for the next change

**Related:** [Prompting for agents](../quick-reference/prompt-engineering-for-agents.md) ·
[Evidence Ladder](../frameworks/evidence-ladder.md)
