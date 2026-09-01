# Mid-session exercises — the agentic artefact set

## The Agentic Artefact Set

Four short exercises. Each takes five to seven minutes. You choose options and type a short answer into the chat. Nothing to write out.

The running product is **SkyWays Booking**, the same one from the session. Everything you need is on the slides you have already seen.

How to answer: type your letters as one line, for example `1b 2d 3a`. Where an exercise asks for a set, type all the letters that apply.

---

## Exercise 1 — Which artefacts does this feature owe?

**Format: multi-select. Time: 6 minutes.**

A new feature lands on the SkyWays backlog.

> **Seat-preference agent.** When a booking is confirmed, the agent reads the passenger's past bookings, predicts the seat they are likely to want, and reserves it automatically. If the flight is full in that cabin it does nothing. It never charges anything and never contacts another airline.

Work it through the artefact sheet. Below are the ten artefacts. Type the letters of every artefact this feature **owes**.

| | Artefact | | Artefact |
|---|---|---|---|
| a | Problem brief | f | Statistical acceptance plan |
| b | Agent spec | g | Open-decisions log |
| c | Autonomy line | h | Agent registry entry |
| d | Acceptance bar | i | Autonomy spec (detailed) |
| e | Tool contract | j | Rollback runbook |

Then answer one more, single-select:

**1k. What is this agent's autonomy ceiling?**

- a. L1, approve first
- b. L2, act and tell
- c. L3, act alone

---

## Exercise 2 — Complete the decision tree

**Format: fill the branches. Time: 5 minutes.**

Here is the conditional-artefact decision tree with three of its four leaves blanked out. Each blank is a `?`. Match each blank to the right artefact from the bank.

```
                          A CONDITIONAL ARTEFACT
                                   |
        +----------------+----------+----------+----------------+
        |                |                     |                |
   agent ACTS?     output is            decisions           runs with
        |          PROBABILISTIC?        still OPEN?       OTHER agents?
        |                |                     |                |
       yes              yes                   yes              yes
        |                |                     |                |
   [ ? BLANK 1 ]    [ ? BLANK 2 ]       [ ? BLANK 3 ]     Registry entry
```

**The bank:**

- p. Open-decisions log
- q. Autonomy spec
- r. Rollback runbook
- s. Statistical acceptance plan
- t. Tool contract

Type your matches as `1-? 2-? 3-?`, for example `1-p 2-q 3-s`.

One of the bank options is a distractor that fits no blank. You do not have to name it, but you should not use it.

---

## Exercise 3 — Spot the ceiling that is wrong

**Format: single-select plus a follow-up. Time: 6 minutes.**

A colleague scored the actions for a **baggage-claim agent** and wrote its ceiling underneath. Read the table.

| The action | Reversible? | Hurts if wrong? | Level it allows |
|---|---|---|---|
| Read the baggage record | Yes | No | L3 |
| Look up the compensation policy | Yes | No | L3 |
| Send the passenger an update | No | No | L2 |
| Pay interim expenses to the passenger's card | No | Yes | L1 |
| **Their written ceiling** | | | **L2 act and tell** |

**3a. Is the ceiling correct?**

- a. Correct
- b. Wrong

**3b. If it is wrong, which single fact makes it wrong?**

- c. Sending an update cannot be taken back
- d. Paying interim expenses is irreversible and hurts if wrong
- e. Looking up a policy could return an outdated policy
- f. Reading the record is the only fully safe action

Type your answer as `3a-? 3b-?`.

---

## Exercise 4 — The guardrail decision

**Format: single-select chain. Time: 7 minutes.**

The **codeshare-rebooking agent** decides routes across partner airlines. Here are its numbers.

- One right answer saves **$8** of handling.
- One wrong answer costs **$48**: a wrong reissue, a refund, and a service credit.
- The team measures the model at **82% correct** on the codeshare slice.

**4a. What acceptance bar does this agent have to clear?**

Use the 1-in-N idea: rights per wrong is damage divided by saving, and the bar is one minus one over that plus one.

- a. 50%
- b. 80%
- c. 86%
- d. 90%

**4b. At 82% measured, does it clear the bar?**

- e. Yes, ship it
- f. No, it is below the bar

**4c. The team adds a hold: a person approves any codeshare reissue before it is charged. A wrong answer now costs only the $8 of wasted handling. What is the new bar?**

- g. 40%
- h. 50%
- i. 60%
- j. 75%

**4d. At 82% measured, does it clear the new bar?**

- k. Yes, the hold made it shippable
- l. No, it is still below

Type your answer as `4a-? 4b-? 4c-? 4d-?`.

---

## Exercise 5 — Match the feature to its build (bonus, if time)

**Format: matching. Time: 5 minutes.**

Match each SkyWays feature on the left to the build it needs on the right. Each build is used at least once.

**Features:**

1. Notify a passenger when their gate changes
2. Choose the best of several rebooking options for a delayed flight
3. Refund a cancelled booking inside a fixed policy, no judgement
4. Rebook a multi-leg international trip across partner airlines end to end

**Builds:**

- w. Rule or workflow (no model)
- x. Assisted (model suggests, person decides)
- y. Agentic (model decides across tools)

Type your matches as `1-? 2-? 3-? 4-?`.

---

*Answers are released after you have submitted. Type your letters in the chat.*
