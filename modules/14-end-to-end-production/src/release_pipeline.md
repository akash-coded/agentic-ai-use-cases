# Release Pipeline: Versioning, Rollout, Rollback

A deployed agent is not done. This is how you make every change safe to ship and
instant to undo. Pair this with `release.py` (runs the whole loop offline) and
`version_manifest.json` (the artifact it reads and writes).

The frame: treat the agent as deployable software, but software whose output is
non-deterministic. The pipeline mirrors CI/CD with one addition, an evaluation
gate, because a prompt edit has no compiler to catch it.

---

## 1. One release = three pinned things

Behavior is a function of prompt + agent config + model. Pin one and miss the
others and you cannot reproduce a result. So they version as one unit.

```json
{
  "release": "travelmind-2026.06.12-rc1",
  "prompt_version": "v6",
  "prompt_sha": "a91f3c7e",
  "model_id": "us.anthropic.claude-haiku-4-5-20251001-v1:0",
  "agent_config": { "temperature": 0.2, "max_tokens": 1024 },
  "gate": { "status": "passed", "eval_pass_rate": 0.94 },
  "rollback_target": "travelmind-2026.06.11-rc3"
}
```

Two habits make this work:

| Habit | Why |
|---|---|
| `prompt_sha` on every release | a prompt change shows up in a diff, like code |
| prompt logic outside app code | a prompt bump is a data change with its own version, not a redeploy |

---

## 2. Promote through environments, never straight to prod

| Environment | What it is |
|---|---|
| local | your machine; fast loop, mocked or real model, no users |
| staging | deployed like prod, internal traffic only; the gate runs here first |
| prod | real users, behind canary and rollback; changes arrive gated |

The same versioned artifact moves rightward unchanged. You promote a build, you
do not rebuild it per environment. Each arrow is a gate.

---

## 3. Roll out in stages

| Phase | What happens | Why |
|---|---|---|
| shadow | new version runs on copies of live traffic, output discarded | compare with zero user risk |
| canary | 5 to 10% of real traffic goes to the new version | real signal, small blast radius |
| progressive | widen 5% then 25% then 100% as gates keep passing | earn each increase |

A concrete schedule used in production: canary 5% for 6 hours, then 25% for 24
hours, then 100%, and monitor 48 hours before marking it stable and updating the
rollback target. A second model grades canary responses against a rubric, so
promotion needs no human at off-hours.

**Feature flags** decouple deployment from activation: deploy the new prompt
dark, then turn it on for a slice. Shipping the code and exposing it become two
separate, reversible decisions.

---

## 4. Rollback is a redirect, not a redeploy

One rule makes rollback fast: deployed versions are never destroyed. The
previous build stays live and addressable.

Rolling back means redirecting traffic to the release named in
`rollback_target`. No rebuild, no debugging, seconds not a hotfix cycle.

The dividend: the failing version and the exact production inputs that exposed
it become new test cases. The incident permanently hardens your golden set.

---

## 5. The gate is the promotion check

The gate you built in Session 1 (`quality_gate.py`) becomes the thing standing
between staging and prod, and between each canary step.

| Gate | Threshold | Source |
|---|---|---|
| eval pass rate | at least 90% | golden set, substring + judge |
| cost per resolution | at most $0.02 | tokens times price |
| p95 latency | at most 4000 ms | traces |
| safety / PII | 100% | no leak, no invented PNR or flight |

On every promotion: pass widens traffic and tags the release; fail stops the
rollout and redirects to `rollback_target`. Merges are blocked when quality
falls below threshold, which is what prevents a silent regression from reaching
users.

---

## Worked example: run it yourself (offline)

`release.py` models this loop with a tiny golden set and a simulated prompt, so
you can watch a bad change get blocked and a fix get promoted. No AWS needed.

```bash
python release.py --show
python release.py --set-prompt v7      # the "answer concisely" change
python release.py --gate               # FAILS: it silently dropped rebooking options
python release.py --set-prompt v7.1    # restore the options, stay concise
python release.py --gate               # PASSES -> canary 10%
python release.py --promote            # canary -> progressive
python release.py --rollback           # redirect to the safe version, instant
```

What it proves: the gate caught the regression before any user saw it; the fix
was a prompt edit re-gated, not a redeploy; rollback was one command to the
named target. The same `test_report.json`, `eval_report.json`, and
`cost_latency.json` from Session 1 feed the real gate.

---

## What to avoid

| Anti-pattern | Why it bites, and the fix |
|---|---|
| canary with no eval gate | latency and errors stay green while quality drops; gate on eval too |
| no named rollback target | if you cannot say which version is good, you cannot roll back fast |
| prompt logic inside app code | a prompt change becomes a slow, risky code deploy; externalize prompts |
| deploy equals activate | shipping and exposing in one step removes your safety valve; use feature flags |
| one-and-done canary check | quality drifts over hours; hold the canary 24 to 48 hours with automated gates |

The goal is not zero change. It is change you can make at noon and undo by 12:05
without paging anyone.
