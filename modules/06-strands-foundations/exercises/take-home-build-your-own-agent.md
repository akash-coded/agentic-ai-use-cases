# Take-home project: build your own agent

Build an agent for a task from your own world. The project comes in four parts that get progressively more hands-on. Each part stands on its own: you can do Part A with no code at all, and go as far as your time and comfort allow. There is no single right answer here. The interesting choices are yours to make.

Pick your domain now. A few that work well:

- support-ticket triage
- travel replanning when a flight gets cancelled
- a research-and-summarize helper
- an internal FAQ answerer
- meeting notes turned into action items

Use your own if you have one. Keep the same domain across all four parts so each builds on the last.

---

## Setup that will not fight you

You only need this once. It is the same starter from class.

```bash
pip install -q strands-agents strands-agents-tools
```

Credentials and region:

- Colab: open the Secrets panel (key icon) and add `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`. Add `AWS_SESSION_TOKEN` too only if you use temporary keys.
- Local: run `aws configure` once, or export the `AWS_` variables in your shell.
- Region: set it to wherever you enabled Bedrock model access.

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

If you hit a wall:

| Message | Fix |
|---|---|
| on-demand throughput isn't supported | keep the `us.` prefix on the model id |
| throttling / too many requests | expected under load - the retries handle it, wait a few seconds |
| could not load credentials | recheck region and keys above |

Stay on Haiku 4.5 throughout. It is fast and cheap, which is exactly what you want while iterating.

---

## Part A - think it through (no code)

Write a short design note. Markdown or paper is fine. Answer these:

- The one job. One sentence: "This agent _____ for _____."
- Tools. List 3 to 5 tools it would need. For each, give a name, what it does, and its inputs and output. Just describe them.
- Memory. What must it remember within a single conversation? Anything across sessions?
- Failure. Three ways it could go wrong, and what you would want to happen in each.
- Done. What does a good answer look like, and how would you know it worked?

You are done when: someone else could read your note and understand what you are about to build, and why.

This part is worth taking seriously. The clarity you create here is what makes the code parts easy.

---

## Part B - basic build (hands-on)

Bring the agent to life at a basic level.

- A system prompt that captures the role from Part A.
- One or two of your tools. Faked data is completely fine.
- Ask it a realistic question from your domain that needs a tool.

```python
@tool
def my_tool(arg: str) -> str:
    """One clear sentence on what this does and when to use it."""
    ...

agent = Agent(model=MODEL, system_prompt="...", tools=[my_tool], callback_handler=None)

result = agent("...a real question from your domain...")
print(say(result))
print(result.metrics.get_summary())   # what did it actually do?
```

You are done when: it answers using at least one tool, and the metrics show the tool was called.

---

## Part C - full build (hands-on)

Make it genuinely useful and hard to break.

- Add the rest of your tools. Aim for 2 to 4 in total.
- For at least one kind of question, return a typed result with Pydantic.
- Add memory: either follow-up questions in one chat, or `agent.state` for something that persists during the session, read and written from a tool through `tool_context`.
- Make one tool defensive: on bad input, return a clear message telling the model what to do, instead of failing silently.

Typed output, for reference:

```python
from pydantic import BaseModel, Field

class Result(BaseModel):
    summary: str = Field(description="one-line summary")
    actions: list[str] = Field(description="concrete next steps")

# agent.structured_output(Result, "...your prompt...")
```

A defensive tool, for reference:

```python
@tool
def fetch(record_id: str) -> str:
    """Fetch a record by id."""
    known = {"r1": "..."}
    if record_id not in known:
        return f"ERROR: no record '{record_id}'. Known ids: {list(known)}. Ask the user to confirm."
    return known[record_id]
```

You are done when: it handles a multi-part request, returns typed data at least once, remembers something within the chat, and a bad input produces a helpful message rather than a crash.

Poke at it: try to break it. Feed it nonsense, ask for something out of scope. Tighten your prompts and tool descriptions until it behaves.

---

## Part D - make it a team (with agents)

Split the work across more than one agent. Choose the shape that fits your task:

- Orchestrator plus specialists - the simplest. Wrap one or two specialist agents as tools and let a coordinator route to them.
- A graph - a fixed pipeline. For example: classify, then handle, then summarize, with a conditional edge that branches on the classification.
- A swarm - only if your flow is genuinely exploratory and you cannot predict the order of work.

Whichever you choose, add one guardrail and one safety net:

- A cap: `set_max_node_executions(n)` on a graph, or `max_handoffs` and `node_timeout` on a swarm.
- A fallback: wrap the multi-agent call in `try/except` and answer with a single plain agent if it fails.

Orchestrator-as-tools skeleton:

```python
@tool
def specialist(question: str) -> str:
    """What this specialist is good at."""
    sub = Agent(model=MODEL, system_prompt="...", callback_handler=None)
    return say(sub(question))

coordinator = Agent(model=MODEL,
                    system_prompt="Route to the right specialist, then combine the answers.",
                    tools=[specialist], callback_handler=None)
print(say(coordinator("...a question that needs a specialist...")))
```

Graph skeleton, if you go that way:

```python
from strands.multiagent import GraphBuilder

gb = GraphBuilder()
gb.add_node(step_one, "one")
gb.add_node(step_two, "two")
gb.add_edge("one", "two")
gb.set_entry_point("one")
gb.set_max_node_executions(10)   # the cap
graph = gb.build()
```

You are done when: at least two agents collaborate to produce the answer, there is a cap so it cannot run forever, and a failure falls back to a single agent.

Stretch, optional: add a validator step that checks the output and asks for one revision; or print tokens per node to see where the cost goes.

---

## What to hand in

- Your Part A design note.
- A notebook or `.py` file with Parts B to D, as far as you got.
- A short paragraph: what you built, one thing that surprised you, one thing you would improve.

## Two rules

- Keep it lean. The smallest thing that works beats a clever thing that half-works. No over-engineering.
- When stuck on AWS, it is almost always the model-id prefix, the region, or the credentials. Check those three first.
