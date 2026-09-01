# Interview Guide · Solutions Architect (Agentic AI)

Architects are hired for judgement under constraint. These questions probe judgement, not recall.

---

## The five questions

### 1. "A client wants an agent to handle 100% of their support tickets. Respond."

**Weak:** designs the system.
**Strong:** pushes back before designing. Which tickets? What share follows a known path? What happens on
the ones it cannot handle? What is the cost per ticket they can defend?

Ends up proposing routing: cheap workflow for the known majority, agent for the rest, human for the
ambiguous. See [Autonomy Ladder](../frameworks/autonomy-ladder.md).

### 2. "Justify a multi-agent architecture."

**Weak:** "Separation of concerns, each agent specialises."
**Strong:** states the [H× multiplier](../frameworks/handoff-multiplier.md) and what it buys. Knows every
handoff re-sends context, that the merge call is the most expensive one, and that adding agents does not fix
a bad prompt.

**Follow-up:** *"When would you collapse it back to a single agent?"*

### 3. "How locked in is the client?"

**Weak:** "It's all AWS, so pretty locked in" — or the opposite reflex, "it's portable".
**Strong:** itemises. Agent loops, tool design, RAG pipeline design and evaluation are portable. The
platform layer is not. Then describes how to structure a build so the lock-in stays narrow — tools behind
interfaces, prompts in files, evaluation harness framework-free.

See [Portability Matrix](../../docs/concepts/portability-matrix.md).

### 4. "Where does this cost money, and where does it cliff?"

**Weak:** "Per-token pricing, so it scales with usage."
**Strong:** knows cost is **not linear**. Names cliffs: retry storms, non-converging loops, unbounded
swarms, top-k inflation, idle infrastructure. Knows OpenSearch collections and AgentCore runtimes bill for
existing, not for use.

See [Cost Cliff Map](../frameworks/cost-cliff-map.md).

### 5. "The agent must never issue a refund. How do you guarantee that?"

**Weak:** "System prompt instruction, plus a guardrail."
**Strong:** *do not give it the tool.* Guarantee lives in IAM, not in prose. Then goes further —
decomposes into `assess_eligibility` (green) plus a human commit step, so the agent is just as useful and
cannot cost anything by being wrong.

This is the single best architect question. It separates people who think in prompts from people who think
in permissions.

## Design exercise

> *"Design an agent that answers HR policy questions for 5,000 employees. 20 minutes."*

**Listen for, in roughly this order:**

| Good architects raise | Weak answers skip |
| --- | --- |
| Who owns the policy corpus and how often it changes | ← almost always skipped |
| What happens when policy is ambiguous | ← the abstention question |
| PII in questions, not just answers | |
| Cost per query × 5,000 employees | |
| How they will know it is wrong | |
| Whether this needs an agent at all — search might do | ← the best answers start here |

The strongest candidates spend their first three minutes questioning the premise, then design quickly.

## Depth probes

| Area | Question |
| --- | --- |
| Retrieval | "Recall is fine but answers are wrong. Where do you look?" |
| Scaling | "1k → 100k documents. What breaks?" |
| Multi-tenancy | "How do you keep tenant A's data out of tenant B's context?" |
| Failover | "Primary model throttles. What happens, and how do you know?" |
| Evaluation | "Client says 'it just needs to be accurate'. Turn that into a gate." |
| Migration | "They are on LangChain and want Strands. Advise." |

## Red flags

- Designs before questioning the premise
- Treats prompts as a safety mechanism
- Cannot name a cost cliff
- Recommends multi-agent as a default
- No opinion on abstention
- Framework allegiance rather than framework reasoning

## Green flags

- Asks what happens when it is wrong, early and unprompted
- Distinguishes "portable concept" from "portable implementation"
- Talks about who operates it, not just who builds it
- Proposes the smallest thing that could work, then names what would justify more
- Says "this might not need an agent" when true

---

## If you are the candidate

Have one reference architecture you can draw from memory, with the cost model attached and the three
failure modes you consider most likely. Be able to say what you would cut first under a 50% budget cut.

**Study:** [Handoff Multiplier](../frameworks/handoff-multiplier.md) ·
[Blast Radius Grid](../frameworks/blast-radius-grid.md) ·
[Cost Cliff Map](../frameworks/cost-cliff-map.md) ·
[Portability Matrix](../../docs/concepts/portability-matrix.md) ·
[Architecture HLD](../../docs/architecture/)
