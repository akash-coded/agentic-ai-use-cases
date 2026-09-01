# Facilitator runsheet — Bedrock Agents

**What the room can do by the end**
1. Say what the model does versus what Bedrock does.
2. Connect to and drive their console-built agent from code.
3. Control its behaviour: the runaway loop, temperature / topK, and hallucinations.

**Anchor narrative.** Open on yesterday's broken trace ("Can you go with option-1" returned "Sorry, I am unable to assist"). That is the spine of the whole session. They name the disease at the midpoint and learn the cure in the last hour. Every block points back to it.

**The spine is LAB (your own framework).** Each block runs Learn (deck) then Apply (one activity workbook plus a 2 to 4 minute mini) then Build (a notebook live, the mid-session exercise, or the take-home). Notebooks run on PRIMM: Predict, Run, Investigate, Modify. The workbooks are the Predict surface: they guess what a toggle does before the notebook proves it.

**Open in tabs before you start.** Three decks. Notebooks 00 to 05. Three workbooks: `bedrock_agents_concepts_activities`, `console_to_code_activities`, `controlling_behavior_activities`. The mid-session exercise and the take-home.

**Live-environment facts (from yesterday).** The agent is **Nova Lite 1.0**. Use PNR **JX48Q2** when you run notebook 00 live (it is the one your tools know), not the notebook's placeholder ABC123. The `us.` prefix block you hit was real, so the Model ID Checker mini lands with weight.

---

## The clock

| Start | Min | Block | On screen | The move | Artifact | If behind, cut this |
|---|---|---|---|---|---|---|
| 0:00 | 10 | Cold open + recover | yesterday's broken trace | Hook: "why did it say that?" Then 60s think-pair: "what did we build yesterday?" Set the 3-part map. | the trace image | never cut the hook |
| 0:10 | 30 | A. Concept (Learn) | `bedrock_agents_deck` | Spine slides only (~12 of 25): loop not model, component map, orchestrator + ReAct, trace authorship, the loop-break, three ways to build. | deck | drop "three ways to build" to a 90s teaser; it recurs Day 9 |
| 0:33 | 5 | Mini 1 (Apply) | ReAct Loop Sim | Predict then toggle: goal = Confirm option-1, terminal action = No, greedy. It goes RUNAWAY. Flip terminal action to Yes: clean exit. This is yesterday's bug, on screen. | `bedrock_agents_concepts` | shorten to 3 min, skip Trace Authorship quiz |
| 0:38 | 2 | Modality switch | stand, stretch | Reset attention. | — | keep |
| 0:40 | 35 | B. Code (Learn + Apply) | `Day8_Deck1_Console_to_Code` + nb 00 then 01 | Teach the 4 clients with Client Picker open as the live lookup. Then PRIMM notebook 00: connect, run the 3 paths, read the trace, fix the fail path. | deck, `console_to_code`, nb00/01 | run only nb00; mention nb01 exists |
| 1:05 | 3 | Mini 2 (Apply) | Model ID Checker | Predict: Claude + on-demand in us-east-1, works or fails? Toggle: FAILS. Switch to cross-region profile: works. Callback to yesterday's block. | `console_to_code` | keep; it is 2 min and personal to them |
| 1:08 | 12 | B. Code (Build reveal) | nb 02 (then nb 03 teaser) | The hand-built loop: "here is what the orchestrator did for you." Show the loop body, the stopReason check, the toolResult append. Action groups (nb 03) as a 90s preview. | nb02/03 | skip nb03 entirely; one line that tools = action groups |
| 1:20 | 5 | Break | — | Hard stop, real break. | — | keep |
| 1:25 | 20 | MID-SESSION EXERCISE (Build) | exercise sheet | Pairs. Diagnose yesterday's loop from the trace, reproduce it in the sim, and predict the fix family. You float and prompt. 4 min share-out at the end. | `Day8_MidSession_Exercise` | floor is 15 min; trim share-out to 2 min, never skip the pairing |
| 1:45 | 50 | C. Control (Learn + Apply) | `Day8_Deck2_Controlling_Behavior` + nb 04 then 05 | Loop control, inference, reasoning-model traps, hallucination defence. One workbook sheet per concept as you teach it. Close the option-1 loop here (callback). | deck, `controlling_behavior`, nb04/05 | nb05 becomes a 3 min tour; cut the production deep-dive |
| 2:35 | 3 | Mini 3 (Apply) | Reach-For Table | Rapid retrieval: "runaway loop, what do you reach for? ungrounded answer, what do you reach for?" | `controlling_behavior` | keep; it is the recall check |
| 2:38 | 17 | Synthesise + close the loop | the cold-open trace again | The room states the full fix out loud (terminal action + reply-directly instruction + spin guard). Five takeaways, rapid-fire. | trace image | trim takeaways to 3 |
| 2:55 | 5 | Take-home brief + next | take-home sheet | Two tracks, they pick one. Show the rubric. One line on Day 9. | `Day8_TakeHome_Assignment` | keep |

