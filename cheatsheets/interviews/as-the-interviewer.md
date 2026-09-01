# Guide · Hiring for agentic AI

You are hiring into a field where almost nobody has five years of experience and everybody has a
confident opinion. This is how to tell them apart.

---

## What you are actually hiring for

| Not this | This |
| --- | --- |
| Knows the frameworks | Can debug when the framework does not help |
| Has built a demo | Has operated something in production |
| Keeps up with model releases | Knows what to measure and why |
| Confident about what agents can do | Clear about what they cannot |

> The strongest predictor across every role is whether someone can describe a **failure they caused** and
> what they changed afterwards. Ask for it directly.

## The universal questions

Ask these regardless of role. They work for engineers, PMs, architects, BAs and QA alike.

**1. "What does the system do when it doesn't know the answer?"**
Reveals whether the person has thought about failure at all. Everyone in agentic AI should have an answer.

**2. "How do you know it works?"**
Listen for an [evidence rung](../frameworks/evidence-ladder.md). "It works well" is E0.

**3. "Tell me about something you decided not to build."**
Judgement under enthusiasm. Everyone can list what they built.

**4. "What did you get wrong, and what changed as a result?"**
The single highest-signal question in this field. No production experience → no good answer.

## The three-signal rubric

Score each candidate on three axes rather than a checklist:

| Axis | Weak | Strong |
| --- | --- | --- |
| **Failure orientation** | Talks about capability | Talks about what breaks and how they would know |
| **Evidence discipline** | Asserts | Quantifies, and names the denominator |
| **Cost awareness** | Never mentions it | Knows cost is structural, not incidental |

Two of three is usually hireable. Zero on failure orientation is not, at any level.

## Structuring the loop

| Stage | Purpose | Do |
| --- | --- | --- |
| Screen | Filter demo-only experience | The four universal questions |
| Technical / craft | Depth in the actual job | Role guide below |
| Practical | Watch them work | Broken agent, or a real ticket sample |
| System / design | Judgement under constraint | Design exercise with a cost constraint |
| Values | How they handle being wrong | "Tell me about a time you were confidently wrong" |

**Bias toward the practical stage.** Agentic AI is a field where articulate people can sound expert
without having built anything. Forty-five minutes with a broken agent settles it.

## The practical exercise that works for every role

Give a real artefact and ask what they would do with it.

| Role | Artefact | Watch for |
| --- | --- | --- |
| Engineer | Agent with one seeded defect | Do they instrument or guess? |
| Architect | A design with an unbounded swarm | Do they spot it unprompted? |
| PM | Metrics showing 58% against a 60% target | Do they ask what the 42% is? |
| BA | 20 real support tickets | Do they classify, or summarise? |
| QA | A golden set that passes 100% | Do they distrust it? |

## Role guides

- 🛠️ **[Agent Engineer](agent-engineer.md)**
- 🏛️ **[Solutions Architect](solutions-architect.md)**
- 📋 **[Product Manager](product-manager.md)**
- 📊 **[Business Analyst](business-analyst.md)**
- 🔬 **[QA Engineer](qa-engineer.md)**

## Calibration for a young field

- **Do not require years.** Require evidence of judgement. Someone who shipped one careful agent beats
  someone who prototyped ten.
- **Adjacent experience counts.** Distributed systems, search relevance, safety-critical software and data
  quality all transfer well. Search relevance transfers unusually well to RAG work.
- **Discount fluency.** This field rewards people who sound confident. Weight what they measured over what
  they can describe.
- **Test for updating.** Present a fact that contradicts their answer and see whether they incorporate it
  or defend. This is the trait that matters most in a field changing this fast.

## Questions that do not work

| Avoid | Why |
| --- | --- |
| "What's the difference between LangChain and Strands?" | Recall, not judgement |
| "How does attention work?" | Irrelevant to almost every agent role |
| "What's the context window of model X?" | Changes monthly; it is a lookup |
| "Design an AGI system" | Unfalsifiable, rewards fluency |
| Anything answerable from a blog post | You will hire the best reader |

## The offer conversation

Candidates worth hiring will ask you these. Have answers:

- What is on-call like for the agent?
- Is there a golden set, and does the gate fail the build?
- Who owns the corpus?
- What is the cost per task today?
- What was the last incident, and what changed?

Not having answers is informative for both sides.

---

[⬅️ Field guide](../) · [🧠 Frameworks](../frameworks/)
