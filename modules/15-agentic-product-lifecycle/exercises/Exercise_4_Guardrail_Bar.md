# Exercise 4 — The guardrail decision

*Format: single-select chain · Time: 7 minutes · Answer in the chat*

## Recap

The acceptance bar comes from what a wrong answer costs. A hold on the risky action lowers the damage, which lowers the bar, which can make an already-built model shippable.

```
rights per wrong  =  cost of wrong  /  saving of right
bar  =  1  -  1 / (rights per wrong + 1)
```

## The codeshare-rebooking agent

> A model decides routes across partner airlines.
> **One right answer saves $8** of handling.
> **One wrong answer costs $48**: a wrong reissue, a refund, and a service credit.
> The team measures the model at **82% correct** on the codeshare slice.

## The exercise

**4a. What acceptance bar does this agent have to clear?**

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

**How to answer.** Type all four, for example `4a-c 4b-f 4c-h 4d-k`.
