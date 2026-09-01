# Day 6 — Live-AWS Runbook: Deploy the TravelMind Agent to AgentCore

Deploy the `travelmind_agent.py` your notebook wrote, from a working laptop to a live AgentCore Runtime endpoint. Every step lists the **exact command or click** and the **expected output**. If a step's output does not match, jump to the **Failure → Fix** table at the end.

> AgentCore and its toolkit move fast (parts are still labelled preview). Command names are stable; the **interactive prompt wording in `configure` may differ slightly** in your version. Match the intent, not the exact string.

**Constants used throughout**

| Thing | Value |
|---|---|
| Region | `us-west-2` |
| Model id | `us.anthropic.claude-sonnet-4-5-20250929-v1:0` (a `us.` inference profile) |
| Agent file | `travelmind_agent.py` (written by the lab notebook, Section 5) |
| Config file written by toolkit | `.bedrock_agentcore.yaml` (hidden) |

---

## 0 · Prerequisites (≈2 min)

- Time-boxed **admin AWS access** for this session (you have it).
- `travelmind_agent.py` and `requirements.txt` from the notebook, in your current folder.
- Python 3.10+ and a terminal.

```bash
python --version          # 3.10 or higher
ls travelmind_agent.py    # the file the notebook wrote
```

Expected:
```
Python 3.11.x
travelmind_agent.py
```

---

## 1 · Enable model access (console — click path)

The model must be enabled in your account **before** the agent can call it.

1. Open the **Amazon Bedrock** console.
2. Top-right region selector → **US West (Oregon) `us-west-2`**. (Must match the region you deploy to.)
3. Left nav → **Model catalog**. *(This replaced the old "Model access" page — if you still see "Model access", that works too.)*
4. Filter by provider **Anthropic** → open **Claude Sonnet 4.5**.
5. Click **Available to request** / **Enable** / **Request access**. Most Anthropic models in `us-west-2` enable in seconds; some show "In progress" briefly.

**Expected:** the model shows **Access granted** (green). If it says "Use case details required", fill the short form and resubmit.

> Quick proof it worked (CLI):
> ```bash
> aws bedrock list-foundation-models --region us-west-2 \
>   --query "modelSummaries[?contains(modelId,'claude-sonnet-4-5')].modelId" --output text
> ```
> Expected: one or more `...claude-sonnet-4-5...` ids printed.

---

## 2 · Connectivity check (CLI — ≈1 min)

```bash
aws sts get-caller-identity
```

Expected (an account + role ARN, not an error):
```json
{
  "UserId": "AROA...:session",
  "Account": "123456789012",
  "Arn": "arn:aws:sts::123456789012:assumed-role/.../your-session"
}
```

If this errors, your credentials are not set — see Failure → Fix (`credentials`).

---

## 3 · Install the starter toolkit (≈2 min)

```bash
python -m venv .venv && source .venv/bin/activate
pip install "bedrock-agentcore" "strands-agents" "bedrock-agentcore-starter-toolkit" boto3
agentcore --help
```

Expected (last command lists the verbs):
```
Usage: agentcore [OPTIONS] COMMAND [ARGS]...
Commands:
  configure   Configure an agent for deployment
  launch      Deploy the agent to AgentCore Runtime
  invoke      Invoke a deployed agent
  destroy     Remove the deployed agent and resources
  ...
```

> **The two-CLI trap.** This is the **Python** toolkit — verbs are `configure / launch / invoke`. There is also an **npm** package `@aws/agentcore` whose verbs are `create / deploy` and which needs Node 20+ and the AWS CDK. If you see `agentcore create` in a guide, that is the *other* CLI. Stay on the Python toolkit for this lab.

---

## 4 · (Optional) test the agent locally before deploying (≈2 min)

```bash
python travelmind_agent.py      # starts a local server on :8080
```

