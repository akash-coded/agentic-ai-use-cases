# AgentCore Console - Live Build Guide (Harness + Memory + Playground)

Build a full working agent on the Amazon Bedrock AgentCore console, click by click, then connect to it from code. Themed on TravelMind to match the cohort. Account `123456789012`, Region `us-east-1`.

> Status: the AgentCore **Managed Harness** is in public preview (since 22 Apr 2026). The flow and field values below are from current AWS docs. Button labels and panel layout can shift in preview, so read the label, not the pixel. Where a label may differ, the nearby text tells you what to click.

> Demo order that never leaves you stranded: do **Section 1 (Quick Create)** first so a working harness is on screen in under a minute. Then build the full thing manually in Sections 2 to 4. If the manual build hiccups live, you already have a working agent to fall back to.

---

## Section 0 - Pre-flight (2 minutes, before the room)

| Check | What to confirm | If wrong |
|---|---|---|
| Region | Top-right region is **N. Virginia (us-east-1)**. Harness preview runs only in us-east-1, us-west-2, eu-central-1, ap-southeast-2 | If the **Harness** tab is missing, you are in the wrong region. Switch to us-east-1 |
| Model access | Claude is usable in Bedrock (the model-access page was retired in late 2025, serverless models auto-enable) | If a model is greyed out, open Amazon Bedrock console and request access |
| Caller IAM | Your principal has `BedrockAgentCoreFullAccess` + `AmazonBedrockFullAccess` | See Appendix B if harness create/invoke is denied (preview action gap) |
| boto3 (for the code snippet) | `boto3 >= 1.43` so `invoke_harness` exists | `pip install -U boto3 botocore` |

Console entry point: AWS Console search bar, type **Bedrock AgentCore**, open it. Left sidebar shows **Runtime**, **Memory**, **Gateway**, **Identity**, **Observability**, and **Harness** (with a Preview tag).

---

## Section 1 - The 60-second safety net: Quick Create

Goal: a working agent on screen immediately.

1. Left sidebar > **Harness**.
2. Top-right > **Quick create harness**.
3. Wait a few seconds. It provisions a harness with recommended settings (default model **Claude Sonnet 4.6** on Bedrock, an auto-created execution role that already includes Browser and Code Interpreter) and drops you into the **Playground**.
4. In the chat box, type:
   ```
   In one sentence, what can you help an airline customer with?
   ```
5. It replies. You now have a running, managed agent with zero code. Leave this tab open.

What just happened (say this to the room): the harness bundled compute (a per-session microVM), the orchestration loop (powered by Strands), memory threading, tools, identity, and observability behind one resource. No container, no loop code.

---

## Section 2 - Build the Memory element

Memory is what lets a returning customer be remembered across sessions. Build it first so the harness can attach it.

1. Left sidebar > **Memory** > **Create memory**.
2. Fill in:

| Field | Value to type |
|---|---|
| Name | `travelmind-memory` |
| Description | `Cross-session memory for TravelMind support` |
| Event expiry (days) | `30` |

3. Add memory strategies (these are what extract durable facts). Add two:

| Strategy type | Name | Namespace |
|---|---|---|
| User Preferences | `Preferences` | `support/{actorId}/preferences` |
| Semantic | `Facts` | `support/{actorId}/facts` |

   `{actorId}` is a literal placeholder. AgentCore fills it per user at write time. Do not replace it.
4. **Create**. Status goes to **Creating**, then **Active** in 1 to 2 minutes.
5. Copy the **Memory ID** (looks like `travelmind-memory-XXXXXXXXXX`) and its ARN. You will attach this in Section 3.

Fallback if the console is slow live, one command does the same:
```bash
aws bedrock-agentcore-control create-memory \
  --name travelmind-memory \
  --event-expiry-duration 30 \
  --memory-strategies '[{"userPreferenceMemoryStrategy":{"name":"Preferences","namespaces":["support/{actorId}/preferences"]}},{"semanticMemoryStrategy":{"name":"Facts","namespaces":["support/{actorId}/facts"]}}]'
```

