# 🏛️ Solutions Architect

**For:** you design agent systems, review other people's, and answer for the cost. **Time:** ~45 hours.
**Finish line:** an architecture you can defend on cost, failure modes and lock-in.

You will run fewer notebooks than the [engineer path](agent-engineer.md) and read more design material —
but you still run the ones that teach a trade-off, because a trade-off you have not felt is one you will
get wrong.

## 1 · Decision frameworks — 6 h

- [Module 00](../../modules/00-agentic-foundations/) in full. The classifier and failure-pattern
  diagnostic are the tools you will use on every review.
- [Module 15](../../modules/15-agentic-product-lifecycle/) — artefacts and gates.

## 2 · The AWS surface — 10 h

- [Module 02](../../modules/02-bedrock-essentials/) — read all decks, run
  [`converse_api_masterclass.ipynb`](../../modules/02-bedrock-essentials/notebooks/converse_api_masterclass.ipynb).
- [Module 03](../../modules/03-bedrock-agents/) — run
  [`02_handbuilt_loop.ipynb`](../../modules/03-bedrock-agents/notebooks/02_handbuilt_loop.ipynb).
  Understanding what the managed loop does is the whole point.
- [Module 04](../../modules/04-agent-builder-and-knowledge-bases/) — decks only.
- [AWS service map](../concepts/aws-service-map.md) and
  [portability matrix](../concepts/portability-matrix.md).

## 3 · Framework and topology trade-offs — 12 h

- [Module 05](../../modules/05-agent-loop-no-framework-to-strands/) — run the hand-built loop. Yes, really.
- [Module 07](../../modules/07-strands-multi-agent-patterns/) — run
  [`PierPoint_Release_Desk_Graph_vs_Swarm.ipynb`](../../modules/07-strands-multi-agent-patterns/notebooks/PierPoint_Release_Desk_Graph_vs_Swarm.ipynb),
  the head-to-head comparison, and fill the
  [pattern selector](../../modules/06-strands-foundations/activities/MultiAgent_Pattern_Selector.xlsx).
- [Module 08](../../modules/08-langchain-and-langgraph/) — the
  [side-by-side notebook](../../modules/08-langchain-and-langgraph/notebooks/06_langchain_vs_strands_side_by_side.ipynb) only.

## 4 · Retrieval architecture — 6 h

- [Module 10](../../modules/10-rag-opensearch-litellm/) — the
  [index design](../../modules/10-rag-opensearch-litellm/labs/rag-labs/03_index_design.ipynb) and
  [evaluation gate](../../modules/10-rag-opensearch-litellm/labs/rag-labs/06_evaluation_gate.ipynb) labs,
  plus [tokens and cost](../../modules/10-rag-opensearch-litellm/labs/rag-labs/07_tokens_cost.ipynb).

## 5 · Platform and production — 11 h

- [Module 11](../../modules/11-bedrock-agentcore/) — decks, the
  [three-way deploy](../../modules/11-bedrock-agentcore/notebooks/01_build_an_agent_three_ways.ipynb),
  and the [cost and capacity workbench](../../modules/11-bedrock-agentcore/activities/AgentCore_Cost_and_Capacity_Workbench.xlsx).
- [Module 14](../../modules/14-end-to-end-production/) — the
  [reference architecture](../../modules/14-end-to-end-production/assets/reference_architecture.png),
  [release pipeline](../../modules/14-end-to-end-production/src/release_pipeline.md) and
  [readiness checklist](../../modules/14-end-to-end-production/src/readiness_checklist.md).
- [Architecture HLD](../architecture/) and every [LLD](../architecture/lld/).

## Finish line

Produce, for a real use case: an HLD diagram, a cost model with the four drivers named, a topology choice
with its multiplier, a lock-in assessment, and the three failure modes you consider most likely with their
detection method. The [LLD pages](../architecture/lld/) are the template.