Expected: a line indicating the server is serving on port 8080 (`/invocations`, `/ping`). In a **second** terminal:

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Status of PNR JX48Q2 and my options?"}'
```

Expected: a JSON body whose `result` mentions the cancellation and rebooking options. Then `Ctrl+C` to stop the local server.

---

## 5 · Configure (`agentcore configure`)

```bash
agentcore configure -e travelmind_agent.py --disable-memory
```

You will be prompted. Typical answers:

| Prompt (wording may vary) | Answer | Why |
|---|---|---|
| Execution role | **Enter** (auto-create) | toolkit makes a role with the right permissions |
| ECR repository | **Enter** (auto-create) | only used for container deploys |
| Deployment mode | **Enter** = `direct_code_deploy` (default) | no Docker needed for Python |
| Memory (if not disabled by the flag) | `--disable-memory` already skips it | add Memory on Day 7 |
| Region | `us-west-2` | match Step 1 |

**Expected:** a config summary and a new hidden file:
```
✓ Configuration written to .bedrock_agentcore.yaml
  entrypoint: travelmind_agent.py
  region:     us-west-2
  deployment: direct_code_deploy
```

```bash
cat .bedrock_agentcore.yaml     # sanity check — entrypoint + region present
```

---

## 6 · Launch (`agentcore launch`)

```bash
agentcore launch
```

This packages your code to S3, creates the IAM execution role, and provisions the Runtime endpoint. **Takes ~2–5 minutes.**

**Expected** (the key lines — note the ARN and the log group):
```
• packaging code (direct_code_deploy) … done
• creating execution role … done
• provisioning AgentCore Runtime … done
✓ Agent deployed
  Agent ARN: arn:aws:bedrock-agentcore:us-west-2:123456789012:runtime/travelmind_agent-XXXX
  Logs:      /aws/bedrock-agentcore/runtime/travelmind_agent-XXXX
