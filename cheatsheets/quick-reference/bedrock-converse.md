# Bedrock Converse API — Cheat Sheet

The one API that carries you from hello-world to tool use to retrieval. Learn it properly once.

---

## The four clients — pick the right one

| Client | Operations | Use for |
| --- | --- | --- |
| `bedrock` | `list_foundation_models`, guardrail + KB **config** | Managing things |
| `bedrock-runtime` | `converse`, `converse_stream`, `invoke_model` | **Calling a model** |
| `bedrock-agent` | `create_agent`, `create_knowledge_base` | Managing agents |
| `bedrock-agent-runtime` | `invoke_agent`, `retrieve`, `retrieve_and_generate` | **Calling an agent or KB** |

> Calling `.converse()` on a `bedrock` client is the single most common first-hour error.

## Minimal call

```python
import boto3
brt = boto3.client("bedrock-runtime", region_name="us-east-1")

resp = brt.converse(
    modelId="us.anthropic.claude-sonnet-4-5-20250929-v1:0",   # note the us. prefix
    messages=[{"role": "user", "content": [{"text": "Explain tokenisation in two sentences."}]}],
    inferenceConfig={"maxTokens": 512, "temperature": 0.2},
)
print(resp["output"]["message"]["content"][0]["text"])
print(resp["usage"])        # {'inputTokens':…, 'outputTokens':…, 'totalTokens':…}
print(resp["stopReason"])   # end_turn | tool_use | max_tokens | stop_sequence
```

**Always read `usage`.** It is the only honest source for [token accounting](../frameworks/token-tax-ledger.md).

## Model IDs and inference profiles

Many models must be called through a cross-Region **inference profile**, whose ID carries a geography
prefix (`us.`, `eu.`, …). Passing the bare model ID raises `ValidationException`.

```bash
aws bedrock list-inference-profiles --region us-east-1 \
  --query 'inferenceProfileSummaries[].inferenceProfileId' --output table
```

Use whatever that returns as `modelId`. With a geographic profile you need model access in **every** region
it routes to.

## Message shape

```python
{"role": "user" | "assistant",
 "content": [ {"text": "..."},
              {"image":  {"format": "png",  "source": {"bytes": b"..."}}},
              {"document": {"format": "pdf", "name": "policy", "source": {"bytes": b"..."}}} ]}
```

Roles must **alternate**. A conversation cannot start with `assistant`. Two consecutive `user` messages are
rejected.

System prompt is a separate argument, not a message:

```python
brt.converse(modelId=..., system=[{"text": "You are…"}], messages=[...])
```

## Tool use — the round trip everyone gets wrong

```python
tool_config = {"tools": [{"toolSpec": {
    "name": "get_booking",
    "description": ("Retrieve a single booking by reference: passenger, itinerary, fare class, status. "
                    "Does NOT contain refund eligibility — use get_fare_rules for that."),
    "inputSchema": {"json": {
        "type": "object",
        "properties": {"booking_ref": {"type": "string", "description": "Six-character reference, e.g. XY7Q2M"}},
        "required": ["booking_ref"]}}}}]}

messages = [{"role": "user", "content": [{"text": "Is booking XY7Q2M refundable?"}]}]
resp = brt.converse(modelId=MID, messages=messages, toolConfig=tool_config)

while resp["stopReason"] == "tool_use":
    # 1. append the ASSISTANT message verbatim — this is the step people skip
    messages.append(resp["output"]["message"])

    # 2. run each requested tool
    results = []
    for block in resp["output"]["message"]["content"]:
        if "toolUse" not in block:
            continue
        tu = block["toolUse"]
        try:
            out = dispatch(tu["name"], tu["input"])
            results.append({"toolResult": {"toolUseId": tu["toolUseId"],
                                           "content": [{"json": out}], "status": "success"}})
        except Exception as e:
            # fail loudly — an empty result reads as "nothing applies"
            results.append({"toolResult": {"toolUseId": tu["toolUseId"],
                                           "content": [{"text": f"error: {e}"}], "status": "error"}})

    # 3. append results as a USER message
    messages.append({"role": "user", "content": results})
    resp = brt.converse(modelId=MID, messages=messages, toolConfig=tool_config)

print(resp["output"]["message"]["content"][0]["text"])
```

**The two rules:** append the assistant message *before* the tool result, and every `toolResult` must carry
the matching `toolUseId`.

Force a specific tool with `toolConfig["toolChoice"] = {"tool": {"name": "get_booking"}}`; require any tool
with `{"any": {}}`; default is `{"auto": {}}`.

## Streaming

```python
stream = brt.converse_stream(modelId=MID, messages=messages)
for ev in stream["stream"]:
    if "contentBlockDelta" in ev:
        print(ev["contentBlockDelta"]["delta"].get("text", ""), end="", flush=True)
    elif "metadata" in ev:
        print("\n", ev["metadata"]["usage"])
```

Streaming does not reduce total latency — it reduces *perceived* latency, which is often what matters. See
[Three Clocks](../frameworks/three-clocks.md).

## Guardrails

```python
resp = brt.converse(
    modelId=MID, messages=messages,
    guardrailConfig={"guardrailIdentifier": "abc123", "guardrailVersion": "1", "trace": "enabled"})

if resp["stopReason"] == "guardrail_intervened":
    ...  # inspect resp["trace"]["guardrail"] for the triggering policy
```

## Retrieval — the agent-runtime side

```python
bar = boto3.client("bedrock-agent-runtime")
r = bar.retrieve(knowledgeBaseId="KB123",
                 retrievalQuery={"text": "refund policy for cancelled flights"},
                 retrievalConfiguration={"vectorSearchConfiguration": {"numberOfResults": 5}})
for res in r["retrievalResults"]:
    print(res["score"], res["content"]["text"][:120], res["location"])
```

Keep `location` — it is what makes a citation checkable. See
[Grounding Triangle](../frameworks/grounding-triangle.md).

## Error decoder

| Error | Cause | Fix |
| --- | --- | --- |
| `AccessDeniedException` | Model access not granted in this region | Bedrock → Model access |
| `ValidationException` (model id) | Needs an inference profile ID | `list-inference-profiles` |
| `ValidationException` (messages) | Roles not alternating | Check the sequence |
| `ThrottlingException` / 503 | Capacity | Backoff; cross-Region profile |
| `AttributeError: converse` | Wrong client | Use `bedrock-runtime` |

Fuller list: [troubleshooting](../../docs/setup/troubleshooting.md).

## Learn it properly

[Module 02](../../modules/02-bedrock-essentials/) ·
[Converse masterclass](../../modules/02-bedrock-essentials/notebooks/converse_api_masterclass.ipynb) ·
[Module 02 LLD](../../docs/architecture/lld/02-bedrock-essentials.md)
