# Troubleshooting

The errors this curriculum actually produces, in the order you will meet them.

## Access and identity

**`AccessDeniedException` on any Bedrock call**

Model access is granted per model, **per region**. Enable it under Bedrock → Model access in the region you
are calling. If you are using a geographic inference profile, you need access in *every* region that
profile routes to — a profile that fans out to three regions needs access in all three.

**Empty model list from `list-foundation-models`**

Same cause. This is a permissions state, not an outage.

**`UnrecognizedClientException` / `InvalidSignatureException`**

Credentials are wrong or expired. `aws sts get-caller-identity` is the fastest check.

## Model IDs and invocation

**`ValidationException` mentioning the model identifier**

Almost always the inference profile. Many models must be invoked through a cross-Region inference profile
ID (carrying a geography prefix such as `us.` or `eu.`) rather than the bare model ID. List what your
region actually offers:

```bash
aws bedrock list-inference-profiles --region us-east-1 \
  --query 'inferenceProfileSummaries[].inferenceProfileId' --output table
```

Use that value as `modelId`.

**`AttributeError` — the client has no such method**

Four different Bedrock clients, four different jobs:

| Client | Use it for |
| --- | --- |
| `bedrock` | Managing models, guardrails, knowledge base configuration |
| `bedrock-runtime` | `Converse`, `InvokeModel` — actually calling a model |
| `bedrock-agent` | Creating and configuring agents |
| `bedrock-agent-runtime` | `InvokeAgent`, `Retrieve` — actually calling an agent or KB |

Calling `converse` on a `bedrock` client is the most common version of this.

**`ThrottlingException` or `503 Service Unavailable`**

Capacity, not correctness. Retry with backoff, use a cross-Region inference profile to spread load, or move
to a quieter region.

## Conversation and tool use

**The model repeats a tool call, or answers as if the tool never ran**

You dropped the assistant's `toolUse` message from the history. The sequence must be: assistant message
containing the `toolUse` block → user message containing the `toolResult` block → next `Converse` call.
Both turns. See the [Module 02 LLD](../architecture/lld/02-bedrock-essentials.md).

**The model calls the wrong tool, or fills arguments badly**

The tool description is the bug. The model never sees your function — only name, description and schema.
Rewrite the description for the model.

**`ValidationException` on message ordering**

Roles must alternate. Two consecutive user messages, or a conversation starting with an assistant message,
are rejected.

## Agents

**Bedrock Agent cannot invoke its Lambda**

The Lambda needs a resource-based policy allowing `bedrock.amazonaws.com` to invoke it. The trace shows
`AccessDeniedException` at the action-group step.

**Agent returns an error observation from a working Lambda**

Response shape. It must be
`{"response": {"actionGroup", "apiPath", "httpMethod", "httpStatusCode", "responseBody"}}`.

**Agent ignores its instructions**

Usually length. Long instructions get diluted, and you pay for them on every turn.

## Knowledge bases and RAG

**Answers with no citations**

Grounding did not happen — the model answered from parametric knowledge. Treat an uncited policy claim as
a failure, not a fallback.

**Correct-looking answers that contradict the source**

Check ingestion freshness before blaming the model. A knowledge base does not re-sync on its own after the
source changes.

**Retrieval returns nothing relevant**

Usually chunking. If the answer spans a chunk boundary, no retriever can win. See the
[Module 10 LLD](../architecture/lld/10-rag-opensearch-litellm.md).

## AgentCore

**Deploy succeeds, invoke fails**

Check the runtime role. Over-broad roles fail late and confusingly; under-scoped roles fail at the first
downstream call.

**Memory grows without bound**

No retention policy. Set a TTL — this is a cost decision, not a technical one.

## Still stuck

Search [existing discussions](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions),
then open a new **Q&A** discussion with the module, the exact error, and what you already tried.
