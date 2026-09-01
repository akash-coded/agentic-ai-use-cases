# Error Index

Every error this material produces, by the string you actually see. **Search this page for your error text** — that is what it is for.

> **Relationship to the repo.** [`docs/setup/troubleshooting.md`](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/docs/setup/troubleshooting.md) is the curated, versioned subset that ships with the material. This page is the growing superset: anyone can add an error the moment they hit one, no pull request. When an entry proves common, it gets promoted into the repo.

**Adding one?** Four columns, and the third is the one people skip. [How to edit](Contributing-to-this-Wiki).

---

## Access and identity

### `AccessDeniedException` — on any Bedrock call
**Cause.** Model access is granted per model, **per region**, on request.
**Fix.** Bedrock → Model access → Modify → select → submit, in the region you are calling.
**The part that catches people twice:** if you use a cross-Region inference profile, you need access in **every** region it routes to. A profile fanning out to three regions needs access in all three, which makes the failure look intermittent — it depends where the request landed.

### `AccessDeniedException` — only sometimes, same code
**Cause.** Almost always the above: a geographic inference profile routing to a region where you lack access.
**Fix.** `aws bedrock list-inference-profiles` and check each destination region.

### Empty list from `list-foundation-models`
**Cause.** Not an outage. Model access has not been granted in that region.
**Fix.** As above. An empty list is a permissions state.

### `UnrecognizedClientException` / `InvalidSignatureException`
**Cause.** Credentials wrong or expired.
**Fix.** `aws sts get-caller-identity` — if it does not name your account, fix credentials before anything else.

---

## Model IDs and invocation

### `ValidationException: Invocation of model ID … with on-demand throughput isn't supported`
**Cause.** You passed a bare model ID where an **inference profile ID** is required. Profile IDs carry a geography prefix — `us.`, `eu.` and others.
**Fix.**
```bash
aws bedrock list-inference-profiles --region us-east-1 \
  --query 'inferenceProfileSummaries[].inferenceProfileId' --output table
```
Use that value as `modelId`.
**Also:** if you scope IAM, grant **both** the profile ARN and the underlying foundation-model ARNs. Granting only the profile is a common cause of a confusing denial. ([Full answer](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/59))

### `AttributeError: 'Bedrock' object has no attribute 'converse'`
**Cause.** Wrong client. Four clients, four jobs:

| Client | For |
| --- | --- |
| `bedrock` | Managing models, guardrails, KB config |
| `bedrock-runtime` | `converse`, `invoke_model` — **calling a model** |
| `bedrock-agent` | Creating and configuring agents |
| `bedrock-agent-runtime` | `invoke_agent`, `retrieve` — **calling an agent or KB** |

### `ValidationException` mentioning messages or roles
**Cause.** Roles must alternate. Two consecutive `user` messages, or a conversation starting with `assistant`, are rejected.
**Fix.** `print([m["role"] for m in messages])` before the call. Usually the tool-result loop appending two user turns.

### `ThrottlingException` / `503 Service Unavailable`
**Cause.** Capacity, not correctness.
**Fix.** Backoff and retry; use a cross-Region inference profile to spread load; or move region. Log which model answered so failover is not silent.

---

## The agent loop

### The model asks for the same tool twice, identically
**Cause.** You appended the tool result but **not the assistant message that requested it**. From the model's side it never asked, so the reply has nothing to attach to.
**Fix.** Append the assistant message verbatim first, then a user message with the `toolResult`.
**Detect it in 30 seconds:** `print([m["role"] for m in messages])` — `['user','user']` is the tell.
[Full answer](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/58) · [AGL-02 lab](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/labs/catalog/agent-loop/AGL-02)

### `TypeError: f() got an unexpected keyword argument`
**Cause.** The model hallucinated a parameter name; `**args` raised.
**Fix.** Catch it in the dispatcher and return an error result naming the valid arguments, so the model can self-correct. Never let it escape the loop.

### `SystemExit` kills the whole run
**Cause.** `except Exception` does not catch `SystemExit` or `KeyboardInterrupt` — they inherit from `BaseException`. A dependency calling `sys.exit()` on a config problem takes your agent with it.
**Fix.** In a dispatcher, `except BaseException` is correct. It is a boundary, and boundaries catch everything.

