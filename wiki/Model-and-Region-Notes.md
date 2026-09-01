# Model & Region Notes

Community notes on what is actually available where, and what changed.

> ⚠️ **This page is deliberately not in the repository.** Model and region availability changes monthly; a versioned file would be wrong within a quarter and quietly mislead people. Here it can be corrected the moment somebody notices.
>
> **AWS is authoritative, not this page.** Always verify with the commands below before relying on anything written here.

---

## Verify it yourself — always start here

```bash
# models you can call in a region
aws bedrock list-foundation-models --region us-east-1 \
  --query 'modelSummaries[].modelId' --output table

# inference profile IDs — these are what you pass as modelId
aws bedrock list-inference-profiles --region us-east-1 \
  --query 'inferenceProfileSummaries[].[inferenceProfileId,status]' --output table
```

An **empty list is a permissions state**, not an outage — model access has not been granted in that region.

---

## The rules that do not change

These are stable even as the model list churns, which is why they are worth writing down:

1. **Access is per model, per region, on request.** Not automatic, and approval is not always instant.
2. **Many models require an inference profile ID**, not the bare model ID. The profile carries a geography prefix — `us.`, `eu.`, and others.
3. **A geographic profile routes across several regions**, and you need model access in **every** destination — not just the one you call from. This is why access failures can look intermittent.
4. **Feature availability lags model availability.** A region having a model does not mean it has Knowledge Bases, Guardrails or AgentCore.
5. **`us-east-1` has the widest support.** This curriculum is developed against it. Elsewhere, verify before starting a module.

---

## Region notes

| Region | Notes | Last checked | By |
| --- | --- | --- | --- |
| `us-east-1` | Curriculum baseline. Widest model and feature coverage | — | maintainer |
| `us-west-2` | Generally good coverage; verify AgentCore before Module 11 | — | — |
| `eu-*` | Model set differs; `eu.` profile prefix. Verify per module | — | — |
| `ap-*` | Verify before starting. Feature gaps more likely | — | — |

**Add a row when you verify one.** Region, what worked, what did not, and the date — the date is the important column.

---

## Feature availability, by module

Before starting a module in a non-baseline region, check the thing it actually needs:

| Module | Needs | Check |
| --- | --- | --- |
| [02 Bedrock](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/modules/02-bedrock-essentials) | Converse API, a chat model | `list-foundation-models` |
| [02 / 04](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/modules/04-agent-builder-and-knowledge-bases) | Knowledge Bases, Guardrails | Console — feature presence varies |
| [03 Bedrock Agents](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/modules/03-bedrock-agents) | Bedrock Agents + Lambda | Console |
| [10 Retrieval](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/modules/10-rag-opensearch-litellm) | OpenSearch Serverless, an embedding model | `aws opensearchserverless list-collections` |
| [11 AgentCore](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/modules/11-bedrock-agentcore) | AgentCore — **not available everywhere** | Console |

---

## Model choice, when the list changes under you

The [model selection cheat sheet](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/cheatsheets/quick-reference/model-selection.md) is deliberately written to survive this: choose on four dimensions (capability, latency, context, cost ceiling), record what you rejected and why, and re-decide on a stated trigger.

The one number worth carrying between models: **cost per *resolved* task**, not cost per token. A cheaper model needing two extra turns is not cheaper.

---

## Changes worth recording

When something changes in a way that breaks material here, note it — and open an [issue](https://github.com/akash-coded/aws-bedrock-agentcore-strands/issues/new/choose) so the repo can be fixed.

| Date | What changed | Affects | Reported by |
| --- | --- | --- | --- |
| — | — | — | — |

**AWS behaviour changing is the single highest-value thing to report here.** Nothing degrades teaching material faster.
