# Exercise 4 solution — The guardrail decision

**Codeshare-rebooking agent.**

## Answer

**4a = c (86%)**  ·  **4b = f** below the bar  ·  **4c = h (50%)**  ·  **4d = k** now it ships.

## Teaching point

A bar comes from the cost of a mistake. A hold lowers the damage, which lowers the bar, which can make an already-built model shippable.

## The arithmetic

| | Damage | Saving | Rights per wrong | Bar = 1 − 1/(n+1) | 82% vs bar |
|---|---|---|---|---|---|
| No hold | $48 | $8 | 6 | **85.7% ≈ 86%** | below |
| With a hold | $8 | $8 | 1 | **50%** | clears |

## Why 80% (4a-b) is the tempting wrong answer

It is the flight agent's bar from the deck, where the damage was $32. Learners recall it instead of recomputing for $48 damage. The habit to break is answering from memory when the numbers changed.

## The whole point in one line

The model did not improve between 4b and 4d. The hold lowered the damage, the bar dropped from 86% to 50%, and the same 82% model went from unshippable to shippable.
