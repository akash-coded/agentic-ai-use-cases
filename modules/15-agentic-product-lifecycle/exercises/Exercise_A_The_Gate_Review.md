# Mid-session exercise A — The gate review

*Format: read the board, then decide · Time: 10 minutes · You are the reviewer · Answer in the chat*

## Recap

Before engineering builds, the P1 gate checks that the mandatory set is complete, every triggered conditional artefact is present, and each is signed off. A blank autonomy line or a bar with no sample size fails on sight.

**The gate is four checks:**

1. **Mandatory set complete?** all five produced and filled
2. **Conditional triggers covered?** every triggered artefact present
3. **Each artefact signed off?** one accountable name per row
4. **Anything that fails on sight?** a blank autonomy line, a bar with no sample

A fail names the one artefact to finish. It does not send the whole thing back.

## The situation

You chair the P1 gate for SkyWays. A product owner brings the **Auto-Refund agent**: when a booking is cancelled, it reads the booking, decides the refund the passenger is owed using a model, and issues it. It can refund up to $200 without a person. It never touches a partner airline. The PM says it is ready to build and wants your sign-off today.

Here is exactly what they produced. Read every row before you decide.

| Duty | Artefact | Status | What was produced |
|---|---|---|---|
| M | Problem brief | **DONE** | Reduce agent-handled refunds; 9,000/mo at $9 each |
| M | Agent spec | **PARTIAL** | Job, trigger, actions listed. Boundary field left blank |
| M | Autonomy line | **MISSING** | No level written for any action |
| M | Acceptance bar | **PARTIAL** | "90% accurate" written, no slice, no sample size |
| M | Tool contract | **DONE** | Refund tool: reads booking, issues refund, $200 cap, logs |
| C | Statistical acceptance plan | **MISSING** | Output is a model score, so this is triggered |
| C | Open-decisions log | **DONE** | One open item: partial-refund policy unconfirmed |
| C | Autonomy spec | **MISSING** | The agent acts on a model decision, so triggered |

## The questions

**A1. What is your gate decision?**

- a. Pass. The mandatory set is mostly there and the rest can follow during build
- b. Hold. Name the artefacts to finish first, then re-gate
- c. Reject and send the whole set back to be redone
- d. Pass on condition the PM verbally confirms the missing pieces

**A2. Which produced artefact fails the gate on sight, even though something was written?**

- e. The problem brief, because the numbers are rough
- f. The acceptance bar, because "90%" has no slice and no sample size
- g. The tool contract, because $200 is too low a cap
- h. The open-decisions log, because one item is still unconfirmed

**A3. The PM argues the missing autonomy line is "obvious, it just issues refunds." What do you tell them?**

- i. Agreed, it is obvious, waive that one
- j. The refund action is irreversible and moves money, so its level must be written, not assumed
- k. Autonomy lines are the architect's job, not theirs
- l. It only matters after launch, so it can wait for P2

**A4. Which two conditional artefacts are triggered here but missing? (pick two)**

- m. Statistical acceptance plan
- n. Registry entry
- o. Autonomy spec
- p. Rollback runbook

**How to answer.** Type all four with the letters you choose, for example `A1-a A2-e A3-i A4-mn`.
