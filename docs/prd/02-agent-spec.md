# 02 · Agent Spec — TravelMind

> The contract between product and engineering. Precise enough to build from, and to test against.

**Status:** baseline · **Owner:** Product + Engineering

## Identity

**Name:** TravelMind · **Purpose:** resolve refund and disruption enquiries against published policy,
with a citation.

## Goal and non-goals

**Goal.** Given an enquiry and a booking reference, return a decision, the reasoning, and the policy
citation that supports it.

**Non-goals.** Executing payments. Negotiating exceptions. Answering without a citation. Anything
customer-facing.

## Behaviour contract

| The agent must | The agent must never |
| --- | --- |
| Cite the policy passage supporting any policy claim | Answer a policy question without a citation |
| Abstain and hand off when policy is ambiguous | Guess at an ambiguous case |
| State when a booking could not be retrieved | Proceed on an assumed booking state |
| Log which model produced the answer | Fail over silently |

## Tools

Designed with the [tool catalogue](../../modules/06-strands-foundations/activities/Tool_Catalog.xlsx).
Descriptions are written for the model, not for engineers — see the
[Module 06 LLD](../architecture/lld/06-strands-foundations.md).

| Tool | Description given to the model | Input | Returns | Failure behaviour |
| --- | --- | --- | --- | --- |
| `get_booking` | Retrieve a booking by its reference, including fare class and current status | `booking_ref: str` | Booking record | Return not-found; agent must say so |
| `get_fare_rules` | Retrieve the fare rules that apply to a given fare class | `fare_class: str` | Rules document | Return empty; agent must abstain |
| `search_policy` | Search refund and disruption policy for passages relevant to a question | `query: str` | Passages + citations | Return empty; agent must abstain |
| `get_disruption` | Retrieve disruption status for a flight on a date | `flight_no: str, date: str` | Disruption record or none | Return none; treat as no disruption |

No tool writes. Every tool is a read. That is what keeps the agent recommending rather than acting.

## Memory

| Scope | Kept | Retention | Why |
| --- | --- | --- | --- |
| Session | Turns in the current enquiry | Session end | Multi-turn clarification |
| Long-term | Resolved enquiry summaries, by agent | 30 days | Audit and handoff context |

Not kept: raw booking records, payment details, customer PII beyond the booking reference.

## Guardrails

| Policy | Behaviour |
| --- | --- |
| Denied topic — payment execution | Refuse and hand off |
| Denied topic — contract exceptions | Refuse and hand off |
| PII in output | Blocked beyond the booking reference |
| Grounding | Policy claim without citation fails a contract test |

## Escalation

The agent hands off to a human when: policy search returns nothing relevant; the booking cannot be
retrieved; two interpretations of policy conflict; or the user asks for anything in the non-goals.

Abstention is a success state. An agent that never abstains is not careful, it is overconfident.

## Acceptance criteria

1. Given a valid booking and a cancelled flight, returns eligibility with a policy citation.
2. Given an ambiguous policy case, abstains and states why.
3. Given an unretrievable booking, says so and does not proceed.
4. Given a request to issue a refund, refuses and hands off.
5. Every policy claim in every response carries a citation.

Encoded as contract tests in
[`test_contracts.py`](../../modules/13-agentic-qa-and-evaluation/src/test_contracts.py).

---

**Next:** [technical design](03-technical-design.md)
