# The Reversibility Test (the U-Turn Test)

> **One line:** before an agent may act, you must be able to say who undoes it, how, and how fast.

Reversibility is decided at design time and discovered at 2 a.m. This test moves the discovery forward.

---

## The four questions

For every action an agent can take, answer all four. Any unanswered question is a blocker.

| # | Question | Bad answer | Good answer |
| --- | --- | --- | --- |
| 1 | **Who can undo it?** | "We'd have to ask someone" | "The on-call engineer, alone" |
| 2 | **How long does undoing take?** | "Depends" | "Under 5 minutes, one command" |
| 3 | **What is lost even after undoing?** | "Nothing?" | "The customer saw the email. Trust cost is real." |
| 4 | **Has the undo been rehearsed?** | "It should work" | "Yes, on the 14th. Took 3 minutes." |

Question 4 is the one that matters. An untested rollback is a plan, not a capability.

## The reversibility tiers

| Tier | Undo | Example | Agent may act |
| --- | --- | --- | --- |
| **T0 — Free** | Nothing to undo | Read, search, draft | ✅ Autonomously |
| **T1 — Automatic** | System reverts itself | Cache write, scratch state | ✅ Autonomously |
| **T2 — One command** | Engineer runs one thing | Deploy rollback, feature flag | ✅ With alerting |
| **T3 — Coordinated** | Multiple systems or people | Data correction across services | ⚠️ Human commits |
| **T4 — Irreversible** | Cannot be undone | Money sent, email delivered, data destroyed | 🔴 Human commits, always |

Note that T4 includes anything a **human has seen**. You cannot un-send information. An agent that
autonomously emails a customer is operating at T4 regardless of what your database can roll back.

## Deploy-level reversibility

The same test applies to the release, not just to individual actions.

| Element | Reversible? | How |
| --- | --- | --- |
| Code | ✅ | Redeploy previous image digest |
| Prompt | ⚠️ **Only if versioned** | Prompt version in the manifest |
| Model choice | ⚠️ Only if pinned | Model id in the manifest |
| Retrieval index | 🔴 Often not | Snapshot before re-ingestion |
| Memory contents | 🔴 Usually not | Retention policy, scoped writes |

> **The most common gap:** code is versioned, prompts are not. A prompt change ships, quality drops, and
> there is no artefact to roll back to — only a git diff someone has to interpret under pressure.
> **Version prompts like code, in the manifest.**

## The rehearsal

Once per release cycle, in a non-production environment:

1. Deploy a version
2. Deploy a second version
3. Roll back to the first **using only the manifest**, without rebuilding
4. Time it
5. Write the time down

If step 3 requires a rebuild, you do not have rollback. You have redeployment, which takes as long as a
deploy and is not available during an incident.

## The one-line rule

> **An agent may take an action autonomously only if the undo is T2 or better, and the undo has been
> rehearsed within the last release cycle.**

Everything else goes through a human.

## Where this shows up

- [Module 14](../../modules/14-end-to-end-production/) — version manifest, release pipeline, rollback
- [Production readiness PRD](../../docs/prd/05-production-readiness.md) — "rollback rehearsed, not assumed"
- [Rollback runbook](../runbooks/rollback.md)

**Related:** [Blast Radius Grid](blast-radius-grid.md) · [Demo-to-Production Gap](demo-to-production-gap.md) ·
[Tool Surface Audit](tool-surface-audit.md)