Total 180. Three slack points are built in (the two modality breaks and the nb05 tour) so a 10-minute overrun anywhere does not sink the close.

---

## Where each artifact enters, and why there

| Artifact | Enters at | Job |
|---|---|---|
| ReAct Loop Sim | 0:33 (Mini 1) | Predict surface for the loop. Re-creates yesterday's failure so the concept is felt, not told. |
| Client Picker | 0:40 (live, Block B) | A lookup you teach from, not a quiz. Kills the 4-client confusion in real time. |
| Model ID Checker | 1:05 (Mini 2) | Names the exact `us.`-prefix trap they hit yesterday. Personal, so it sticks. |
| Mid-session exercise | 1:25 | The diagnosis. Pairs name the disease using only what A and B taught. Sets up C. |
| Loop Control Sim | 1:45 (Block C) | The cure for the cold-open mystery. Toggle the three fixes, watch the runaway resolve. |
| Inference Tuner + Reasoning Guard | within Block C | "When to change temperature, when not" and the thinking-on 400 trap, both as Predict-then-check. |
| Defense Designer + Guardrail Lab | within Block C | Hallucination control made tangible: layers, coverage, BLOCK versus PASS at a threshold. |
| Reach-For Table | 2:35 (Mini 3) | Retrieval check: symptom to control. |
| Take-home | 2:55 | The Build that outlives the room. |

---

## Your gaps, and the guardrail for each (today only)

Stated plainly because you asked. These are working-style tendencies, not verdicts. Each has one concrete countermeasure baked into the clock above.

| Tendency | How it shows up in a room | Today's guardrail |
|---|---|---|
| Treating your read as the only right one | You lecture and defend instead of drawing the room out; you close divergent ideas fast | Three scripted Socratic / steelman prompts (below). You ask before you reveal. Run them even when you are sure. |
| Going deep to avoid moving on | You over-explain the interesting part and run out of clock for the rest | The cut column is pre-decided. When the clock says move, you move. Park deep questions on a visible "parking lot", answer two at the close. |
| Low interaction by default | The session becomes a monologue | The mid-session is pair-only. Three minis force a predict-out-loud. Two think-pairs in the first 40 minutes. |
| Energy dips on the dull stretches | Setup and plumbing drag, pace sags | Modality switches every 25 to 35 minutes are on the clock. Plumbing (clients, IDs) is taught off a live workbook, not slides. The cold-open mystery supplies the urgency. |

**The three prompts (say them verbatim):**
- After Mini 1: "Argue the agent is not broken. What is it doing exactly right?" (steelman the orchestrator; the answer is "faithfully dispatching the only tool it has").
- In Block C, on inference: "When would lowering temperature be the wrong move?" (drafting, brainstorming; determinism is not always the goal).
- At the close, before you give the fix: "Smallest change that stops the loop. One sentence. Go." (let two pairs answer before you confirm).

---

## Cold-open script (say roughly this)

"Yesterday this agent told a passenger 'Sorry, I am unable to assist.' It was not refusing. It was stuck in a loop until Bedrock killed it. By the end of today you will know exactly why, and the three-line fix. First we figure out what the model is even doing, then we drive this thing from code, then we take the controls."

Then the 60-second think-pair: "Turn to the person next to you. In one sentence each: what did we actually build yesterday?" Take two answers, move.

---

## Closing script (the loop closes)

Put the broken trace back up. "We can now read this. The model authored only the repeating thought and the repeating call. The orchestrator faithfully ran it fifty times because there was no terminal action and greedy decoding meant it never drifted. The fix is three things." Let the room say them. Confirm: a terminal action so the goal can end, an instruction to answer directly on selection, and a loop guard that breaks on identical repeats.

Five takeaways, rapid-fire, no slide needed:
1. The model thinks; the orchestrator loops.
2. The model authored only `rawResponse`. Everything else is plumbing or your code.
3. Every goal needs a terminal action.
4. Thinking on means sampling off.
5. Grounding plus guardrail are the heavy hitters for hallucination.

---

## If AWS access wobbles again

The mid-session exercise ships with a printed trace excerpt, so pairs can diagnose with zero live calls. The workbooks need no network. If notebook 00 will not connect live, narrate the cells and run the exercise off the excerpt. Do not burn class time debugging IAM; that goes on the parking lot.