---

## Section 3 - Build the full Harness manually (touch every element)

This is the "configure everything" walkthrough. Each step below is one block in the harness configuration sidebar.

Left sidebar > **Harness** > **Create harness** (the full form, not Quick create).

**3.1 Name**
```
travelmind-support
```

**3.2 Model and system prompt**
- Model: pick **Claude Sonnet 4.5** (or keep the default Claude Sonnet 4.6). Any model your account can access works. For a cheaper demo pick **Claude Haiku 4.5**.
- System prompt (paste):
```
You are TravelMind, an airline customer support agent.
Help with flight status, cancellations, rebooking, refunds, baggage, and seat or meal preferences.
Use the customer's remembered preferences when you have them.
For any refund or fare calculation, compute the exact number with the code interpreter. Do not estimate money in your head.
Be concise and friendly. If you are unsure, say so.
```

**3.3 Memory**
- Open the **Memory** block. Choose **Connect an AgentCore Memory instance**.
- Select `travelmind-memory` (from Section 2).
- Effect: the harness saves and loads conversation context across sessions automatically. Without this, every session starts blank.

**3.4 Tools**
- Open the **Tools** block. Add (one click each, no Lambda, no schema):
  - **AgentCore Browser Tool** (`aws.browser.v1`) - lets the agent open and read web pages.
  - **Code Interpreter** - lets the agent run Python for exact math (the refund calc).
- You can also point at an MCP server, an AgentCore Gateway, or an inline function. Skip those for this demo.

**3.5 Skills** (optional, skip for the live demo)
- Skills are files mounted to the harness filesystem at a path like `.agent/skills/refund-policy.md`. The agent reads them at runtime. Mention it, do not build it live.

**3.6 Inbound Auth**
- Keep **Use IAM permissions** (the default). This means whoever calls `InvokeHarness` with valid AWS credentials is allowed. JWT (Cognito/Okta) is the alternative when you want end-user identity to flow through.

**3.7 Permissions (execution role)**
- This is the IAM role the harness assumes to call the model, tools, and memory.
- Easiest: let the console **auto-create** the execution role.
- Gotcha to pre-empt: the auto-created role covers the model, Browser, and Code Interpreter, but may not include **Memory** actions. Since you attached memory in 3.3, add the Memory add-on (Appendix A, "AgentCore Memory" block) to this role if memory calls fail. If you want zero surprises, attach the full role from Appendix A before creating.

**3.8 Advanced configurations (cost guardrails)**
- Open **Advanced configurations** > **Invocation limits**. Set caps so a runaway loop cannot burn tokens:

| Limit | Value |
|---|---|
| Max iterations (steps in the loop) | `15` |
| Timeout (seconds) | `300` |
| Max tokens per invocation | `4096` |

- Leave Network, Filesystem, Environment variables at defaults for the demo.

**3.9 Create**
- **Create harness**. Status goes **Creating** then **Ready** (about a minute).
- Copy the **harness ARN** from the detail page. It looks like:
  ```
  arn:aws:bedrock-agentcore:us-east-1:123456789012:harness/travelmind-support-XXXXXXXX
  ```

---

## Section 4 - Test it in the Playground (visual, no code)

1. Left sidebar > **Harness** > **Playground** tab.
2. From the dropdown, pick **travelmind-support**. A test session starts (note the harness ARN shown at the top).
3. Run these prompts in order. Each shows a different element.

| # | Paste this | What it proves |
|---|---|---|
| 1 | `My PNR is JX48Q2. I always want an aisle seat and a vegetarian meal.` | Sets a preference; the agent acknowledges and memory stores it |
| 2 | `My flight got cancelled. Rebook me on the next one. What seat and meal should you pick for me?` | Memory recall: it should choose aisle + vegetarian without being re-told |
| 3 | `My ticket was 18500 INR. Cancellation fee is 12 percent and taxes of 2400 INR are refundable. What is my exact refund?` | Code Interpreter: it runs Python and returns the exact number (16280 + 2400 = compute live) |
| 4 | `Open https://example.com and tell me the main heading on the page.` | Browser tool: it fetches a live page and reports the heading |

