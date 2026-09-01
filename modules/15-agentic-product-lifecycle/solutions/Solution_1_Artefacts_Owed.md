# Exercise 1 solution — Which artefacts does this feature owe?

**Seat-preference agent** on SkyWays Booking.

## Answer

**Owed: a b c d e f i.** Ceiling **1k = c, L3 act alone.**

## Teaching point

Mandatory artefacts are owed by what the agent *is*. Conditional ones by what it *does*. The autonomy spec is owed only when a model acts, not merely when the agent acts.

## How you decide, for any artefact

| Question | If yes | Meaning |
|---|---|---|
| Owed by what the agent IS? | MANDATORY | always owe it |
| Triggered by a named condition? | CONDITIONAL | owe it when the condition is true |
| Neither | OPTIONAL | rarely owe it |

## The seat agent, artefact by artefact

| Artefact | Duty | Owed? | Why |
|---|---|---|---|
| a Problem brief | Mandatory | OWED | every agent needs a reason |
| b Agent spec | Mandatory | OWED | the buildable description |
| c Autonomy line | Mandatory | OWED | how much it decides alone |
| d Acceptance bar | Mandatory | OWED | the number it must hit |
| e Tool contract | Mandatory | OWED | what it may touch |
| f Statistical acceptance plan | Conditional | OWED | it predicts, so output is probabilistic |
| i Autonomy spec (detailed) | Conditional | OWED | a model decides AND it acts |
| g Open-decisions log | Conditional | skip | nothing unresolved |
| h Agent registry entry | Conditional | skip | it runs alone |
| j Rollback runbook | Optional | skip | no high-impact action |

## Why L1 and L2 are wrong for 1k

L1 needs an action that is irreversible and harmful; this agent has none. L2 needs one that is irreversible but harmless, like the confirmation email in the deck; again none. Reserving a seat can be released and hurts nobody, so nothing pulls the ceiling below L3.

## The common miss

Leaving off **i, the autonomy spec.** Many stop at the five mandatory plus the statistical plan because the actions feel harmless. It still acts on a model's decision, so the spec is owed.
