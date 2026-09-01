# How to · Staff an agent team

**The mistake:** hiring "AI engineers" for a problem that is 30% model work and 70% data, integration,
evaluation and operations.

---

## What the work actually is

Across delivered agent projects, roughly:

| Work | Share | Who does it |
| --- | --- | --- |
| Tool/integration engineering | ~30% | Backend engineer |
| Corpus and retrieval quality | ~20% | Data or search-minded engineer |
| Evaluation and gating | ~20% | QA with a testing-under-uncertainty mindset |
| Agent loop, prompts, topology | ~15% | Anyone who has built one |
| Operations, observability, on-call | ~15% | Whoever is on-call |

**The "AI" part is the smallest slice.** Staffing for it exclusively is why teams end up with an
impressive agent that has no evaluation, no corpus owner and nobody on-call.

## The minimum viable team

| Role | Why | Can be shared? |
| --- | --- | --- |
| **Backend engineer** | Tools are API integrations | No |
| **Someone who owns evaluation** | Otherwise there is no evidence | No |
| **Domain expert access** | The golden set needs their judgement | Part-time, but real |
| **Corpus owner** | Unowned corpus goes stale silently | Often outside the team |
| **Product/BA** | Specification and scope | Shared |
| **On-call** | It is production software | Existing rota |

> If you cannot name the **corpus owner** and the **evaluation owner**, you are not ready to start. Those
> two gaps cause more failed agent projects than any technical decision.

## Hire for these three traits

| Trait | Why | How to test |
| --- | --- | --- |
| **Failure orientation** | The job is anticipating what breaks | "What did you get wrong, and what changed?" |
| **Evidence discipline** | Claims without denominators are how projects die | "How do you know it works?" |
| **Cost awareness** | Cost is structural here, not incidental | "Cost doubled, traffic flat. Where do you look?" |

Adjacent experience transfers well: distributed systems, **search relevance** (unusually well to RAG),
safety-critical software, data quality. Do not require "years of LLM experience" — almost nobody has them,
and the ones who claim them are often the least calibrated.

See the [hiring guide](../../interviews/as-the-interviewer.md).

## Team shapes by stage

| Stage | Shape |
| --- | --- |
| **Exploration** | 1 engineer + PM, 4–6 weeks, output is a decision not a product |
| **First build** | 2 engineers + evaluation owner + part-time domain expert |
| **Production** | Add operations ownership and a named corpus owner |
| **Multiple agents** | Platform team owns the runtime; product teams own agents |

The exploration stage should be explicitly allowed to conclude "this should not be an agent". If it cannot,
it is not exploration.

## Skills to build in the team

Cheapest first:

1. **Everyone writes the agent loop by hand once** —
   [Module 05](../../../modules/05-agent-loop-no-framework-to-strands/). One afternoon, and it changes how
   they debug forever.
2. **Everyone reads the gate** —
   [`quality_gate.py`](../../../modules/13-agentic-qa-and-evaluation/src/quality_gate.py). It is short and
   it defines "done".
3. **One person goes deep on retrieval** — [Module 10](../../../modules/10-rag-opensearch-litellm/). This is
   where quality actually lives.
4. **One person goes deep on the platform** — [Module 11](../../../modules/11-bedrock-agentcore/).

## The four ownership questions

Ask these at kickoff. Blank answers are your risk register.

| Question | Owner |
| --- | --- |
| Who owns the corpus and its update cadence? | |
| Who owns the golden set and arbitrates disputed cases? | |
| Who is on-call when the agent misbehaves? | |
| Who decides to roll back, and on what criteria? | |

## Anti-patterns

| Anti-pattern | Consequence |
| --- | --- |
| A "GenAI team" separate from the domain team | Builds impressive things nobody adopts |
| No evaluation owner | No evidence; every review is opinion |
| Corpus owned by nobody | Stale index, confident-wrong, silently |
| No on-call | Failures found by customers |
| Hiring only for model expertise | 70% of the work is unstaffed |

**Related:** [Hiring guide](../../interviews/as-the-interviewer.md) ·
[Agent Readiness Scorecard](../../frameworks/agent-readiness-scorecard.md)
