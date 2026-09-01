# Mid-Session Exercise: Read the Trace, Name the Failure

**Format:** pairs. **Time:** 18 minutes (6 diagnose, 7 reproduce, 4 predict, 1 commit). **You need:** notebook 00 (optional, live) and `bedrock_agents_concepts_activities.xlsx`. No network needed; the trace is printed below.

**The situation.** Yesterday the TravelMind agent (Nova Lite) handled a disruption well, then a passenger said "go with option-1" and got back "Sorry, I am unable to assist you with this request." Your job is to prove what actually went wrong, using only what we have covered so far. You will not fix it yet. You will name the disease and predict the cure.

---

## The trace (excerpt)

```
USER: Can you go with option-1

ASSISTANT: Thought: <thinking> The user picked option 1. I should confirm the
           rebooking. Let me look up the booking. </thinking>
           Action: BookingActions__lookup_booking(pnr="JX48Q2")
TOOL (lookup_booking): { "status": "CANCELLED", "flight": "AI-302", "date": "2026-06-12" }

ASSISTANT: Thought: <thinking> The user picked option 1. I should confirm the
           rebooking. Let me look up the booking. </thinking>
           Action: BookingActions__lookup_booking(pnr="JX48Q2")
TOOL (lookup_booking): { "status": "CANCELLED", "flight": "AI-302", "date": "2026-06-12" }

ASSISTANT: Thought: <thinking> The user picked option 1. I should confirm the
           rebooking. Let me look up the booking. </thinking>
           Action: BookingActions__lookup_booking(pnr="JX48Q2")
TOOL (lookup_booking): { "status": "CANCELLED", "flight": "AI-302", "date": "2026-06-12" }

   ... same thought, same call, same result, repeats ~50 times ...

ASSISTANT: Thought: <thinking> (1
[orchestration iteration cap hit · operationTotalTimeMs: 67844 · inputTokens: 11661]

RETURNED TO USER: "Sorry, I am unable to assist you with this request."
```

The agent's three tools: `lookup_booking`, `get_disruption_reason`, `get_rebooking_options`.

---

## Part 1: Diagnose (6 min)

Answer on paper. One or two lines each.

1. The reply "Sorry, I am unable to assist" came from one of: the model, the orchestrator, the tool. Which one, and what in the trace tells you?
2. Look at the repeating block. Which field did the model itself author, and which fields are plumbing? (Use the trace-authorship rule from this morning.)
3. The agent says "I should confirm the rebooking." Look at its three tools. What can it not do, and so what does it fall back to?
4. Two separate things had to be true for this to loop forever, not just once. Name both.

## Part 2: Reproduce it (7 min)

Open `bedrock_agents_concepts_activities.xlsx`, sheet **ReAct Loop Sim**.

5. Set: User goal = `Confirm option-1`, Terminal action available = `No`, Decoding = `1 (greedy)`, cap = `8`. Read the OUTCOME cell and the turn table. Write down what it says and why.
6. Now change exactly one dropdown so the outcome becomes a clean exit. Which one did you change, and what is the new outcome?
7. Put it back to `No`, and instead change only the decoding to `>1 (varied)`. Does the loop stop? What does that tell you about which fix actually matters?

## Part 3: Predict the cure (4 min)

You will see the code controls in the next block. Predict now.

8. In one sentence: what is the smallest change to the agent's design that stops this loop?
9. Name one more guard you would add in code as a backstop, in case the model still misbehaves.

## Commit (1 min)

Each pair: one sentence for question 8, ready to say out loud.

---
---

## Facilitator answer key (do not project)

1. **The orchestrator.** The model never emitted a final answer. The trace shows the iteration cap hit and the last thought cut off mid-token. That sentence is Bedrock's orchestration fallback, not TravelMind.
2. The model authored only the **Thought and the Action** (its `rawResponse`, with the thought surfaced as `rationale`). The `TOOL` results and the dispatch are orchestrator and Lambda. The point: the model really did keep choosing the same call.
3. There is **no `confirm_rebooking` tool**. The goal it set itself ("confirm the rebooking") has no terminal action, so it falls back to the only concrete tool that runs, `lookup_booking`.
4. Both must hold: **(a) no terminal action** for the goal, and **(b) greedy decoding (topK=1)** so identical input gives identical output every turn, so it never drifts out on its own.
5. OUTCOME = RUNAWAY, repeats `lookup_booking` to the cap. The turn table shows `tool_use` every turn and CAP HIT on the last.
6. Set **Terminal action = Yes**. Outcome becomes a clean exit (`confirm_rebooking` runs, then end_turn). This is the real fix.
7. Loop still runs. Changing decoding alone does **not** save it; the missing terminal action is the cause. Good moment to say: do not reach for sampling knobs to fix a design hole.
8. Add a terminal action (`confirm_rebooking`), or instruct the agent to reply directly on selection. Either gives the goal a legal way to end.
9. A loop guard: a `max_turns` cap plus repeat-detection that breaks on an identical consecutive call, falling back to `handoff_to_human`.

## What good looks like

A pair that says: "It is not a refusal and not a code bug. The orchestrator looped because the agent had no way to finish, and greedy decoding meant it never changed its mind. Add a terminal action; back it with a repeat-breaking cap." That pair is ready for Block C.
