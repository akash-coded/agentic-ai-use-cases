# How to · Migrate a LangChain agent to Strands (or the reverse)

**Time:** a day for a simple agent. **First:** decide whether you should.

---

## 0. Should you?

| Migrate to Strands when | Stay on LangChain/LangGraph when |
| --- | --- |
| The agent is a tool-calling loop, not a state machine | Control flow is genuinely a graph with branches |
| Team is AWS-native | You depend on the LangChain integration ecosystem |
| You want less framework surface | You need checkpointing and resumability |
| The LangGraph state is doing nothing a loop would not | Existing team knowledge is deep |

> **Migrating for its own sake is a cost with no benefit.** Run
> [the side-by-side notebook](../../../modules/08-langchain-and-langgraph/notebooks/06_langchain_vs_strands_side_by_side.ipynb)
> on your own task before deciding.

## 1. Extract what is portable first

Do this even if you never migrate. It makes the codebase better either way.

| Move out of the framework | Into |
| --- | --- |
| Tool implementations | Plain functions in `tools/` |
| Prompts | Version-controlled files |
| Golden set and evaluation | Framework-free test module |
| Retrieval logic | Its own module |

After this, the framework is a thin orchestration layer — and the migration is small. If it is not small,
the extraction is the real work, and it is worth doing regardless.

## 2. Map the concepts

| LangChain / LangGraph | Strands |
| --- | --- |
| `ChatBedrockConverse` | `BedrockModel` |
| `@tool` (langchain_core) | `@tool` (strands) — docstring + type hints become the schema |
| `llm.bind_tools([...])` | `Agent(tools=[...])` |
| `create_react_agent` | `Agent(...)` — the loop is built in |
| `StateGraph` + conditional edges | `GraphBuilder` |
| Multi-agent supervisor | Agents as tools, or `Swarm` |
| `with_structured_output` | Structured output via tool schema |
| `MemorySaver` checkpointer | Session state / AgentCore Memory |

## 3. Port the tools first

Tools are the highest-value, lowest-risk part. Both frameworks derive the schema from the signature and
docstring, so the change is mechanical:

```python
# LangChain
from langchain_core.tools import tool

# Strands
from strands import tool
```

Keep the docstring identical — it is the model-facing contract, and changing it changes behaviour.

## 4. Port the loop

```python
# LangChain
agent = create_react_agent(llm, tools)
result = agent.invoke({"messages": [("user", q)]})

# Strands
agent = Agent(model=BedrockModel(model_id=MID), tools=tools)
result = agent(q)
```

For a straightforward ReAct-style agent this is most of the migration.

## 5. Port the graph, if there is one

A LangGraph state machine maps to `GraphBuilder`. But first ask: **is the graph doing anything?** Many
LangGraph agents are a single node in a loop, which is just an agent.

```python
from strands.multiagent import GraphBuilder
b = GraphBuilder()
b.add_node(triage, "triage"); b.add_node(refund, "refund")
b.add_edge("triage", "refund"); b.set_entry_point("triage")
graph = b.build()
```

## 6. Prove equivalence with the golden set

This is the step that makes the migration defensible:

| | Pass rate | Abstention | Cost/task | p95 |
| --- | --- | --- | --- | --- |
| LangChain (before) | | | | |
| Strands (after) | | | | |
| Delta | | | | |

**A migration that changes behaviour is not a migration** — it is a rewrite, and it needs its own
evaluation. Watch abstention especially: framework defaults around tool-failure handling differ, and that
shows up as an abstention delta.

## 7. What usually differs

| Area | Watch for |
| --- | --- |
| Tool failure handling | Different defaults on what the model sees after an error |
| Message history shape | Both handle it; they format differently |
| Streaming events | Different event names and granularity |
| Max iterations | Different defaults — **set yours explicitly in both** |
| Structured output | Different mechanisms, different strictness |

## 8. Run both for a while

Keep the old path behind a flag for a release cycle. Compare on the same traffic. Delete the old path only
once the numbers match.

**Related:** [Strands](../../quick-reference/strands.md) · [LangGraph](../../quick-reference/langgraph.md) ·
[Module 08](../../../modules/08-langchain-and-langgraph/)
