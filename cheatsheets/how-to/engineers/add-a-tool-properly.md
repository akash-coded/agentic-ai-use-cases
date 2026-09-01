# How to · Add a tool the model actually calls correctly

**Time:** 30 minutes. **You need:** a working agent and one capability to expose.

Most "the model chose the wrong tool" bugs are schema bugs. This is the order that avoids them.

---

## 1. Write the boundary before the code

Before implementing anything, write two sentences:

```
get_fare_rules — retrieves change fees, refund eligibility and conditions for a fare class.
NOT for: a specific booking's status (use get_booking).
```

If you cannot write the "NOT for" line, you have not distinguished it from its neighbours — and neither
will the model.

## 2. Implement, with honest failure

```python
from strands import tool

@tool
def get_fare_rules(fare_class: str) -> dict:
    """Retrieve fare rules for a fare class: change fees, refund eligibility, conditions.

    Use after get_booking, which gives you the fare class.
    Does NOT know about a specific booking's status.

    Args:
        fare_class: Fare class code, e.g. "Y", "QW7", "B2"
    """
    rules = fare_db.get(fare_class)
    if rules is None:
        # explicit, not empty — an empty result reads as "nothing applies"
        return {"status": "not_found",
                "searched_fare_class": fare_class,
                "detail": "No rules on file for this fare class."}
    return {"status": "ok", "rules": rules}
```

**The single most important line is the `not_found` branch.** Returning `{}` or `[]` reads to a model as
"nothing applies", which is the opposite of "I could not check". That confusion is a leading cause of
confident-wrong answers.

## 3. Read the schema as the model receives it

```python
print(get_fare_rules.tool_spec)     # Strands
# or, for Bedrock directly, print your toolConfig
```

Read it as if you were the model and knew nothing else. Can you tell when to use this rather than the tool
next to it?

## 4. The neighbour test

Put every tool description side by side and ask a colleague:

> "Which of these answers *why was my refund declined*?"

If they hesitate, the model will too. Fix by naming the boundary and pointing at the alternative.

## 5. Test tool selection, not just tool execution

```python
def test_selects_fare_rules_for_eligibility_question():
    r = agent("Is fare class QW7 refundable?")
    assert "get_fare_rules" in [c.name for c in r.tool_calls]

def test_does_not_select_fare_rules_for_status_question():
    r = agent("What is the status of booking XY7Q2M?")
    assert "get_fare_rules" not in [c.name for c in r.tool_calls]
```

The negative test is the one that catches description overlap. Most suites only have the positive one.

## 6. Test failure honesty

```python
def test_abstains_when_rules_not_found(monkeypatch):
    monkeypatch.setattr(fare_db, "get", lambda _: None)
    r = agent("Is fare class ZZZ refundable?")
    assert "not" in str(r.message).lower() or "unable" in str(r.message).lower()
    assert "refundable" not in str(r.message).lower().replace("not refundable", "")
```

You are asserting the agent **says it could not check** rather than inventing an answer.

## 7. Score it before you ship

Run the [Tool Surface Audit](../../frameworks/tool-surface-audit.md): distinctness, sufficiency, failure
honesty, idempotency, blast radius, observability. Any red is a defect.

## 8. Prune

Does every route need this tool in context? Every tool costs
[schema tax](../../frameworks/token-tax-ledger.md) on every turn and adds one more chance to choose wrong.
Attach tools per route, not per agent.

## The checklist

- [ ] Boundary sentence written before the code
- [ ] Failure returns an explicit status, never `{}` or `[]`
- [ ] Schema read as the model receives it
- [ ] Neighbour test passed with a human
- [ ] Positive **and negative** selection tests
- [ ] Failure-honesty test
- [ ] Blast radius scored
- [ ] Attached only to routes that need it

**Related:** [Strands cheat sheet](../../quick-reference/strands.md) ·
[Tool Surface Audit](../../frameworks/tool-surface-audit.md) ·
[Module 06](../../../modules/06-strands-foundations/)
