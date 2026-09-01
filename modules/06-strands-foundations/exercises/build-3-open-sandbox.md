# Open sandbox

A loose space to build something that makes you grin and quietly teaches you the craft underneath. Take it as far as you like - five minutes or twenty-five.

## Spin up

```python
import os
os.environ["AWS_DEFAULT_REGION"] = "us-west-2"   # your enabled-model region

from strands import Agent, tool
from strands.models import BedrockModel
from botocore.config import Config

def get_model(model_id="us.anthropic.claude-haiku-4-5-20251001-v1:0",
              temperature=0.5, max_tokens=2048):
    return BedrockModel(model_id=model_id, temperature=temperature, max_tokens=max_tokens,
        boto_client_config=Config(read_timeout=900, connect_timeout=900,
                                  retries={"max_attempts": 4, "mode": "adaptive"}))

def say(result):
    return "".join(b.get("text", "") for b in result.message["content"]).strip()

MODEL = get_model()
```

If AWS argues: check the `us.` prefix, the region, then your credentials.

## Start here - a character with a gadget

Make an agent with a strong personality and give it one playful tool.

Seed ideas (pick one or invent your own):

- a dramatic dungeon master with `roll_dice(sides)`
- a deadpan assistant with `mood_emoji(text)` that tags its replies
- a tiny shopkeeper with `price_of(item)`

```python
import random

@tool
def roll_dice(sides: int) -> int:
    """Roll a die with the given number of sides."""
    return random.randint(1, sides)

dm = Agent(model=MODEL, system_prompt="You are a dramatic dungeon master.",
           tools=[roll_dice], callback_handler=None)
print(say(dm("I attack the goblin. Roll for me.")))
```

You are done when: the character answers in voice and actually uses the tool when it should.

## Go further - make the tool matter

- Force the answer to depend on the tool's output - the reply must reflect the dice roll, the price, the mood tag.
- Add a second tool. Then try to make the agent misbehave by calling the wrong tool, and fix the docstrings until it behaves.

You are done when: you have changed a tool's description and watched the agent's choice change.

## Push it - failure and teamwork

Pick one:

- A tool that can fail. Make a lookup return "not found" for unknown input, ask about something unknown, and watch the agent recover. Even a raised error is handled - Strands hands the model an error result instead of crashing.
- Two agents, one job. Wrap one agent as a tool that another agent calls - an expert the host consults. The host passes a question string and gets the expert's answer back.

```python
@tool
def lore_expert(question: str) -> str:
    """Answer questions about the game world."""
    expert = Agent(model=MODEL, system_prompt="You are a keeper of world lore.",
                   callback_handler=None)
    return say(expert(question))

host = Agent(model=MODEL, tools=[lore_expert], callback_handler=None)
print(say(host("Who rules the northern keep?")))
```

You are done when: a tool failure is handled gracefully, or two agents collaborate on one answer.

## Notice this

- Persona plus tool design is most of the craft. The model is the easy part.
- Agents do not crash on a tool error. They receive the error and can react to it.
- Wrapping an agent as a tool is the simplest way to make agents work together.

## Poke at it

What is the smallest change that makes your agent reliably do the right thing - better wording, a sharper tool description, or a better return value?