4. Point out the per-turn **token and latency metrics** next to each response, and the **Configs panel** on the right. From that panel you can swap the model (Bedrock, OpenAI, Gemini), edit the system prompt, or toggle tools **for this session only**, without editing the harness. Great for "what if we used Haiku instead" live.

Memory across sessions: start a **new** session in the Playground, ask prompt 2 again. Because the harness is connected to `travelmind-memory`, the preference from the earlier session is recalled.

---

## Section 5 - Connect from your code (the snippet)

Once the harness exists, calling it is tiny. Same loop as the Playground, driven from Python.

```python
import boto3, uuid

client = boto3.client("bedrock-agentcore", region_name="us-east-1")

resp = client.invoke_harness(
    # paste your harness ARN from Section 3.9
    harnessArn="arn:aws:bedrock-agentcore:us-east-1:123456789012:harness/travelmind-support-XXXXXXXX",
    # same id across calls = the harness threads the conversation server-side. Must be >= 33 chars.
    runtimeSessionId="travelmind-" + uuid.uuid4().hex,
    messages=[{"role": "user",
               "content": [{"text": "My PNR is JX48Q2 and my flight was cancelled. What are my options?"}]}],
)

for event in resp["stream"]:
    if "contentBlockDelta" in event:
        delta = event["contentBlockDelta"].get("delta", {})
        if "text" in delta:
            print(delta["text"], end="", flush=True)
    elif "runtimeClientError" in event:
        print("\nERROR:", event["runtimeClientError"]["message"])
```

Notes:
- The model, prompt, tools, and memory all come from the harness config. Override any of them per call with the `model`, `systemPrompt`, or `tools` arguments on `invoke_harness`.
- If you do not set a model anywhere, the harness defaults to Claude Sonnet 4.6.
- `runtimeSessionId` must be 33+ characters. `"travelmind-" + uuid4().hex` is 43, so you are safe.

CLI one-liner (same thing from a terminal):
```bash
agentcore invoke --harness travelmind-support \
  --session-id "$(uuidgen)" \
  "My PNR is JX48Q2 and my flight was cancelled. What are my options?"
```

Find the harness ARN any time:
```bash
aws bedrock-agentcore-control list-harnesses
```

---

## Section 6 - Observability (where to look)

- Harness detail page > **Observability** panel: runtime sessions, invocations, error rate, throttle rate, vCPU and memory consumption (the metrics you are billed on).
- **Log delivery** dropdown on the same panel sends logs to **CloudWatch Logs**, **S3**, or **Data Firehose**. No subscription filters to wire up.
- The invoke response stream is itself structured observability: it emits the model's reasoning, each tool call and its result, and token/latency metadata.

---

## Section 7 - Cleanup (avoid charges)

Console: **Harness** > select `travelmind-support` > **Delete**. Then **Memory** > select `travelmind-memory` > **Delete**.

Or by command:
```bash
aws bedrock-agentcore-control delete-harness --harness-id travelmind-support-XXXXXXXX
aws bedrock-agentcore-control delete-memory  --memory-id  travelmind-memory-XXXXXXXXXX
```

Memory has its own meter (events, storage, retrievals), so deleting it matters more than deleting the harness.

---

## Section 8 - Failure playbook (anticipated)

