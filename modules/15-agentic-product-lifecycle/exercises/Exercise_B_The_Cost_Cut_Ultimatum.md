# Mid-session exercise B — The cost-cut ultimatum

*Format: work the numbers, then choose · Time: 10 minutes · Answer in the chat*

## Recap

The acceptance bar comes from what a wrong answer costs, per slice. When a model is below the bar, you have three moves: improve the model (slow), lower the damage with a hold (this week), or narrow the scope and ship the slices that already clear their bar.

```
rights per wrong  =  cost of a wrong answer  /  saving of a right answer
the bar  =  1  -  1 / (rights per wrong + 1)
```

**The three slices, measured:**

| Slice | Accuracy | Cases |
|---|---|---|
| Same route | 96% correct | 5,400 |
| Reprice | 89% correct | 2,700 |
| Codeshare | 71% correct | 900 |

## The situation

The **codeshare-rebooking agent** is built. It reissues tickets across partner airlines. One right answer saves **$8** of handling; one wrong answer costs **$32** (a wrong reissue, a refund, a service credit). The model measures at **84% overall** across the three slices above. Engineering says it is not accurate enough and wants three months to retrain. The quarter closes in three weeks. You need a decision.

**The three moves available:**

| Improve the model | Lower the damage | Narrow the scope |
|---|---|---|
| Retrain on more data | Add a hold on the paid reissue | Ship the two easy slices now |
| 3 months, an ML team | a person approves before charge | hold the hard codeshare slice |
| The bar does not move | wrong now costs $8 not $32 | each slice gets its own bar |
| *slow, the only option engineering named* | *a product decision you make this week* | *ship value now, finish later* |

## The questions

**Work it out.** The bar with no hold: $32 ÷ $8 = 4 rights per wrong, so bar = 1 − 1/5 = **80%**. Check each slice against 80%. Then decide.

**B1. Against the 80% bar, which slices clear it?**

- a. All three
- b. Same route and Reprice; Codeshare fails
- c. Only Same route
- d. None, because the overall 84% is below 90%

**B2. Engineering's plan is to retrain for three months. What does that do to the bar?**

- e. Lowers the bar to something the model can hit
- f. Nothing. Retraining changes the model, not the cost of a wrong answer
- g. Raises the bar, because expectations rise
- h. Removes the need for a bar entirely

**B3. You add a hold: a person approves any codeshare reissue before it is charged, so a wrong answer costs only the $8 of wasted handling. What is the codeshare slice's new bar, and does 71% clear it?**

- i. New bar 50%, and 71% clears it
- j. New bar 50%, and 71% still fails
- k. New bar 75%, and 71% fails
- l. The bar is unchanged, a hold does not affect it

**B4. What do you decide, to ship value this quarter?**

- m. Wait three months for the retrain, as engineering asked
- n. Ship Same route and Reprice now; put a hold on Codeshare so it ships too
- o. Ship all three now at 84%, the average is fine
- p. Lower the bar to 71% so everything qualifies

**How to answer.** Type all four with the letters you choose, for example `B1-a B2-e B3-k B4-m`.
