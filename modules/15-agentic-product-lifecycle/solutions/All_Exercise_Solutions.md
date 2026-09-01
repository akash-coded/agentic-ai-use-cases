# Day 3 exercises — answer key

## For the trainer. Release after learners submit.

Each answer gives the key, the reasoning, and why the tempting wrong options fail. The teaching point of each exercise is named first, so you know what to reinforce when you reveal it.

---

## Exercise 1 — Which artefacts does this feature owe?

**Teaching point:** mandatory artefacts are owed by what the agent *is*; conditional ones by what it *does*. The autonomy spec is owed only when a model acts, not merely when the agent acts.

**Answer: a b c d e f i** owed, and **1k = c (L3).**

The seat-preference agent uses a model (it predicts) and it acts (it reserves a seat), and every action it takes is reversible and harmless.

| Artefact | Owed? | Why |
|---|---|---|
| a Problem brief | Yes | Mandatory. Every agent needs a reason it exists. |
| b Agent spec | Yes | Mandatory. |
| c Autonomy line | Yes | Mandatory. |
| d Acceptance bar | Yes | Mandatory. |
| e Tool contract | Yes | Mandatory. |
| f Statistical acceptance plan | Yes | It predicts, so the output is probabilistic. |
| g Open-decisions log | No | Nothing in the brief is unresolved. |
| h Registry entry | No | It runs alone; no other agents. |
| i Autonomy spec (detailed) | Yes | A model decides *and* it acts. Both are true, so it is owed. |
| j Rollback runbook | No | No high-impact action. Reserving a seat is reversible. |

**Why the ceiling is L3 (1k = c):** reserving a seat can be released, and no passenger is worse off if the guess is wrong, so both actions are reversible and harmless. Nothing pulls the ceiling down.

- 1k-a (L1) is wrong: nothing here is irreversible-and-harmful. Learners pick it if they assume "it acts automatically" means high autonomy, which is the exact confusion to correct.
- 1k-b (L2) is wrong: L2 is for an action that is irreversible but harmless, like the confirmation email in the deck. This agent has no such action.

**The common miss:** leaving off **i**. Many will stop at the five mandatory plus the statistical plan and forget the autonomy spec, because the agent's actions feel harmless. It still acts on a model's decision, so the spec is owed.

---

## Exercise 2 — Complete the decision tree

**Teaching point:** each conditional artefact is tied to one specific trigger. Reading the tree is matching a leaf to its condition, not guessing.

**Answer: 1-q  2-s  3-p.**

| Blank | Condition above it | Artefact |
|---|---|---|
| Blank 1 | agent ACTS | q. Autonomy spec |
| Blank 2 | output is PROBABILISTIC | s. Statistical acceptance plan |
| Blank 3 | decisions still OPEN | p. Open-decisions log |

**The distractors:**

- **t. Tool contract** is the trap. It is a real artefact, but it is *mandatory*, not conditional, so it never hangs off a trigger in this tree. Anyone who places it has confused a mandatory artefact for a conditional one, which is the distinction the whole session turns on.
- **r. Rollback runbook** is the unused bank option. It is optional and tied to high-impact actions, not to any of these three conditions.

---

## Exercise 3 — Spot the ceiling that is wrong

**Teaching point:** the ceiling is the *lowest* level any single action allows, not the most common. One irreversible-and-harmful action sets it for the whole agent.

**Answer: 3a = b (wrong), 3b = d.**

The paying-interim-expenses action is irreversible and hurts if wrong, which forces **L1, approve first**. The colleague wrote L2, most likely by taking the level that appears most often in the table rather than the lowest.

- **3b-c** (sending an update is irreversible) is true but not the reason. An update is irreversible *and harmless*, so it only forces L2, not L1. It is a real fact used as a wrong reason, which is the trap.
- **3b-e** (a policy lookup could be outdated) is a real risk but it is about accuracy, not autonomy. It does not change what an irreversible payment costs.
- **3b-f** (reading is the only safe action) is false. Reading and the policy lookup are both fully safe, so the statement is wrong on its face.

**The number to say out loud:** at L2 the payment runs unattended. One wrong payment is real money out the door and cannot be clawed back easily, which is exactly what approve-first prevents.

---

## Exercise 4 — The guardrail decision

**Teaching point:** a bar comes from the cost of a mistake, and a hold lowers the damage, which lowers the bar, which can make an already-built model shippable.

**Answer: 4a = c (86%), 4b = f (no), 4c = h (50%), 4d = k (yes).**

- **4a:** damage $48 divided by saving $8 is 6 rights per wrong. The bar is 1 minus 1 over 7, which is **85.7%, rounded to 86%.**
  - 4a-a (50%) is the bar when damage equals saving. Wrong scale.
  - 4a-b (80%) is the flight agent's bar from the deck ($32 damage). Learners pick it from memory instead of recomputing, which is the habit to break.
  - 4a-d (90%) is close but not what the arithmetic gives.
- **4b:** 82% measured is below the 86% bar, so **no, it does not clear.**
- **4c:** with a hold, a wrong answer costs only the $8 of wasted handling. Damage $8 divided by saving $8 is 1 right per wrong, and the bar is 1 minus one-half, which is **50%.**
  - The other options are there because learners sometimes halve the original bar (43%) or guess a round number.
- **4d:** 82% measured clears the 50% bar easily, so **yes, the hold made it shippable.**

**The whole point in one line:** the model did not get better between 4b and 4d. The hold lowered the damage, the bar dropped from 86% to 50%, and the same 82% model went from unshippable to shippable. That is the guardrail lesson made concrete.

---

## Exercise 5 — Match the feature to its build

**Teaching point:** most of a backlog is not agentic. Naming the build for each feature is what takes rules out of the AI conversation.

**Answer: 1-w  2-x  3-w  4-y.**

| Feature | Build | Why |
|---|---|---|
| 1. Notify on a gate change | w. Rule / workflow | A fixed trigger fires a message. No model, no decision. |
| 2. Choose the best rebooking option | x. Assisted | A model ranks the options; a person picks. |
| 3. Refund inside a fixed policy | w. Rule / workflow | Fixed rules, deterministic. No judgement. |
| 4. Rebook a multi-leg trip across partners | y. Agentic | A model decides across several tools end to end. |

**The point to land:** two of the four features (1 and 3) need no model at all. In a real backlog that share is often higher than the room expects, and those rows leave the agentic work entirely. That is the most useful thing a PM can do with this framework: shrink the list of things that actually need an agent.

---

## Running the set

Any two of these fit a mid-session break. Suggested pairing by what you want to reinforce:

- To drill the **artefact set**, run Exercises 1 and 2.
- To drill **autonomy and the bar**, run Exercises 3 and 4.
- Exercise 5 is the fastest and works as a warm-up or a closer.

Collect answers as letter strings in the chat, then reveal one row at a time. The disagreement to look for is on 1k, 3b and 4a, where the tempting wrong answer is a real fact used for the wrong reason. That disagreement is the discussion.
