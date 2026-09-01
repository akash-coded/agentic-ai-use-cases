# How to · Deploy any agent to AgentCore

**Time:** 60–90 minutes first time. **You need:** a working agent and AWS access.

AgentCore Runtime does not care which framework built your agent. This is the path that works for Strands,
LangGraph, or no framework at all.

---

## 1. Separate the agent from the transport

The most common deployment problem is logic tangled with the notebook. Split first:

```
app/
├── agent.py       # your agent — no AWS runtime imports
└── main.py        # the entrypoint — thin
```

`agent.py` should run unchanged in a notebook, a test, and the runtime. If it imports the runtime, you
cannot test it without deploying it.

## 2. Write a thin entrypoint

```python
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from agent import build_agent

app = BedrockAgentCoreApp()
agent = build_agent()

@app.entrypoint
def handler(payload):
    result = agent(payload.get("prompt", ""))
    return {
        "answer":   str(result.message),
        "model":    result.metrics.model_id,   # log which model answered
        "trace_id": payload.get("trace_id"),
    }

if __name__ == "__main__":
    app.run()
```

**Return the answering model.** One field, and it is the only thing that makes silent failover detectable
later. See [Silent Degradation Watchlist](../../frameworks/silent-degradation-watchlist.md).

## 3. Pin your dependencies

```
# requirements.txt — pin, do not float
strands-agents==<version>
bedrock-agentcore==<version>
boto3>=1.35.0
```

A floating dependency means the deployed agent differs from the tested one.

## 4. Decide retention before you deploy

Memory is a **cost decision** made at design time:

| Scope | Keep | TTL |
| --- | --- | --- |
| Session | Current interaction turns | Session end |
| Long-term | Summaries, outcomes | Set one — 30 days is a common default |
| Never | Raw PII, payment details | — |

Deploying without a TTL is [cost cliff 8](../../frameworks/cost-cliff-map.md): storage grows forever and
nobody notices until billing.

## 5. Scope identity per tool

```
❌  one role: {"Action": ["dynamodb:*", "s3:*", "lambda:InvokeFunction"]}

✅  get_booking    → dynamodb:GetItem on table/Bookings
    search_policy  → bedrock:Retrieve on knowledge-base/KB123
    draft_response → no AWS permissions at all
```

See [IAM for agents](../../quick-reference/iam-for-agents.md).

## 6. Deploy

Follow the walkthrough matching your framework — the runtime is the same in all three:

| Framework | Walkthrough |
| --- | --- |
| Strands | [`AgentCore_01_Strands_Minimum_Deploy.ipynb`](../../../modules/11-bedrock-agentcore/walkthroughs/AgentCore_01_Strands_Minimum_Deploy.ipynb) |
| No framework | [`AgentCore_02_NoFramework_Minimum_Deploy.ipynb`](../../../modules/11-bedrock-agentcore/walkthroughs/AgentCore_02_NoFramework_Minimum_Deploy.ipynb) |
| LangGraph | [`AgentCore_03_LangGraph_Minimum_Deploy.ipynb`](../../../modules/11-bedrock-agentcore/walkthroughs/AgentCore_03_LangGraph_Minimum_Deploy.ipynb) |

For a CDK-managed project, [`MyFirstRuntimeAgent`](../../../modules/11-bedrock-agentcore/src/MyFirstRuntimeAgent/)
is a complete working example.

## 7. Verify before you celebrate

- [ ] Invoke returns an answer **and** a trace id
- [ ] `model` field shows the model you expected
- [ ] A deliberately bad input produces abstention, not invention
- [ ] A tool failure produces an honest response
- [ ] Logs appear in CloudWatch and you can find one run by its trace id

## 8. Write down the teardown

Runtimes, gateways and memory stores bill for **existing**:

```
□ delete runtime   □ delete gateway   □ delete memory store
□ cdk destroy      □ delete log groups
```

Put it in the repo, not in your head.

## Common failures

| Symptom | Cause |
| --- | --- |
| Deploy succeeds, invoke fails | Runtime role missing a downstream permission |
| Works locally, not deployed | Region or inference-profile mismatch |
| Cannot debug a production run | No trace id returned to the caller |
| Bill climbing with no traffic | No memory TTL, or infrastructure left up |

**Related:** [AgentCore cheat sheet](../../quick-reference/agentcore.md) ·
[Module 11](../../../modules/11-bedrock-agentcore/) ·
[Module 11 LLD](../../../docs/architecture/lld/11-bedrock-agentcore.md)
