# How to · Build a golden set from real tickets

**Time:** 1–2 days with a domain expert. **Output:** the artefact that *is* the specification.

This is the highest-value thing a BA can produce on an agent project. It converts "it should be accurate"
into something engineering can build against and QA can gate on.

---

## 1. Get real inputs, not curated ones

| Good source | Bad source |
| --- | --- |
| Last 200 support tickets, sampled across the period | Examples someone remembered |
| Escalation logs | The documented process |
| Chat transcripts | Cases written for the demo |

Sample across time. Ticket mix changes with season, releases and incidents.

## 2. Classify — this is the real work

For each case, decide the **correct behaviour**, not what the current system does:

| Class | Correct behaviour | Target share |
| --- | --- | --- |
| **Answerable** | Answer, with a citation | ~50% |
| **Ambiguous** | **Abstain**, state the ambiguity | ~15% |
| **Out of scope** | Refuse, route | ~10% |
| **Data unavailable** | Say what is missing | ~10% |
| **Adversarial** | Resist | ~10% |

> **When two experts disagree about the answer, that is not a dispute to escalate — it is an ambiguous
> case, and the correct agent behaviour is abstention.** Recognising this is the core BA skill on agent
> projects. Record the disagreement as the evidence.

## 3. Write each case in a fixed shape

```json
{"id": "gs-047",
 "input": "My flight got cancelled and I booked through a travel agent, can I get a refund?",
 "class": "ambiguous",
 "expected_behaviour": "abstain",
 "expected_reason": "third_party_booking_ambiguous",
 "notes": "Fare rules cover direct bookings. Agent bookings governed by a separate agreement.",
 "source": "ticket-88213",
 "expert": "—",
 "added": "2026-07-14"}
```

`notes` is what makes the case survivable when the person who wrote it leaves.

## 4. Include cases the system currently fails

**A set built only from passing cases measures nothing.** Aim for at least 15% currently failing at
freeze. If everything passes on day one, you have documented current behaviour, not correct behaviour.

## 5. Derive the abstention target

```
target_abstention = ambiguous + out_of_scope + data_unavailable
                  ≈ 15% + 10% + 10% = 35%
```

That number goes straight into the [acceptance criteria](../product/write-acceptance-criteria.md). Nobody
sets it, so nobody notices when the agent abstains never or always.

## 6. Freeze it, then version it

- Freeze **before** tuning. A set tuned against is a mirror.
- Version it. Adding cases is normal; changing an expected answer needs a reason recorded.
- Never edit a case to make a build pass. That is editing the test.

## 7. Hand it over properly

Engineering needs:

| | |
| --- | --- |
| The file | JSONL, one case per line |
| The classification rules | So new cases can be added consistently |
| Slice definitions and target shares | So the gate can check per slice |
| The abstention target | With how it was derived |
| The owner | Who arbitrates a disputed case |

## 8. Keep it alive

Production surfaces what your set could not. Add real failures monthly. A golden set whose newest case is
six months old is [silent degradation #12](../../frameworks/silent-degradation-watchlist.md).

## The checklist

- [ ] ≥100 cases from real inputs
- [ ] All five classes represented
- [ ] ≥15% currently failing
- [ ] Adversarial cases include injection via *retrieved content*
- [ ] Abstention target derived and documented
- [ ] Frozen before tuning, and versioned
- [ ] Owner named
- [ ] Refresh cadence agreed

**Related:** [Evidence Ladder](../../frameworks/evidence-ladder.md) ·
[Abstention Budget](../../frameworks/abstention-budget.md) ·
[Module 13](../../../modules/13-agentic-qa-and-evaluation/)
