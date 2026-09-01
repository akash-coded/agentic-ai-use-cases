# Prompting for Agents — Cheat Sheet

Prompting for an agent is not prompting for a chatbot. The model is choosing actions, not composing prose,
and it re-reads your instructions on **every turn of the loop**.

---

## The three prompts in an agent

| Prompt | Read | Optimise for |
| --- | --- | --- |
| **System prompt** | Every turn, every loop | Brevity — this is [instruction tax](../frameworks/token-tax-ledger.md) ×N |
| **Tool descriptions** | Every turn | Distinctness — the model picks from these alone |
| **User turn** | Once | Nothing; you do not control it |

Most prompt effort goes into the system prompt. Most prompt *bugs* are in the tool descriptions.

## System prompt structure that works

```
ROLE       One sentence. What you are.
SCOPE      What you handle, and explicitly what you do not.
EVIDENCE   Where truth comes from, and what to do without it.
ABSTENTION When to decline, and how to say so.
OUTPUT     The shape of a response.
```

Worked:

```
You assess refund eligibility for travel bookings against published fare rules.

You handle: refund eligibility, disruption rebooking options, policy explanation.
You do not handle: issuing refunds, contract exceptions, anything customer-facing.

Every policy claim must cite the passage that supports it. If search_policy returns
no relevant passage, you do not know the answer — say so.

Abstain when: policy is ambiguous, the booking cannot be retrieved, or two readings
conflict. State which, and what would resolve it. Abstaining is a correct outcome.

Respond with: decision, one-line reasoning, citation. No preamble.
```

Note what is absent: no persona, no "you are a helpful assistant", no politeness instructions. Every one of
those is tax paid on every turn for no behavioural gain.

## The five rules

**1. Say what to do when there is no answer.** The single highest-value line in any agent prompt. Without
it the model's default is to produce *something*, and something is how confident-wrong happens.

**2. Make abstention sound like success.** "Abstaining is a correct outcome" changes behaviour measurably.
If declining reads like failure, the model avoids it — and so does the next engineer who edits the prompt.

**3. Put boundaries in tool descriptions, not the system prompt.** The model reads the schema when
choosing. "Does NOT contain refund eligibility — use get_fare_rules" belongs on the tool.

**4. Never rely on the prompt for safety.** "Never issue a refund" is a suggestion. Not having a refund
tool is a fact. See [Blast Radius Grid](../frameworks/blast-radius-grid.md).

**5. Shorter is usually better.** Long instructions dilute, and you pay for them every turn. If you cannot
say why a line is there, delete it and run the golden set.

## Prompts are code

| Practice | Why |
| --- | --- |
| Version prompts in the manifest | Otherwise a regression cannot be correlated to a change |
| Review prompt diffs | A one-line change can alter every behaviour |
| Re-run the golden set on every change | A prompt change invalidates your evidence |
| Never edit the prompt to make a build pass | That is editing the test |

> The most common ungoverned change in agent systems is a prompt edit with no version bump. Nothing errors.
> Behaviour changes. Nobody can correlate it later.

## Anti-patterns

| Anti-pattern | Why it fails |
| --- | --- |
| "Be accurate and do not hallucinate" | Not actionable. Give it a rule: cite or abstain |
| Long persona preamble | Tax every turn, no behavioural gain |
| Examples of every case | Bloats context; use tool descriptions and retrieval instead |
| Rules contradicting earlier rules | The model picks one, unpredictably. Bisect the diff |
| Formatting instructions in the system prompt | Use structured output instead |

## Testing a prompt change

1. Run the golden set **before** the change; record the numbers
2. Make one change
3. Run it again
4. Check the abstention rate specifically — a *drop* usually means bolder, not better
5. Check cost per task — reasoning-token blow-up is [cliff 6](../frameworks/cost-cliff-map.md)
6. Bump the prompt version in the manifest

Steps 4 and 5 are the ones people skip, and they are where the regressions hide.

**Related:** [Abstention Budget](../frameworks/abstention-budget.md) ·
[Tool Surface Audit](../frameworks/tool-surface-audit.md) ·
[Ship a prompt change](../runbooks/deploy-prompt-change.md)
