# The toolsmith

A single tool is a gadget. A few well-described tools plus a clear role is an assistant that does real work and hands back clean, usable results. Build one.

The running example is a lightweight trip assistant. Swap in your own domain if you prefer - support, research, internal ops. The mechanics are identical.

## Spin up

Same starter as before. Stay on Haiku 4.5 while you build.

```python
import os
os.environ["AWS_DEFAULT_REGION"] = "us-west-2"   # your enabled-model region

from strands import Agent, tool
from strands.models import BedrockModel
from botocore.config import Config

def get_model(model_id="us.anthropic.claude-haiku-4-5-20251001-v1:0",
              temperature=0.3, max_tokens=2048):
    return BedrockModel(model_id=model_id, temperature=temperature, max_tokens=max_tokens,
        boto_client_config=Config(read_timeout=900, connect_timeout=900,
                                  retries={"max_attempts": 4, "mode": "adaptive"}))

def say(result):
    return "".join(b.get("text", "") for b in result.message["content"]).strip()

MODEL = get_model()
```

Stuck on AWS: it is almost always the `us.` model-id prefix, the region, or your credentials. Check those three first.

## Level 1 - a small toolkit that routes

Give one agent two or three related tools, then ask a question that needs more than one of them.

```python
@tool
def weather(city: str) -> str:
    """Current weather for a city."""
    ...

@tool
def seat_price(route: str) -> str:
    """Approximate economy seat price for a route like 'BLR-DEL'."""
    ...

assistant = Agent(model=MODEL, tools=[weather, seat_price], callback_handler=None)
print(say(assistant("What's the weather in Delhi, and roughly what's a BLR-DEL seat?")))
```

- Faked data is fine. Each tool: one job, a clear docstring, typed inputs.

You are done when: a single question triggers more than one tool and the agent stitches the results into one answer.

## Level 2 - hand back data, not prose

You want to drop the result into an app, not read a paragraph. Make the agent fill a typed shape.

```python
from pydantic import BaseModel, Field

class TripPlan(BaseModel):
    destination: str = Field(description="city")
    items: list[str] = Field(description="3-5 things to pack")
    est_cost: float = Field(description="rough total in your currency")

planner = Agent(model=MODEL, callback_handler=None)
plan = planner.structured_output(TripPlan, "Plan a 2-day trip to Delhi in July.")

print(plan.destination, plan.est_cost)   # a real string and a real number
print(plan.items)                         # a real Python list
```

You are done when: you get back a real object with the right types (a list is a list, a number is a number), not text you have to parse.

## Level 3 - push it

Pick one:

- Memory in a chat. Keep talking to the same agent: tell it a preference, then ask a follow-up that depends on it.
- State the model never sees. Give a tool an itinerary it edits through `tool_context` (`tool_context.agent.state.get(...)` / `.set(...)`), then ask "what's on my list?".
- Model trade-off. Run a genuinely hard reasoning question on Haiku, then on Sonnet with `get_model(model_id="us.anthropic.claude-sonnet-4-20250514-v1:0")`. Compare answer quality and tokens.

You are done when: your assistant remembers something across turns, or you can state the Haiku-versus-Sonnet trade-off from your own run.

## Notice this

- Tool descriptions are the routing logic. Vague descriptions cause skipped or doubled calls.
- Structured output is how an agent becomes a building block that other code can use.
- Memory has layers: the running chat, hidden state, and later, sessions that survive a restart.

## Poke at it

Write two tools that could both plausibly answer the same question. Which one does the agent pick, and how does editing the descriptions change that?