| Symptom | Cause | Fix |
|---|---|---|
| No **Harness** tab in the console | Wrong region | Switch to **us-east-1** (or us-west-2 / eu-central-1 / ap-southeast-2) |
| `AccessDenied` on **Create harness** or **Invoke** | Preview action gap: `InvokeHarness` needs both `bedrock-agentcore:InvokeHarness` and `:InvokeAgentRuntime`; `CreateHarness` needs `:CreateHarness` and `:CreateAgentRuntime`. The managed policy may predate these | Attach the inline policy in **Appendix B** |
| Harness stuck, never reaches **Ready** | Execution role or model access problem | Check the role exists and the trust policy allows `bedrock-agentcore.amazonaws.com`; confirm model access; check CloudTrail for the denied action |
| Agent answers but **ignores memory** | Memory not attached, or execution role lacks memory actions | Re-check Section 3.3; add the Memory add-on (Appendix A) to the execution role |
| Code interpreter / browser tool not firing | Tool not attached, or role lacks the tool actions | Re-add the tool in Section 3.4; the base role in Appendix A includes Browser + Code Interpreter actions |
| `invoke_harness` not found in Python | boto3 too old | `pip install -U boto3 botocore` (need >= 1.43) |
| `ValidationException` on invoke about session id | `runtimeSessionId` shorter than 33 chars | Use a UUID, e.g. `"travelmind-" + uuid4().hex` |
| Picked OpenAI or Gemini and it fails | Non-Bedrock providers need an API key stored as an AgentCore Identity credential provider | Stay on Bedrock for the demo, or add an API key credential provider and the add-on in Appendix A |
| Bill higher than expected | Token usage is 5 to 10x your guess (reasoning + tool payloads flow through the model); memory events and retrievals are metered | Set the invocation limits in Section 3.8; delete memory after the demo |
| Refund number looks wrong | The model estimated instead of computing | Confirm the system prompt forces code-interpreter math and that the tool is attached |

---

## Appendix A - Harness execution role (copy-paste)

Trust policy (lets AgentCore assume the role):
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {"Service": "bedrock-agentcore.amazonaws.com"},
    "Action": "sts:AssumeRole"
  }]
}
```

Base permissions (model + Browser + Code Interpreter + logs + metrics; replace region/account if needed):
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {"Sid":"BedrockModel","Effect":"Allow",
     "Action":["bedrock:InvokeModel","bedrock:InvokeModelWithResponseStream"],
     "Resource":["arn:aws:bedrock:*::foundation-model/*","arn:aws:bedrock:us-east-1:123456789012:*"]},
    {"Sid":"EcrPublicToken","Effect":"Allow","Action":["ecr-public:GetAuthorizationToken"],"Resource":"*"},
    {"Sid":"StsBearer","Effect":"Allow","Action":["sts:GetServiceBearerToken"],"Resource":"*"},
    {"Sid":"XRay","Effect":"Allow",
     "Action":["xray:PutTraceSegments","xray:PutTelemetryRecords","xray:GetSamplingRules","xray:GetSamplingTargets"],"Resource":"*"},
    {"Sid":"LogsGroup","Effect":"Allow","Action":["logs:CreateLogGroup","logs:DescribeLogStreams"],
     "Resource":"arn:aws:logs:us-east-1:123456789012:log-group:/aws/bedrock-agentcore/runtimes/*"},
    {"Sid":"LogsDescribe","Effect":"Allow","Action":["logs:DescribeLogGroups"],
     "Resource":"arn:aws:logs:us-east-1:123456789012:log-group:*"},
    {"Sid":"LogsStream","Effect":"Allow","Action":["logs:CreateLogStream","logs:PutLogEvents"],
     "Resource":"arn:aws:logs:us-east-1:123456789012:log-group:/aws/bedrock-agentcore/runtimes/*:log-stream:*"},
    {"Sid":"Metrics","Effect":"Allow","Action":"cloudwatch:PutMetricData","Resource":"*",
     "Condition":{"StringEquals":{"cloudwatch:namespace":"bedrock-agentcore"}}},
    {"Sid":"WorkloadIdentity","Effect":"Allow",
     "Action":["bedrock-agentcore:GetWorkloadAccessToken","bedrock-agentcore:GetWorkloadAccessTokenForJWT"],"Resource":["*"]},
    {"Sid":"Browser","Effect":"Allow",
     "Action":["bedrock-agentcore:StartBrowserSession","bedrock-agentcore:StopBrowserSession","bedrock-agentcore:GetBrowserSession","bedrock-agentcore:ListBrowserSessions","bedrock-agentcore:UpdateBrowserStream","bedrock-agentcore:ConnectBrowserAutomationStream","bedrock-agentcore:ConnectBrowserLiveViewStream"],
     "Resource":"arn:aws:bedrock-agentcore:us-east-1:aws:browser/*"},
    {"Sid":"CodeInterpreter","Effect":"Allow",
     "Action":["bedrock-agentcore:StartCodeInterpreterSession","bedrock-agentcore:StopCodeInterpreterSession","bedrock-agentcore:GetCodeInterpreterSession","bedrock-agentcore:ListCodeInterpreterSessions","bedrock-agentcore:InvokeCodeInterpreter"],
     "Resource":"arn:aws:bedrock-agentcore:us-east-1:aws:code-interpreter/*"}
  ]
}
```

