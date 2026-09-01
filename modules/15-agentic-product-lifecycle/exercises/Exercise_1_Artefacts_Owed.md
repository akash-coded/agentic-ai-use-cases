# Exercise 1 — Which artefacts does this feature owe?

*Format: multi-select · Time: 6 minutes · Answer in the chat, no writing*

## Recap

Every P1 artefact has one of three duties. You owe the five mandatory ones for every agent. You owe a conditional one only when its condition is true. You rarely owe the optional ones.

| Duty | Owed when | Examples |
|---|---|---|
| **Mandatory** | by what the agent IS | problem brief, agent spec, autonomy line, acceptance bar, tool contract |
| **Conditional** | a condition is TRUE | it acts, output is probabilistic, decisions open, runs with other agents |
| **Optional** | rarely | only if an action is high-impact |

## The feature

> **Seat-preference agent.** When a booking is confirmed, the agent reads the passenger's past bookings, predicts the seat they are likely to want, and reserves it automatically. If the flight is full in that cabin it does nothing. It never charges anything and never contacts another airline.

## The exercise

Work it through the sheet. Type the letters of every artefact this feature **owes**.

| | Artefact | | Artefact |
|---|---|---|---|
| a | Problem brief | f | Statistical acceptance plan |
| b | Agent spec | g | Open-decisions log |
| c | Autonomy line | h | Agent registry entry |
| d | Acceptance bar | i | Autonomy spec (detailed) |
| e | Tool contract | j | Rollback runbook |

**1k. What is this agent's autonomy ceiling?**

- a. L1, approve first
- b. L2, act and tell
- c. L3, act alone

**How to answer.** Type the owed letters plus your ceiling, for example `a b c f 1k-c`.
