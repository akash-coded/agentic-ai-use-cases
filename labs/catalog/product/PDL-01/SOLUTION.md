# PDL-01 · Solution

## The tie-breaker: default down

When a case is genuinely borderline, build the **simpler** shape.

The asymmetry is what decides it. Building a workflow and discovering you needed an agent costs you a
rewrite of something small, and you now have evidence — you can point at the specific input where the
fixed sequence broke. Building an agent and discovering a workflow would have done costs you the rewrite
*plus* everything that accreted around the agent: the evaluation harness for non-determinism, the loop
caps, the topology, the observability, and a team that now describes the project as "our agent".

Organisations walk *up* the ladder easily and *down* it almost never. Start low.

## Why "branches on tool output" is the real question

"Is it complicated" is the question people actually ask, and it does not separate the cases. The
onboarding-pack example is complicated — many steps, varied order, language throughout — and it is a
workflow, because nothing it does depends on what a tool *returned*.

Runtime branching on tool output is the thing you cannot express as a fixed pipeline. Everything else,
however elaborate, is parameterisation.

## The two Break cases

They are inverses, and both are common:

- **"AI-powered intelligent document processing"** — maximum buzzword density, fixed pipeline, no
  language, no branching. A script. The name describes the ambition, not the control flow.
- **"Just answer questions about our docs"** — sounds like a search box. If answering means deciding
  whether to search policy or look up an account based on what the first lookup returned, it branches at
  runtime, and it is an agent.

Descriptions are written to persuade. Classify the control flow, not the pitch.

## Routing the hot path

`route_hot_path` is the highest-return line in this function. When 72% of traffic follows one known path,
sending that path through a deterministic workflow and reserving the agent for the remaining 28% typically
cuts cost by 40–70% with no measurable quality change on that path.

It is almost always available and almost never done first, because the agent gets built for the hard cases
and then inherits the easy ones by default.

## Defaults matter

The hidden checks require that an empty description classifies **down**. An unanswered question should
never silently promote a use case up the ladder — that is how "we haven't decided yet" becomes "it's an
agent" between two meetings.

## Field guide

[Autonomy Ladder](../../../../cheatsheets/frameworks/autonomy-ladder.md) ·
[Scope Fence](../../../../cheatsheets/frameworks/scope-fence.md) ·
[Idea brief](../../../../docs/prd/00-idea-brief.md) — the artefact this feeds
