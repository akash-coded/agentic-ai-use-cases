# Roadmap

What is planned, and what is open for contribution. Tracked publicly on the
[project board](https://github.com/akash-coded/aws-bedrock-agentcore-strands/projects).

## Now

| Item | Status |
| --- | --- |
| 16 modules, complete with exercises and worked solutions | ✅ Done |
| Architecture HLD + 16 LLDs | ✅ Done |
| 5 role-based learning paths | ✅ Done |
| 7 sample PRDs across the lifecycle | ✅ Done |
| Setup, cost-control and troubleshooting guides | ✅ Done |
| CI validating notebooks, links and secret leakage | ✅ Done |

## Next

| Item | Notes |
| --- | --- |
| Session walkthrough recordings | Tracked in the [video index](reference/video-index.md). Say which module you want first in Discussions. |
| Per-module cost estimates | Actual measured cost of completing each module, not estimates |
| Self-assessment checkpoints | A short check at the end of each module so you know whether to move on |
| Terraform alternative to CDK | Module 11 currently ships CDK only |
| Model-agnostic notebook variants | Running the core notebooks against non-Bedrock providers via LiteLLM |

## Open for contribution

These are genuinely wanted and not started. Comment on the relevant issue before starting something large.

- **More adversarial evaluation cases** — the [golden set](../modules/13-agentic-qa-and-evaluation/src/golden_set.jsonl) has 15 adversarial cases. It should have more.
- **Failure modes from real production** — every [LLD](architecture/lld/) has a failure table; real incidents belong in them
- **Exercises in other domains** — TravelMind is the through-line, but standalone exercises in other domains would broaden reach
- **Translations** — starting with module READMEs and `docs/START-HERE.md`
- **AWS behaviour updates** — the highest-value contribution. Services change; material goes stale.

## Deliberately not planned

- **A hosted version.** This is a repository you clone and run. That is the point.
- **Fine-tuning or model training.** Different discipline, different curriculum.
- **Framework advocacy.** [Module 08](../modules/08-langchain-and-langgraph/) compares Strands and LangChain
  on the same task and lets the comparison stand. That will not become a recommendation.

---

Want something that is not here? [Open a Discussion](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/categories/ideas).
