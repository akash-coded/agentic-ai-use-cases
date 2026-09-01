# Take-Home: Give the Agent a Clean Exit, or a Defence

**Due:** start of next session. **Effort:** about 60 to 90 minutes. **Pick one track.** Both use the notebooks and workbooks from today. Submit a single file (code plus screenshots, or a one-page write-up plus the saved workbook).

The point of today was the broken loop and how to control behaviour. This is where you make one of those controls real on your own.

---

## Track 1: Builder (you like code)

Make the option-1 loop impossible.

Start from **notebook 02 (the hand-built loop)** or your console agent. Do all three:

1. **Add a terminal action.** A `confirm_rebooking(pnr, flight)` tool (a stub that returns a confirmation is fine). The goal must now have a legal way to end.
2. **Add a loop guard.** A `max_turns` cap, plus repeat-detection that breaks if the model requests the same tool with the same arguments twice in a row, falling back to a `handoff_to_human` message.
3. **Prove it.** Run the "go with option-1" flow before and after. Capture both: the runaway (or its turn count) before, and the clean exit after.

**Submit:** your modified notebook or script, plus two trace snippets (before and after) with one or two sentences on what changed and why it now terminates.

---

## Track 2: Designer (you like architecture)

Design a hallucination defence for a real scenario.

Pick one: IROPS re-accommodation, baggage-policy answering, or fare-rule lookup. Then:

1. **Choose the layers.** In `controlling_behavior_activities.xlsx`, sheet **Defense Designer**, set the use-case risk and toggle the five layers. Reach a coverage that meets the bar for that risk, with no open gaps.
2. **Set the thresholds.** In sheet **Guardrail Lab**, choose grounding and relevance thresholds for this scenario. Use the sensitivity sweep to justify the number you picked, not a round default.
3. **Write the rationale.** One page: the scenario, the risk tier and why, which layers and why each earns its latency, the thresholds and the trade-off you accepted (fewer fabrications versus more good answers blocked).

**Submit:** the saved workbook plus the one-page rationale.

---

## Constraints (both tracks)

- Region `us-east-1`. If you call a model directly, use the correct id; Claude needs the `us.` cross-region profile, Nova does not.
- No hardcoded secrets or keys. If you note production changes, name the real ones: IAM role not access keys, retries with backoff, no hardcoded region.
- Substance over polish. A working loop or a defensible design beats a pretty document.

## Rubric (10 points)

| Criterion | Points | What earns full marks |
|---|---|---|
| It works / it is defensible | 4 | Track 1: option-1 exits cleanly and the guard breaks a forced repeat. Track 2: coverage meets the risk bar and thresholds are justified by the sweep, not guessed. |
| Reasoning is explicit | 3 | You can say why it terminates / why those layers and thresholds, in your own words. No hand-waving. |
| Names the failure layer correctly | 2 | You distinguish a design hole from a code bug from an infra issue. |
| Constraints respected | 1 | Right region, right model id, no secrets, honest production notes. |

## Stretch (optional, not graded)

Track 1 people: add a one-line spin-detection log so a reviewer can see the guard fire. Track 2 people: state the one input that, if a passenger sent it, would still slip past your defence, and what catches it.
