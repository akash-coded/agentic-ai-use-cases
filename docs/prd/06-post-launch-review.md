# 06 · Post-Launch Review — TravelMind

> Thirty days after release. Written to be uncomfortable — a review that finds nothing wrong found nothing.

**Status:** template with worked examples · **Owner:** everyone who signed off

## 1. What we predicted vs what happened

| Metric | Predicted | Actual | Gap |
| --- | --- | --- | --- |
| Autonomous resolution | 60% | | |
| Cost per resolved enquiry | < $0.04 | | |
| p95 latency | < 6 s | | |
| Policy-contradicting answers | 0 | | |
| Abstention rate | not predicted | | ← predict it next time |

Abstention rate was not in the original PRD. It should have been: an agent that abstains on 40% of
enquiries technically meets a 60% resolution target while being much less useful than intended.

## 2. What the golden set missed

Production surfaces cases a 130-case set cannot. List every production failure with no golden-set analogue,
and add it:

| Production failure | Why the golden set missed it | Added as case |
| --- | --- | --- |
| | | |

This table is the main output of the review. The golden set is a living artefact.

## 3. Decisions that turned out wrong

Be specific. "Reranking was worth it" is a finding. "The architecture was fine" is not.

| Decision | Made in | What we know now |
| --- | --- | --- |
| | [Technical design](03-technical-design.md) | |

## 4. What we would tell ourselves at Gate 1

The most valuable section. One or two sentences that would have changed the build.

## 5. Cost reality

| Driver | Predicted share | Actual share | Note |
| --- | --- | --- | --- |
| Tokens per turn | | | |
| Turns per enquiry | | | |
| Retrieval | | | |
| Runtime + memory | | | |

Cost surprises are almost always in *turns per enquiry*, not tokens per turn. Topology is the expensive
decision.

## 6. Actions

| Action | Owner | Due | Artefact it changes |
| --- | --- | --- | --- |
| | | | |

---

**Feeds back into:** [idea brief](00-idea-brief.md) for the next increment ·
[evaluation plan](04-evaluation-plan.md) for the expanded golden set
