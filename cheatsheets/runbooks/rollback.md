# Runbook · Rolling back

**The test of a rollback plan is whether it has been rehearsed.** An untested rollback is a hope.

---

## Decide fast

Roll back **first**, diagnose **after**, when any of these hold:

- Wrong answers are reaching customers or staff
- A safety-slice failure has occurred, at all
- Cost per task has jumped sharply with no traffic change
- You do not yet know what is wrong

> Diagnosis is cheaper after the bleeding stops. Rolling back is not an admission of failure; failing to
> roll back for two hours while you theorise is.

## Rollback criteria — agreed before release

These belong in the [production readiness artefact](../../docs/prd/05-production-readiness.md), decided in
advance, because nobody makes this call well at 2 a.m.

| Trigger | Threshold |
| --- | --- |
| Policy-contradicting answer reaches a user | Any |
| Autonomous resolution rate | Below X% over a rolling day |
| Cost per task | Above $Y |
| p95 latency | Above Z ms |
| Safety slice | Any failure |

## The four things that must roll back together

| Element | Rolls back via | Common gap |
| --- | --- | --- |
| Code | Previous image digest | Usually fine |
| **Prompt** | Prompt version in the manifest | **Usually not versioned — the classic gap** |
| **Model** | Model ID in the manifest | Unpinned model changes under you |
| Config | Thresholds, top-k, caps | Often only in environment variables |

Rolling back code while leaving a new prompt live is a *different* configuration from either release. You
are now debugging a state that was never tested.

## The procedure

```bash
# 1. what is deployed now
cat version_manifest.json

# 2. what was deployed before
git log --oneline -- version_manifest.json | head -5
git show <previous>:version_manifest.json

# 3. deploy the previous manifest — no rebuild
python release.py --manifest previous_manifest.json --deploy

# 4. verify all four elements
#    code digest · prompt version · model id · config
```

See [`release.py`](../../modules/14-end-to-end-production/src/release.py) and
[`version_manifest.json`](../../modules/14-end-to-end-production/src/version_manifest.json).

## Verify the rollback actually took

- [ ] Version endpoint reports the previous version
- [ ] `model_id` in responses is the previous model
- [ ] Prompt hash matches the previous version
- [ ] Run five golden-set cases live and confirm expected behaviour
- [ ] Confirm the failing symptom is gone

Step 3 is the one people skip, and it is where the incomplete rollbacks are found.

## What rollback does not undo

| Already happened | Undone by rollback? |
| --- | --- |
| Answers already delivered | ❌ Never |
| Emails already sent | ❌ Never |
| Records already written | ⚠️ Only with a separate data fix |
| Memory written during the bad window | ⚠️ Consider scoped purge |
| Trust | ❌ |

This is exactly why the [Blast Radius Grid](../frameworks/blast-radius-grid.md) matters: an agent confined
to green-zone tools has very little that rollback cannot reach.

## The rehearsal — do this every release cycle

1. Deploy version A
2. Deploy version B
3. Roll back to A **using only the manifest**, without rebuilding
4. Time it
5. Write the time down

If step 3 requires a rebuild, you do not have rollback — you have redeployment, and it is not available
under incident pressure.

## After

- [ ] Root cause found before rolling forward again
- [ ] Failing case added to the golden set
- [ ] Gate updated so it would have caught this
- [ ] Rollback time recorded

**Related:** [Reversibility Test](../frameworks/reversibility-test.md) ·
[Module 14](../../modules/14-end-to-end-production/)
