# Post-Session Task - Convert UC-A1 to Strands, then deploy on AgentCore

**Goal.** Take your hand-rolled TravelMind UC-A1 agent, rebuild it in **Strands**, wrap it with **`BedrockAgentCoreApp`**, and deploy it to a live **AgentCore Runtime** endpoint using your admin AWS access. Then answer the reflection checklist.

**Why this one.** The hand-rolled loop taught you the mechanics. This task proves the next two moves: a framework removes the loop boilerplate (and a whole class of bugs), and a runtime turns "runs on my laptop" into "runs as a managed endpoint." That is the actual path an agent takes to production.

**Time:** ~90 minutes. Do the deploy in **one sitting** - your admin access is time-boxed, and idle resources bill.

**You already have:** the hand-rolled version (Demo 1 / the lab), the Strands version (Demo 2), the AgentCore wrapper (Demo 3), and the **Live-AWS Runbook** for the click-by-click deploy + failure -> fix table. Use them as reference, not copy-paste - the point is to rebuild it yourself.

---

## Part 1 - Convert to Strands (~30 min)

Start from your hand-rolled loop. Replace, do not add:

| Hand-rolled (delete it) | Strands (replaces it) |
|---|---|
| `tool_config` written by hand | a `@tool`-decorated function per tool (docstring = description, type hints = schema) |
| the `while stopReason == "tool_use"` loop | `Agent(model=..., tools=[...], system_prompt=...)` - it runs the loop |
| `messages.append(...)` for the assistant turn and the `toolResult` | gone - Strands manages the message thread |
| the `toolUseId` matching | gone - Strands manages ids |
| the `max_steps` guard | built in (you can still configure it) |

Keep the **same three tools, same mock data, same system prompt**. Skeleton:

```python
from strands import Agent, tool
from strands.models import BedrockModel

MODEL = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"   # us. inference profile you have enabled

@tool
def lookup_booking(pnr: str) -> dict:
    """Look up a booking by its PNR code."""
    return {"pnr": pnr, "status": "CANCELLED", "flight": "AI-302", "date": "2026-06-12"}
# ... get_disruption_reason, get_rebooking_options ...

agent = Agent(model=BedrockModel(model_id=MODEL, region_name="us-west-2"),
              tools=[lookup_booking, get_disruption_reason, get_rebooking_options],
              system_prompt="You are TravelMind, a booking-exception assistant. Never invent a PNR.")

print(agent("My flight on JX48Q2 was disrupted - what happened and what are my options?"))
```

**Done when:** it answers the UC-A1 prompt locally and calls the tools (you can see it reason through the disruption).

---

## Part 2 - Wrap for AgentCore (~10 min)

Three additions turn the agent into a hosted service. Add them to a file `travelmind_agent.py`:

```python
from bedrock_agentcore import BedrockAgentCoreApp     # +++

app = BedrockAgentCoreApp()                           # +++

@app.entrypoint                                       # +++
def invoke(payload):
    return {"result": str(agent(payload.get("prompt", "")))}

if __name__ == "__main__":
    app.run()                                         # +++ serves :8080 (/invocations, /ping)
```

**Test locally before deploying** (terminal, not a cell - `app.run()` blocks):

```
python travelmind_agent.py
# in a second terminal:
curl -X POST http://localhost:8080/invocations -H "Content-Type: application/json" -d '{"prompt": "Status of PNR JX48Q2 and my options?"}'
```

**Done when:** the curl returns JSON whose `result` describes the cancellation and rebooking options.

---

## Part 3 - Deploy to Runtime (~25 min)

Full click-by-click + expected output + failure -> fix is in the **Runbook**. Short version:

```
agentcore configure -e travelmind_agent.py --disable-memory
agentcore launch                 # provisions the Runtime; copy the Agent ARN it prints
agentcore invoke '{"prompt": "Status of PNR JX48Q2 and my options?"}'
```

Then verify in the console: **Bedrock -> AgentCore -> Agent Runtime** shows **Status: Ready** and your ARN.

**Stretch (do this for the reflection):** make one run long enough to risk a timeout (ask for a long, detailed itinerary), then **enable streaming** and compare. Note what changes.

**Done when:** `agentcore invoke` returns the UC-A1 answer from the cloud endpoint.

---

## Part 4 - Reflection checklist

Answer in a few sentences each. Evidence beats yes/no.

1. **Did the loop bug disappear?** You no longer write the append step, the `toolUseId` match, or the guard. Which of your hand-rolled bugs are now **structurally impossible**, and which can **still** happen? (Hint: the message-order and id bugs are gone; tool-schema, model-access, and prompt bugs are not.)
2. **Did streaming fix the timeout?** Describe the timeout you saw (or would hit on a long run) and whether streaming resolved it. Be precise: streaming fixes client/idle timeouts on long *generations* - it does **not** fix a genuinely stuck tool or an under-provisioned runtime.
3. **Line count:** hand-rolled vs Strands. What did you delete, and what did you give up? (Control and visibility into every turn, in exchange for brevity.)
4. **Inference profile / model access:** did the `us.` prefix or the region bite you during deploy? Where?
5. **The two-CLI trap:** which `agentcore` CLI did you use, and how did you know it was the right one?
6. **What did `agentcore launch` actually create** in your account? Check the console - name the execution role, the code package, and the endpoint.
7. **Cost:** now that the loop is hosted, what multiplies your token spend? (The agent loop is several model calls per request; retrieval would double the path.)
8. **What is still NOT production-ready** about this deployment? (No Memory / Gateway / Identity / Observability yet - that is Day 7; the tools return mock data; the endpoint's only guard is IAM.)

---

## Submit

Share with your TA: (1) the **Agent ARN**, (2) your **`travelmind_agent.py`**, (3) the **`agentcore invoke` output**, (4) your **reflection answers**.

## Clean up (mandatory)

```
agentcore destroy
```

Also delete any Knowledge Base / OpenSearch collection you created - OpenSearch Serverless bills hourly even when idle. Leaving resources up overnight is the single most common surprise on the bill.

---

### Guardrails

- Stay on the **Python** starter toolkit (`configure` / `launch` / `invoke`), not the npm `@aws/agentcore` (`create` / `deploy`).
- Use **`us-west-2`** everywhere - it must match where you enabled model access.
- Your admin access is **time-boxed**: deploy, verify, reflect, and tear down in one sitting.
