# Give the agent a job

You are prototyping a desk-side assistant for your team. Before it can do anything clever, it needs two things: a clear role, and the sense to reach for a tool when it does not actually know something. That is what you will shape here.

Work at whatever level fits you. Everyone should clear Level 1; go as far past it as you like.

## Spin up (30 seconds)

Run once, in Colab or locally. Stay on Haiku 4.5 while experimenting - it is fast and cheap.

```bash
pip install -q strands-agents strands-agents-tools
```

- Colab: open the Secrets panel (key icon, left sidebar) and add `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.
- Local: run `aws configure` once, or export the `AWS_` variables in your shell.
- Region: set it to wherever you enabled Bedrock model access (for example `us-west-2`).

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
print("ready:", MODEL.get_config()["model_id"])
```

If something complains:

| Message | Fix |
|---|---|
| on-demand throughput isn't supported | keep the `us.` prefix on the model id |
| throttling / too many requests | you are fine - the retries handle it, wait a few seconds |
| could not load credentials | recheck the region and keys above |

## Level 1 - give it a role

Create one agent with a personality and a job, then talk to it.

```python
buddy = Agent(model=MODEL, system_prompt="...you decide the role...", callback_handler=None)
print(say(buddy("...your question...")))
```

- Pick a role you would actually use: a concise travel concierge, a patient Python tutor, a blunt code reviewer. Your call.
- Ask it three things. Then change one line, the system prompt, and ask the same three things again.

You are done when: you can show two clearly different "personalities" answering the same question, changed only by the system prompt.

## Level 2 - stop it from guessing

Your agent will happily invent things it cannot know: today's date, a live price, an order status. Give it one tool so it looks things up instead.

```python
@tool
def order_status(order_id: str) -> str:
    """Look up the delivery status of an order.

    Args:
        order_id: the order number, e.g. "1042"
    """
    # return something, real or faked - the wiring is the point
    ...

agent = Agent(model=MODEL, tools=[order_status], callback_handler=None)
print(say(agent("Where is order 1042?")))
```

- The docstring is not decoration. The model reads it to decide when to call the tool. Write it like an instruction.

You are done when: the agent answers an order question by calling your tool, not by guessing.

## Level 3 - push it

Pick any one:

- Inspect the work. Print `result.metrics.get_summary()` and find total cycles and total tokens.
- Turn the dial. Build the agent with `temperature=0`, ask a creative question twice; rebuild with `temperature=0.9`, ask twice. Compare.
- Add a second tool and ask a two-part question. Check `agent.tool_names`, then look in the metrics summary to see which tools fired.

You are done when: you can explain in one sentence each what temperature changed, and how the agent decided which tool to use.

## Notice this

- The system prompt is the steering wheel. Small wording changes move behavior a lot.
- You never wrote routing logic. The model decides when a tool is relevant, from its name and docstring.
- Tokens and cycles are your cost and behavior signals. Watch them early.

## Poke at it

Ask the agent something your tool does not cover. Does it still try the tool? Why might it, and how would you stop it?
