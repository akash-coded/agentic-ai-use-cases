# Extension Roadmap

The curriculum and [field guide](../cheatsheets/) are complete and usable today. This is what comes next —
organised into five phases, each of which stands alone and ships something useful.

Tracked on the public board: **[Extension Roadmap](https://github.com/users/akash-coded/projects/6)**

---

## Why an extension roadmap at all

The repository currently answers "how do I learn this". The extension answers three further questions:

1. **"How do I know I've learned it?"** — self-assessment, and a certificate path
2. **"How do I use this with my team?"** — facilitation kits, workshop formats, team assessments
3. **"How do I keep this current?"** — automation that catches drift before a learner does

---

## Phase 1 · Depth — make what exists provably good

| Item | Why | Effort |
| --- | --- | --- |
| Self-assessment per module | You can finish a module without knowing whether you learned it | M |
| Measured cost per module | Real numbers beat "tens of dollars" | S |
| Expand the golden set to 200+ cases | 130 is thin for the adversarial and abstention slices | M |
| Solution walkthroughs for the 5 hardest exercises | The capstones lose people | M |
| Per-module prerequisite check script | "Can I start module 11?" answered by a script | S |

## Phase 2 · Reach — more people can use it

| Item | Why | Effort |
| --- | --- | --- |
| Session walkthrough recordings | The [video index](reference/video-index.md) exists and is empty | L |
| Translations: START-HERE + module READMEs | English-only limits reach substantially | L |
| A companion site (GitHub Pages) | Markdown on GitHub is not the best reading experience for 77 field-guide pages | M |
| Printable field-guide PDFs | People want the frameworks on a desk, not a screen | S |
| Audio/short-form summaries of frameworks | Different learning modes | M |

## Phase 3 · Interactive — tools, not just documents

| Item | Why | Effort |
| --- | --- | --- |
| Agent Readiness Scorecard as a web tool | The [scorecard](../cheatsheets/frameworks/agent-readiness-scorecard.md) wants to be interactive |  M |
| Token-cost calculator, in-browser | The xlsx works but is not shareable | M |
| Topology cost estimator (H×) | Turn the [Handoff Multiplier](../cheatsheets/frameworks/handoff-multiplier.md) into a calculator | M |
| Golden-set builder / linter | Validate a set against the slice targets | M |
| "Which module should I do?" quiz | Better than reading five learning paths | S |

## Phase 4 · Team adoption — beyond the individual learner

| Item | Why | Effort |
| --- | --- | --- |
| Facilitator kit: run this as a team workshop | The material was built for cohorts; that path is currently undocumented | M |
| Team readiness assessment | Score a *team*, not a system | S |
| Reading-group guide, 12 weeks | A format organisations actually adopt | S |
| Case-study template + submissions | Real builds are the most persuasive content | S |

## Phase 5 · Currency — keep it true without heroics

| Item | Why | Effort |
| --- | --- | --- |
| Scheduled link + freshness checks | Docs rot silently | S ✅ |
| Notebook smoke-test workflow | Catch breakage before a learner does | M |
| AWS-change watch and issue template | Standing [issue #53](https://github.com/akash-coded/aws-bedrock-agentcore-strands/issues/53) | S ✅ |
| Model-ID and API drift audit, quarterly | The most common source of staleness | S |
| Terraform variant of the AgentCore module | CDK-only today | M |

---

## How to contribute to this

Every phase-1 through phase-4 item is open. The board marks which are
[good first issues](https://github.com/akash-coded/aws-bedrock-agentcore-strands/labels/good%20first%20issue).

Comment on the item before starting anything large so two people do not do the same work.

**The highest-value contributions, in order:**

1. **AWS behaviour that changed** — always. Nothing else degrades the material faster
2. **A case study of something you built** — the most persuasive content that exists
3. **Golden-set cases**, especially adversarial and abstention ones
4. **A translation** of START-HERE and the module READMEs

---

## What is deliberately not on the roadmap

- **A hosted, run-it-in-the-browser version.** This is a repository you clone and run against your own AWS
  account. Removing that removes the point.
- **Fine-tuning or model training content.** Different discipline, different curriculum.
- **Framework advocacy.** [Module 08](../modules/08-langchain-and-langgraph/) compares Strands and
  LangChain on the same task and lets the comparison stand. That will not become a recommendation.
- **Certification with a fee.** If a certificate path happens, it will be free and self-assessed.

---

[🏠 Repository](../) · [📋 Board](https://github.com/users/akash-coded/projects/6) ·
[💬 Suggest something](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/categories/ideas)
