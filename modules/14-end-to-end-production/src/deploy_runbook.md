# Deploy Runbook: TravelMind to AgentCore Runtime

Take the working local agent to a managed endpoint others can call. Every step,
console and CLI. Pair this with `deploy_e2e.ipynb`, which runs the local parts
for real and lays out the cloud parts the same way.

The agent: `travelmind_agent.py`. The wrap: `travelmind_runtime.py`. Anchor PNR
`JX48Q2`, model `us.anthropic.claude-haiku-4-5-20251001-v1:0`, region `us-east-1`.

---

## 0. One-time setup

Pick your environment. Both need AWS credentials with Bedrock access.

**VS Code (local), 3 steps**
```bash
python -m venv .venv && source .venv/bin/activate     # 1. activate venv
aws configure                                         # 2. set creds + region us-east-1
pip install -r requirements.txt                       # 3. install deps
```

**Google Colab, 3 steps**
```python
!pip install -q strands-agents bedrock-agentcore boto3   # 1. install deps
import os                                                  # 2. creds via env / Colab secrets
os.environ["AWS_ACCESS_KEY_ID"] = "..."                    #    (use Colab "Secrets" in real use)
os.environ["AWS_SECRET_ACCESS_KEY"] = "..."
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"             # 3. region
```

### Know which CLI you have

Two different tools answer to `agentcore`. This is the most common reason a
command "is not found." We use the first one.

| | Starter toolkit (use this) | @aws CLI |
|---|---|---|
| Install | `pip install bedrock-agentcore-starter-toolkit` | `npm i -g @aws/agentcore` |
| Commands | `agentcore configure / launch / invoke` | `agentcore create / deploy` |
| Needs | Python only | Node 20 + CDK |

If `agentcore launch` is missing but `agentcore deploy` exists, you are on the
other CLI. Check the package, not your syntax.

---

## 1. Confirm the local agent works

You wrote this on your build days. Confirm it before wrapping anything.
```bash
python -c "from travelmind_agent import get_agent; print(get_agent()('Status of PNR JX48Q2?'))"
```
Expected: a sentence saying JX48Q2 is cancelled due to weather, with options.
No creds yet? Run the offline check instead: `python travelmind_agent.py`.

---

## 2. Wrap it: `travelmind_runtime.py`

Already in the kit. Three things make it deployable:

| Piece | Why |
|---|---|
| `app = BedrockAgentCoreApp()` | the runtime application object |
| `@app.entrypoint def invoke(payload)` | the function Runtime calls per request; reads `payload["prompt"]` |
| `app.run()` | serves `POST /invocations` and `GET /ping` on port 8080 |

Your agent logic is untouched. The wrap adds a request and response contract:
callers send `{"prompt": "..."}` and get a string back.

---

## 3. Run and test the contract locally

```bash
python travelmind_runtime.py                # serves on http://0.0.0.0:8080
```
From a second terminal:
```bash
curl localhost:8080/ping
# {"status": "healthy"}

curl -X POST localhost:8080/invocations \
     -H 'Content-Type: application/json' \
     -d '{"prompt":"Status of PNR JX48Q2?"}'
# "PNR JX48Q2 is cancelled due to weather..."
```
No terminal or no creds? Test the entrypoint in-process instead:
```python
from travelmind_runtime import invoke
print(invoke({"prompt": "Status of PNR JX48Q2?"}))
```
Gate: if it fails here, it fails in the cloud too. Never deploy a red contract.

---

## 4. Containerize

The `Dockerfile` is in the kit. The two lines that matter for the runtime:
```dockerfile
EXPOSE 8080
CMD ["python", "travelmind_runtime.py"]
```
The container must listen on 8080. The starter toolkit can build this for you in
the next step; you do not have to run `docker build` by hand.

---

## 5. `agentcore configure`

```bash
agentcore configure --entrypoint travelmind_runtime.py
```
What it creates:

| Output | What it is |
|---|---|
| `.bedrock_agentcore.yaml` | records entrypoint, region, packaging so launch is repeatable |
| execution role | the identity the running agent uses to call Bedrock and write logs (pass `--role` to use your own) |
| ECR target | the private registry the image is pushed to on launch |

The execution role is where the 403 in step 7 lives if it is too narrow. See
`iam_invoke_policy.json` for the policy that clears it.

---

## 6. `agentcore launch`

```bash
agentcore launch
```
What happens, in order: build the image, push to ECR, provision the managed
runtime (network interfaces, scaling, health checks), return a runtime ARN.

This takes about 5 to 10 minutes. It is one-time provisioning, not per-call
latency. You get back an `agentRuntimeArn` you invoke next.

---

## 7. `agentcore invoke`

```bash
agentcore invoke '{"prompt":"My flight on JX48Q2 was cancelled. Options?"}'
# "JX48Q2 is cancelled (weather). Two options: AI-318 at 18:40, 6E-552 at 21:15..."
```
The same agent now answers from AWS, isolated and scalable.

---

## The wall: the two errors almost everyone hits

| Code | Symptom | Cause | Fix |
|---|---|---|---|
| 404 | model ARN not found | model id missing the `us.` inference-profile prefix | use `us.anthropic.claude-haiku-4-5-20251001-v1:0` |
| 403 | access denied on invoke | execution role cannot invoke that model | attach `iam_invoke_policy.json` (replace `ACCOUNT_ID`) |

The 404 is config: on-demand Claude models must be called through a cross-region
inference profile. The 403 is permissions: the role needs `bedrock:InvokeModel`
on the inference-profile ARN AND on the three regional foundation-model ARNs the
profile fronts (us-east-1, us-east-2, us-west-2). Fix the 404 first, then the
403; doing it in the other order hides the second error.

---

## What changes in production

| In the demo | In production |
|---|---|
| `aws configure` keys | the execution role, no long-lived keys in code or image |
| hardcoded region | injected via environment / config |
| broad-ish role | least privilege: invoke only the models you use, write only your log group |
| no retries | adaptive retries + a request timeout; throttles are normal at scale |
| logs only | observability on at deploy (CloudWatch GenAI spans); you cannot debug what you did not capture |

---

## Cleanup

When you are done with the workshop runtime, remove it so it stops costing:
```bash
agentcore destroy        # tears down the runtime this config created
```
Also delete the ECR image and the log group if you will not reuse them.
