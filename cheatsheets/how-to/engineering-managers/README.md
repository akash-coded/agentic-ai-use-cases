# How-to · Engineering Managers

Your two hardest problems on agent work are staffing for what the job actually is, and operating something
that fails without raising an error.

| How-to | For |
| --- | --- |
| 👥 **[Staff an agent team](staff-an-agent-team.md)** | The work is 30% model, 70% data, integration, evaluation and ops |
| 📟 **[Set up on-call for an agent](set-up-on-call.md)** | Standard on-call misses almost everything that matters here |

## The three things to internalise

1. **The "AI" part is the smallest slice of the work.** Staffing only for it leaves evaluation, corpus
   ownership and operations unowned — which is how agent projects actually fail.
2. **If you cannot name the corpus owner and the evaluation owner, you are not ready to start.**
3. **Alert on quality drift, not availability.** An agent can have a 0% error rate while being wrong most
   of the time.

## The four ownership questions

Ask at kickoff. Blank answers are your risk register.

- Who owns the corpus and its update cadence?
- Who owns the golden set and arbitrates disputed cases?
- Who is on-call when the agent misbehaves?
- Who decides to roll back, and on what criteria?

## Your frameworks

[Agent Readiness Scorecard](../../frameworks/agent-readiness-scorecard.md) ·
[Demo-to-Production Gap](../../frameworks/demo-to-production-gap.md) ·
[Silent Degradation Watchlist](../../frameworks/silent-degradation-watchlist.md)

## Also useful

[Running an agent design review](../../playbooks/agent-design-review.md) ·
[Hiring guide](../../interviews/as-the-interviewer.md) ·
[Killing an agent project](../../playbooks/killing-an-agent-project.md)

---

[⬅️ All how-tos](../)
