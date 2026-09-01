# The Tool Surface Audit

> **One line:** the model never sees your function — it sees a name, a description and a schema, so that
> is the only thing worth auditing.

Most "the model chose wrong" bugs are schema bugs. This audit finds them before production does.

---

## Score every tool on six axes

| Axis | Question | 🔴 Fail | 🟢 Pass |
| --- | --- | --- | --- |
| **Distinctness** | Could this be confused with a neighbouring tool? | Two tools whose descriptions overlap | Description names what it is *not* for |
| **Sufficiency** | Can the model fill every required argument from what it has? | Requires an id the model cannot know | All arguments derivable from context or another tool |
| **Failure honesty** | What does it return when it fails? | `{}`, `null`, or an empty list | An explicit error the model can act on |
| **Idempotency** | Safe to call twice? | Second call has a different effect | Same result, or explicitly guarded |
| **Blast radius** | See the [grid](blast-radius-grid.md) | Irreversible and wide | Reversible and narrow |
| **Observability** | Can you see it was called and what it returned? | No logging | Call, args and result logged with a trace id |

Any 🔴 is a defect. Distinctness and failure honesty produce the most bugs; blast radius produces the
worst ones.

## The neighbour test

Lay every tool description side by side, as the model receives them. Then ask:

> If I only had these descriptions, could I tell which one answers "why was my refund declined?"

If you cannot, the model cannot. The fix is almost always to state the boundary explicitly:

```
❌ "Get booking details."
❌ "Retrieve fare rules."

✅ "Retrieve a single booking by its reference: passenger, itinerary, fare class,
    current status. Use this when you need facts about a specific booking.
    Does NOT contain refund eligibility — use get_fare_rules for that."

✅ "Retrieve the fare rules for a fare class: change fees, refund eligibility,
    and conditions. Use after get_booking, which gives you the fare class.
    Does NOT know about a specific booking's status."
```

Two additions do the work: **what it is not for**, and **which tool to use instead**.

## The failure-honesty test

Force every tool to fail and observe the agent.

| Tool fails with | Agent should | Red flag |
| --- | --- | --- |
| Not found | Say the record does not exist | Invents a plausible record |
| Timeout | Say it could not check, and abstain or retry | Answers as if it had checked |
| Empty result | Distinguish "no results" from "no data available" | Treats empty as "nothing applies" |
| Malformed data | Report the anomaly | Narrates around the gap |

> **The dangerous case is the empty result.** `[]` from a policy search means "I found nothing", which the
> model very often reads as "no policy applies" — the opposite meaning. Return an explicit
> `{"status": "no_matches", "searched": "..."}` instead of a bare empty list.

This single change prevents a whole class of confident-wrong answers.

## The audit table

| Tool | Distinct | Sufficient | Fails honestly | Idempotent | Blast radius | Observable |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | |

## The pruning question

Ask per route, not per agent:

> Does the agent need *this* tool to handle *this* kind of request?

Every tool in context costs [schema tax](token-tax-ledger.md) on every turn, and every extra tool is one
more chance to choose wrong. Pruning the menu improves accuracy and cost simultaneously — a rare
combination worth exploiting.

## Where this shows up

- [Module 06](../../modules/06-strands-foundations/) — tool design and the tool catalogue
- [Tool catalogue workbook](../../modules/06-strands-foundations/activities/Tool_Catalog.xlsx)
- [Module 03](../../modules/03-bedrock-agents/) — OpenAPI schemas for action groups

**Related:** [Blast Radius Grid](blast-radius-grid.md) · [Failure Signature Catalog](failure-signature-catalog.md) ·
[Token Tax Ledger](token-tax-ledger.md)