### The loop never terminates
**Cause.** No iteration cap, or the model is oscillating — same call, same arguments, repeatedly.
**Fix.** A counter in the code, not an instruction in the prompt. Detect a repeated call signature (name **and** arguments) and stop early. [AGL-03 lab](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/labs/catalog/agent-loop/AGL-03)

---

## Agents and action groups

### Bedrock Agent silently cannot call its Lambda
**Cause.** Missing resource-based policy on the Lambda. Shows as `AccessDeniedException` **inside the trace**, not as a top-level error.
**Fix.**
```bash
aws lambda add-permission --function-name YOUR_FN \
  --statement-id bedrock-agent-invoke --action lambda:InvokeFunction \
  --principal bedrock.amazonaws.com \
  --source-arn arn:aws:bedrock:us-east-1:123456789012:agent/AGENTID
```

### Agent returns an error observation from a working Lambda
**Cause.** Response shape.
**Fix.** Must be `{"response": {"actionGroup", "apiPath", "httpMethod", "httpStatusCode", "responseBody"}}`.

---

## Retrieval

### Answers with no citations
**Cause.** The model answered from parametric memory. Retrieval may have run and been ignored.
**Fix.** Assert a citation on every factual claim as a contract test; instruct abstention when retrieval is empty.

### Citations present but the passage does not support the claim
**Cause.** Citation theatre. Models are good at naming a plausible passage for an answer they generated independently.
**Fix.** Human-read five cited passages per release. Flag answers citing 3+ sources for one specific claim. [Full answer](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/62) · [Grounding Triangle](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/cheatsheets/frameworks/grounding-triangle.md)

### Confidently wrong answers about policy
**Cause.** A tool returned `[]` and the model read "I found nothing" as "nothing applies".
**Fix.** Tools return `{"status": "no_matches", "advice": "…"}`, never a bare empty list. [TOOL-03 lab](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/labs/catalog/tools/TOOL-03)

### Retrieval quality decayed as the corpus grew
**Cause.** Recall fell at fixed `top_k` as competition increased.
**Fix.** Re-measure recall@k. Improve ranking rather than just raising k — the accuracy curve peaks and then falls.

---

## Cost and platform

### The bill grew with no traffic change
**Cause.** Usually idle infrastructure. OpenSearch Serverless collections and AgentCore runtimes bill for **existing**.
**Fix.** [Teardown checklist](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/docs/setup/cost-controls.md#teardown-checklist). Also check turns per task — a retry storm or an uncapped loop multiplies four token taxes at once.

### Quality dropped with no deploy
**Cause.** Model failover to a smaller model, or a provider-side model update.
**Fix.** Log which model answered on every response. Pin the model in a version manifest. [PROD-02 lab](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/labs/catalog/production/PROD-02)

### AgentCore deploy succeeds, invoke fails
**Cause.** Runtime role missing a downstream permission.
**Fix.** Scope per tool rather than per agent, and check each downstream ARN.

---

## Labs and local environment

### `SyntaxError: f-string expression part cannot include a backslash`
**Cause.** Python 3.11 running a file that needs 3.12. Only the notebook-generator scripts under `labs/rag-labs/build/` require 3.12.
**Fix.** Use 3.12 for those; the labs themselves run on 3.11.

### `labctl` says "no solution yet"
**Fix.** `python labs/runner/labctl.py start <ID>` copies the starter into your workspace first.

### `labctl verify` fails on a lab you wrote
**Cause.** One of the two rules: your reference must pass all three phases, and your starter must **fail** the public checks.
**Fix.** If the starter passes, the TODOs do not need doing. [Authoring guide](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/labs/CONTRIBUTING-A-LAB.md)

---

## Adding an entry

```markdown
### `the exact error string`
**Cause.** What is actually wrong.
**Fix.** The command or change.
**How you found it.** ← the most valuable line. What led you to the cause?
```

Errors are indexed by search engines. Paste the **exact** string, including punctuation, so the next person finds it.
