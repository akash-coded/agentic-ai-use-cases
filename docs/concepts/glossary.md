# Glossary

Terms as they are used in this curriculum. Where an industry definition is contested, the reading used here
is stated plainly.

## A

**A2A (Agent-to-Agent)** — A protocol letting independently built agents discover each other's capabilities
and delegate work. Covered in [Module 12](../../modules/12-a2a-and-a2ui-interop/).

**A2UI** — A protocol for agents to drive real user interface rather than emitting text.

**Action group** — In Bedrock Agents, a set of operations an agent may call, described by an OpenAPI schema
and backed by Lambda.

**Agent** — A system where a model chooses the next action in a loop, including which tools to call and when
to stop. If the control flow is fixed in advance, it is a workflow, not an agent.

**AgentCore** — Amazon Bedrock's platform for running agents as services: Runtime, Memory, Identity,
Gateway and Observability.

**Agent card** — The A2A document describing what an agent can do and how to reach it.

## C

**Chunking** — Splitting documents before embedding. The highest-leverage decision in a RAG pipeline.

**Context window** — The token budget available on a single turn. See
[portable concepts](genai-core-concepts.md#3-the-context-window-is-a-budget-not-a-container).

**Contract test** — A test asserting the *shape* of an agent's output or tool call rather than its exact text.

**Converse API** — Bedrock's unified inference API. One message format across model families, with native
tool use.

**Critique loop** — A pattern where one agent produces and another reviews, iterating before returning.

## G

**Golden set** — A curated set of inputs with agreed acceptable outputs, used to evaluate a
non-deterministic system.

**Guardrail** — A declarative policy applied at inference time to block disallowed content or topics.

**Gate** — A pipeline step that blocks promotion when metrics fall below threshold. A gate that only warns
is not a gate.

## H

**Hybrid search** — Combining lexical (BM25) and dense (vector) retrieval, usually merged with reciprocal
rank fusion.

**HLD / LLD** — High-level and low-level design. See [`docs/architecture/`](../architecture/).

## I

**Inference profile** — A Bedrock construct routing a model call across regions for capacity. Requires a
regional prefix on the model ID (`us.`, `eu.`, `apac.`).

**Invariance test** — A test asserting behaviour stays stable across paraphrases of the same input.

## M

**MCP (Model Context Protocol)** — A standard for exposing tools and data to models, so an agent can
consume any compliant server.

**Memory** — Any engineering that makes a stateless model appear to remember. Buffer, summary, or vector.

## R

**RAG (Retrieval-Augmented Generation)** — Retrieving relevant text and placing it in the context window so
the model answers from your data.

**Reranking** — A second-stage model that reorders retrieved candidates for relevance. Costs latency; must
be measured, not assumed.

**RRF (Reciprocal Rank Fusion)** — A rank-merging method for combining retrieval strategies without tuning
score scales.

## S

**Strands** — AWS's open-source agent SDK. Used from [Module 05](../../modules/05-agent-loop-no-framework-to-strands/) onward.

**Swarm** — A multi-agent pattern where agents work in parallel on an open problem. Needs an explicit
termination condition.

## T

**Token** — The unit of cost, latency and context. Roughly ¾ of an English word; far less for code or JSON.

**Tool** — A function the model may call, described to it by name, description and JSON schema.

**TravelMind** — The running example across this curriculum: a travel-domain agent that grows from a single
Bedrock call into a deployed, gated, multi-agent service.

## V

**Verbosity tax** — The compounding token cost of an agent that says more than it needs to on every turn.
