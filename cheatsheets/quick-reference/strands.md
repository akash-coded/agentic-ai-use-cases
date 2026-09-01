# Strands Agents — Cheat Sheet

AWS's open-source agent SDK. Model-driven: you describe tools, the model decides when to use them.

```bash
pip install strands-agents strands-agents-tools
```

---

## Minimum agent

```python
from strands import Agent

agent = Agent()                       # sensible Bedrock default
print(agent("Explain reciprocal rank fusion in two sentences."))
```

That is the whole loop — the thing you wrote by hand in
[Module 05](../../modules/05-agent-loop-no-framework-to-strands/).

## Tools

```python
from strands import Agent, tool

@tool
def get_booking(booking_ref: str) -> dict:
    """Retrieve a single booking by reference: passenger, itinerary, fare class, status.

    Use this when you need facts about a specific booking.
    Does NOT contain refund eligibility — use get_fare_rules for that.

    Args:
        booking_ref: Six-character booking reference, e.g. XY7Q2M
    """
    return lookup(booking_ref)

agent = Agent(tools=[get_booking])
```

**The docstring is the model-facing description and the type hints become the schema.** Write the docstring
for the model, not for your teammates — say what the tool is *not* for and which tool to use instead. See
[Tool Surface Audit](../frameworks/tool-surface-audit.md).

Pre-built tools:

```python
from strands_tools import calculator, python_repl, file_write, memory
agent = Agent(tools=[calculator, memory])
```

## Choosing the model

```python
from strands.models import BedrockModel

model = BedrockModel(
    model_id="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    temperature=0.2,
    region_name="us-east-1",
)
agent = Agent(model=model, tools=[get_booking])
```

The `us.` prefix rule from [Bedrock](bedrock-converse.md#model-ids-and-inference-profiles) still applies —
Strands does not hide Bedrock from you.

## Inspecting the run

```python
result = agent("Is XY7Q2M refundable?")
print(result.message)          # the answer
print(result.metrics)          # tokens, latency, cycles
```

`result.metrics` is where your [token tax](../frameworks/token-tax-ledger.md) and
[three clocks](../frameworks/three-clocks.md) numbers come from. Read it before optimising anything.

## MCP — tools from an external server

```python
from mcp import stdio_client, StdioServerParameters
from strands.tools.mcp import MCPClient

mcp = MCPClient(lambda: stdio_client(
    StdioServerParameters(command="python", args=["unit_server.py"])))

with mcp:
    agent = Agent(tools=mcp.list_tools_sync())
    print(agent("Convert 180 minutes to hours."))
```

An MCP server is a dependency with its own latency and failure modes. Wrap calls with timeouts; do not
trust it implicitly.

## Multi-agent

**Agents as tools — delegation.**

```python
analyst = Agent(name="analyst", tools=[calculator], system_prompt="You analyse fare data.")

@tool
def consult_analyst(question: str) -> str:
    """Ask the fare analyst a quantitative question about fare rules."""
    return str(analyst(question))

lead = Agent(tools=[consult_analyst, get_booking])
```

**Graph — you know the control flow.**

```python
from strands.multiagent import GraphBuilder

b = GraphBuilder()
b.add_node(triage,  "triage")
b.add_node(refund,  "refund")
b.add_node(rebook,  "rebook")
b.add_edge("triage", "refund")
b.add_edge("triage", "rebook")
b.set_entry_point("triage")
graph = b.build()
result = graph("Flight cancelled, what are my options?")
```

**Swarm — you do not.**

```python
from strands.multiagent import Swarm
swarm = Swarm([researcher, critic, writer])
result = swarm("Draft the disruption policy summary.")
```

> ⚠️ A swarm without a termination condition does not terminate. Set an explicit bound and a budget
> ceiling. See [Handoff Multiplier](../frameworks/handoff-multiplier.md) for what each shape costs.

## Choosing a shape

| Situation | Use |
| --- | --- |
| One skill, one context | Single agent |
| Known sub-tasks, clean interfaces | Agents as tools (delegation) |
| Control flow known in advance | Graph |
| Open-ended exploration | Swarm — **with a stop rule** |
| Quality matters more than latency | Critique loop, capped at 1 round |

## Common mistakes

| Symptom | Cause |
| --- | --- |
| Model picks the wrong tool | Docstring written for humans; no boundary stated |
| Loop never ends | No iteration cap; tool never satisfies the request |
| Costs multiplied unexpectedly | Handoffs re-send context — measure H× |
| Works locally, fails deployed | Region or inference-profile mismatch |
| Empty tool result treated as "nothing applies" | Return an explicit status, not `[]` |

## Learn it properly

[Module 05](../../modules/05-agent-loop-no-framework-to-strands/) (loop by hand first) ·
[Module 06](../../modules/06-strands-foundations/) (tools, memory, MCP) ·
[Module 07](../../modules/07-strands-multi-agent-patterns/) (topologies) ·
[docs](https://strandsagents.com/)