```

Copy the **Agent ARN** — you need it for the SDK in Step 9. (It is also in `.bedrock_agentcore.yaml` under `bedrock_agentcore:`.)

> For a local container run instead of cloud, use `agentcore launch -l` (needs Docker). Not required here.

---

## 7 · Verify in the console (AgentCore Runtime page — click path)

1. **Amazon Bedrock** console → region **`us-west-2`**.
2. Left nav → **AgentCore** → **Agent Runtime**.
3. Open your agent (`travelmind_agent-XXXX`).

**Expected on the page:**

| Field | Expected value |
|---|---|
| **Status** | **Ready** |
| **Agent ARN** | matches the ARN from Step 6 |
| **Endpoints** | at least one (DEFAULT) |
| **Logs / Observability** | link to the CloudWatch log group |

If **Status = Failed** → open **Logs** and read the latest stream, then see Failure → Fix.

---

## 8 · Invoke from the CLI (≈30 sec)

```bash
agentcore invoke '{"prompt": "Status of PNR JX48Q2 and my options?"}'
```

**Expected:** a JSON response whose `result` reads roughly:
```
"... AI-302 ... cancelled due to weather ... AI-318 at 18:40, or 6E-552 at 21:15 ..."
```

That is your hand-rolled-then-Strands agent answering from a managed endpoint.

---

## 9 · Invoke via the SDK (for your app)

The CLI is for you; apps call `InvokeAgentRuntime` on the `bedrock-agentcore` **data-plane** client. Replace `<AGENT_ARN>`.

```python
import boto3, json
rt = boto3.client("bedrock-agentcore", region_name="us-west-2")   # data plane
resp = rt.invoke_agent_runtime(
    agentRuntimeArn="<AGENT_ARN>",
    payload=json.dumps({"prompt": "Status of PNR JX48Q2 and my options?"}),
)
print(resp["response"].read().decode())
```

**Expected:** the same answer as Step 8, printed as JSON.
**Permission needed:** the caller must have `bedrock-agentcore:InvokeAgentRuntime`.

---

## 10 · Clean up (do this at end of lab)

Idle resources still bill — tear them down.

```bash
agentcore destroy
```

Then in the console, delete anything you created by hand:
- any **Knowledge Base** and its **OpenSearch Serverless** collection (OpenSearch bills hourly even when idle — the ~$350/mo floor / the "$11 lesson")
- the auto-created **ECR repo** / **S3** package if you will not redeploy

**Expected:** `agentcore destroy` reports the Runtime, role, and package removed.

---

## Failure → Fix

| Symptom | Likely cause | Fix |
|---|---|---|
| `ValidationException: ... not supported for on-demand throughput` | Bare model id | Use the **`us.`** inference-profile id (already set in the file) |
| `AccessDeniedException` calling the model | Model access not enabled, or the execution role lacks `bedrock:InvokeModel` | Enable in **Model catalog** (Step 1); ensure the role can invoke the model / profile |
| `ThrottlingException` / quota is 0 | New account has 0 applied quota | Request a quota increase or open a support case; or wait |
| `agentcore: command not found` | Toolkit not installed, or wrong venv | `source .venv/bin/activate` then `pip install bedrock-agentcore-starter-toolkit` |
| `agentcore create` "unknown command" | You're on the **npm** `@aws/agentcore` CLI | Use the **Python** toolkit verbs: `configure` / `launch` / `invoke` |
| `configure`: entrypoint file not found | Wrong directory / path | `cd` to the folder with `travelmind_agent.py`; pass `-e travelmind_agent.py` |
| `launch`: AccessDenied creating role / ECR / S3 | Your identity lacks deploy permissions | Use the provided admin role for the session |
| `launch`: Docker / build error | Expecting local Docker | Default is `direct_code_deploy` (no Docker). For a container, CodeBuild handles it; or `agentcore launch -l` for local |
| Status **Ready** but invoke returns empty / error | Entrypoint returns a non-JSON value | Return a **dict**, e.g. `return {"result": str(result)}` |
| Invoke **times out** on long runs | No streaming on a long agent run | Stream the response, or shorten the run |
| `Unable to locate credentials` / token expired | AWS creds not set / session expired | Re-auth (`aws configure` / refresh SSO / refresh bearer token), re-run Step 2 |
| Model "not found" in region | Region mismatch | Use **`us-west-2`** everywhere (toolkit default) |
| Guardrail blocks a valid query (e.g. the word "token") | Untested guardrail filter | Test the guardrail against your real domain terms; adjust the filter |

---

## Appendix — the deployed file

`travelmind_agent.py` (written by the notebook). The **three additions** that make a Strands agent deployable are marked `+++`.

```python
from bedrock_agentcore import BedrockAgentCoreApp          # +++ AgentCore wrapper
from strands import Agent, tool
from strands.models import BedrockModel

MODEL = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"     # us. inference profile

@tool
def lookup_booking(pnr: str) -> dict:
    """Look up a booking by its PNR code."""
    return {"pnr": pnr, "status": "CANCELLED", "flight": "AI-302", "date": "2026-06-12"}

# ... get_disruption_reason, get_rebooking_options ...

model = BedrockModel(model_id=MODEL, region_name="us-west-2")
agent = Agent(model=model, tools=[lookup_booking, get_disruption_reason, get_rebooking_options],
              system_prompt="You are TravelMind, a booking-exception assistant. Never invent a PNR.")

app = BedrockAgentCoreApp()                                # +++ create the app

@app.entrypoint                                            # +++ mark the entrypoint
def invoke(payload):
    result = agent(payload.get("prompt", ""))
    return {"result": str(result)}

if __name__ == "__main__":
    app.run()                                              # +++ serve on :8080  (/invocations, /ping)
```

**One-screen command recap**
```bash
# 1 enable model access in the console (Model catalog → Claude Sonnet 4.5)
pip install bedrock-agentcore strands-agents bedrock-agentcore-starter-toolkit boto3
agentcore configure -e travelmind_agent.py --disable-memory
agentcore launch                                  # note the Agent ARN
agentcore invoke '{"prompt": "Status of PNR JX48Q2 and my options?"}'
agentcore destroy                                 # at end of lab
```
