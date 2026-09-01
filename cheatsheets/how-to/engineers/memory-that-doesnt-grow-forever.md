# How to · Add memory that does not grow forever

**Time:** 2 hours. **The failure this prevents:** context overflow, and a storage bill nobody predicted.

---

## 1. Decide what you are actually keeping

Before any code, fill this in. It is a product decision, not a technical one.

| Question | Yours |
| --- | --- |
| What must survive within a conversation? | |
| What must survive **across** conversations? | |
| What must never be stored? | |
| How long is the audit window? | |
| Who can request deletion? | |

"Everything, forever" is not an answer — it is a cost and a liability.

## 2. Pick the strategy per scope

| Scope | Strategy | Why |
| --- | --- | --- |
| Within a turn or two | Buffer (verbatim) | Cheap, exact |
| Long conversation | Buffer + summarise past a cap | Bounded |
| Across sessions | Structured facts, not transcripts | Retrievable, small, auditable |
| Domain knowledge | **Not memory — retrieval** | Different problem entirely |

> The most common design error is using memory for what retrieval should do. Company policy is not memory;
> it is a corpus. Memory is what happened *in this relationship*.

## 3. Cap the buffer — with a threshold, not a schedule

```python
MAX_HISTORY_TOKENS = 40_000

def trim(history, summarise):
    used = sum(count_tokens(m) for m in history)
    if used <= MAX_HISTORY_TOKENS:
        return history                       # do nothing — the common case
    # keep the most recent turns verbatim; summarise the rest
    recent, older = history[-6:], history[:-6]
    return [summarise(older)] + recent
```

Summarising **every** turn costs a model call every turn. Summarise when the buffer crosses its bound.

## 4. Store facts, not transcripts

```python
# ❌ grows without bound, hard to use, full of PII
{"session": "s-42", "transcript": [ ...every turn... ]}

# ✅ bounded, useful, reviewable
{"session": "s-42",
 "booking_ref": "XY7Q2M",
 "resolved": True,
 "outcome": "refund_eligible",
 "citation": "fare-rules/QW7#7.3",
 "expires_at": "2026-10-01"}
```

Structured memory is smaller, retrievable, auditable, and deletable per subject — which matters when
someone exercises a deletion right.

## 5. Set a TTL, and mean it

```python
MEMORY_TTL_DAYS = 30    # must equal your audit window, not "as long as possible"
```

On AgentCore, configure retention at the memory store. Whatever the platform, the TTL should be a named
constant with a comment saying *why* that number.

## 6. Never store these

- Raw PII beyond an identifier
- Payment details, credentials, tokens
- Full documents (that is what retrieval is for)
- Anything you could not justify in a subject access request

**Nothing to leak is the strongest control available.**

## 7. Instrument it

| Metric | Alert |
| --- | --- |
| Memory size per session | p99 growing week on week |
| Input tokens per turn | p99 > 85% of the context window |
| Summarisation frequency | Rising — the cap may be too low |
| Store size total | Growing while sessions are flat = TTL not applying |

## 8. Test what it forgets

```python
def test_summary_preserves_the_decisive_fact():
    h = long_conversation_where_user_states_a_constraint_early()
    trimmed = trim(h, summarise)
    assert "wheelchair access" in serialise(trimmed)
```

**This is the test everyone skips.** Summary memory drops detail unpredictably, and the fact it drops is
often the one the user cares most about. Write a test for each fact type that must survive.

## The checklist

- [ ] Retention decision written down, with a reason
- [ ] Buffer capped by tokens
- [ ] Summarisation triggered by threshold, not schedule
- [ ] Long-term memory stores facts, not transcripts
- [ ] TTL set and verified to actually apply
- [ ] No PII beyond an identifier
- [ ] Test asserting a decisive fact survives summarisation
- [ ] Memory size instrumented

**Related:** [Context Budget Ledger](../../frameworks/context-budget-ledger.md) ·
[Module 09](../../../modules/09-llm-memory/) · [AgentCore](../../quick-reference/agentcore.md)