Memory add-on (attach if you connect AgentCore Memory, as in Section 3.3):
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid":"AgentCoreMemory","Effect":"Allow",
    "Action":["bedrock-agentcore:CreateEvent","bedrock-agentcore:DeleteEvent","bedrock-agentcore:GetEvent","bedrock-agentcore:ListEvents","bedrock-agentcore:RetrieveMemoryRecords"],
    "Resource":"arn:aws:bedrock-agentcore:*:*:memory/*"
  }]
}
```

Create the role and attach the base policy:
```bash
cat > harness-trust.json <<'EOF'
{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"bedrock-agentcore.amazonaws.com"},"Action":"sts:AssumeRole"}]}
EOF
aws iam create-role --role-name BedrockAgentCoreTravelMindRole \
  --assume-role-policy-document file://harness-trust.json
# save the base permissions JSON above to harness-exec.json, then:
aws iam put-role-policy --role-name BedrockAgentCoreTravelMindRole \
  --policy-name harnessExec --policy-document file://harness-exec.json
```
Then in Section 3.7, choose this role instead of auto-create. Its ARN: `arn:aws:iam::123456789012:role/BedrockAgentCoreTravelMindRole`.

---

## Appendix B - Caller inline policy (if harness actions are denied)

The harness is in preview, so the managed `BedrockAgentCoreFullAccess` may not yet include the new harness actions. If create or invoke is denied, attach this to your principal (the group `bedrock-lab` or your user):
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "HarnessPreviewActions",
    "Effect": "Allow",
    "Action": [
      "bedrock-agentcore:CreateHarness",
      "bedrock-agentcore:GetHarness",
      "bedrock-agentcore:ListHarnesses",
      "bedrock-agentcore:UpdateHarness",
      "bedrock-agentcore:DeleteHarness",
      "bedrock-agentcore:InvokeHarness",
      "bedrock-agentcore:CreateAgentRuntime",
      "bedrock-agentcore:UpdateAgentRuntime",
      "bedrock-agentcore:DeleteAgentRuntime",
      "bedrock-agentcore:InvokeAgentRuntime"
    ],
    "Resource": "*"
  }]
}
```
```bash
cat > harness-caller.json <<'EOF'
<paste the JSON above>
EOF
aws iam put-group-policy --group-name bedrock-lab \
  --policy-name HarnessPreviewActions --policy-document file://harness-caller.json
```
Scope `Resource` to your harness ARN for production.

---

## Console map (us-east-1)

| Element | Where |
|---|---|
| Harness, Playground | Bedrock AgentCore > Harness |
| Memory | Bedrock AgentCore > Memory |
| Runtime (code-based agents) | Bedrock AgentCore > Runtime |
| Gateway, Identity | Bedrock AgentCore > Gateway / Identity |
| Guardrails | Amazon Bedrock > Guardrails |
| Traces, metrics | CloudWatch > Transaction Search / GenAI Observability, plus the harness Observability panel |
