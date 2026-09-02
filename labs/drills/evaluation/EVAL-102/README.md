# EVAL-102 · Which properties does this golden set violate?

`evaluation` · **medium** · `predict` · ~10 min · no AWS account

A team reports **96% on their golden set** and wants to ship. Here is how the set was built:

> 60 cases, sampled from last quarter's real support tickets. The team labelled the correct answer for each. When we froze it, the agent passed 59. There are no cases where the right answer is "I don't know" — we removed those as unclear. 8 cases are adversarial, including two where the injected instruction arrives inside a retrieved document. The set was finalised after the last prompt-tuning round so it would reflect the current behaviour.

## The five properties of a set that measures something

| id | Property |
| --- | --- |
| `A` | Drawn from real inputs, not invented |
| `B` | Contains cases the agent currently fails (≥ 15% at freeze) |
| `C` | Has an abstention slice — cases whose correct answer is "I don't know" |
| `D` | Has an adversarial slice, including injection via retrieved content |
| `E` | Frozen **before** the tuning it is used to evaluate |

## Your answer

Which properties does this set **violate**? A list of ids.

````markdown
/drill EVAL-102

```python
answer = ["...", "..."]
```
````

And in a sentence above: what is the 96% actually evidence of?

## What this proves

That you can look at a confident number and say precisely what it is and is not evidence of — the one skill that stops a mirror being shipped as a measurement.
