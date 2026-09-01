# Exercise 3 solution — Spot the ceiling that is wrong

**Baggage-claim agent.**

## Answer

**3a = b, the ceiling is wrong.**  **3b = d**, paying interim expenses is irreversible and hurts, which forces L1.

## Teaching point

The ceiling is the *lowest* level any single action allows, not the most common. One irreversible-and-harmful action sets it for the whole agent.

## The action ladder

| The action | Reversible? | Hurts? | Level it allows |
|---|---|---|---|
| Read the baggage record | Yes | No | L3 |
| Look up the compensation policy | Yes | No | L3 |
| Send the passenger an update | No | No | L2 |
| Pay interim expenses to the card | No | Yes | **L1** |

The lowest row is L1, so the agent's ceiling is **L1 approve first**. The written L2 took the most common level, not the lowest.

## Why the other reasons fail

- **c** (an update cannot be taken back) is true but not the reason. An update is irreversible *and harmless*, so it only forces L2, not L1. A real fact used as a wrong reason.
- **e** (a policy lookup could be outdated) is about accuracy, not autonomy. It does not change what an irreversible payment costs.
- **f** (reading is the only safe action) is false. Reading and the policy lookup are both fully safe.

## The number to say out loud

At L2 the payment runs unattended. One wrong payment is real money out the door and hard to claw back, which is exactly what approve-first prevents.
