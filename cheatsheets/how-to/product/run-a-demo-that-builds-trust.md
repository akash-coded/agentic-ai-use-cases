# How to · Run an agent demo that builds trust instead of spending it

**Time:** 45 minutes to prepare. **The trap:** a flawless demo raises expectations you cannot meet, and
the first production failure then reads as a betrayal.

---

## The counter-intuitive rule

> **Show the agent declining to answer.** An audience that sees an agent say "I don't know" trusts the
> answers it *does* give. This is reliably true and almost never done.

A perfect demo teaches your stakeholders that the agent is always right. That is the belief you will spend
the next six months correcting.

## The structure that works

| Minutes | Segment | Purpose |
| --- | --- | --- |
| 0–2 | The job it does, in one sentence | Frame — not "AI", the actual job |
| 2–5 | A clean success, with the trace visible | Show the mechanism, not magic |
| 5–8 | **An abstention** | Build trust; set expectations |
| 8–11 | **An audience input, unrehearsed** | Credibility |
| 11–14 | Cost and evidence | Ground it in numbers |
| 14–20 | Questions | |

## Segment by segment

**The success — show the trace.** Do not just show the answer. Show that it retrieved a passage, cited it,
and why. People trust systems whose reasoning they can inspect, and it inoculates against "it's a black
box".

**The abstention — the most important 3 minutes.** Take a genuinely ambiguous case and show the agent
decline, state the ambiguity, and route to a human.

> Say out loud: *"This is the behaviour we designed for. An agent that always answers is an agent that will
> sometimes be confidently wrong, and confidently wrong is the expensive failure."*

**The audience input.** Take one question from the room, unrehearsed. It may fail. **That is fine and you
should say so beforehand:** *"This is unrehearsed — let's see what it does."* If it fails, you have just
demonstrated the abstention path or a real limitation, both of which are useful.

The willingness to do this is itself the signal. Everyone knows a rehearsed demo is rehearsed.

**Cost and evidence.** Two slides:

```
Evidence:  87% on a 130-case set built from real enquiries.
           20 of those cases are ones where the correct answer is "I don't know".
           15 are adversarial. 100% of the safety cases pass — that one is pass/fail.

Cost:      $0.031 per resolved enquiry, measured.
           At 400/day that is $—/month.
```

Naming the denominator ("of a 130-case set built from real enquiries") is what separates a credible number
from a marketing one.

## What not to do

| Don't | Because |
| --- | --- |
| Cherry-pick only successes | You are borrowing trust you will have to repay |
| Hide the trace | "Black box" objections are earned |
| Say "it's about 90% accurate" | No denominator — someone will ask, and you will look evasive |
| Demo a capability that is not built | It becomes a commitment in the room |
| Take audience input with no failure plan | Prepare the sentence you will say if it fails |
| Claim it will replace anyone | Almost never true, and it makes enemies of your users |

## The questions you will get

| Question | Answer |
| --- | --- |
| "What if it's wrong?" | Here is the abstention rate, the citation requirement, and the human escalation path |
| "Can it do X too?" | Not today. Here is what it would take — [Scope Fence](../../frameworks/scope-fence.md) |
| "How accurate is it?" | X% on [named set of N], built from [source] |
| "Will it replace the team?" | It handles [specific slice]. The team handles the rest, plus the escalations |
| "What does it cost?" | $X per resolved enquiry, measured, at Y volume |

Prepare all five. They are asked every time.

## The one-line close

> *"It resolves [X%] of [specific enquiry type], it declines when it should, every claim carries a
> citation, and it costs [$Y] per resolved case. Here's what we'd need to widen the scope."*

**Related:** [Abstention Budget](../../frameworks/abstention-budget.md) ·
[Demo-to-Production Gap](../../frameworks/demo-to-production-gap.md) ·
[Evidence Ladder](../../frameworks/evidence-ladder.md)
