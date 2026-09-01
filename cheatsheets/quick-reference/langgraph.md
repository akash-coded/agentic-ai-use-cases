# LangChain and LangGraph — Cheat Sheet

The ecosystem you will meet in most existing codebases. LangChain composes; LangGraph adds state.

```bash
pip install langchain langchain-aws langgraph
```

---

## Bedrock as the model

```python
from langchain_aws import ChatBedrockConverse

llm = ChatBedrockConverse(
    model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    region_name="us-east-1",
    temperature=0.2,
)
```

`ChatBedrockConverse` uses the [Converse API](bedrock-converse.md) underneath — the same model-ID and
inference-profile rules apply.

## Composition — the pipe

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a travel operations assistant. Cite policy for every claim."),
    ("human", "{question}")])

chain = prompt | llm | StrOutputParser()
chain.invoke({"question": "Is a cancelled-flight refund automatic?"})
```

Anything implementing `invoke` / `stream` / `batch` is a Runnable and composes with `|`.

> If a plain function would do, use a plain function. A one-step chain is indirection with no benefit.

## Structured output

```python
from pydantic import BaseModel, Field

class RefundDecision(BaseModel):
    eligible: bool = Field(description="Whether the booking is refundable")
    citation: str  = Field(description="Policy clause supporting the decision")
    confidence: str = Field(description="high | medium | abstain")

structured = llm.with_structured_output(RefundDecision)
structured.invoke("Booking XY7Q2M, flight cancelled by carrier. Refundable?")
```

Note `confidence: abstain` as a first-class value — see
[Abstention Budget](../frameworks/abstention-budget.md).

## Tools

```python
from langchain_core.tools import tool

@tool
def get_fare_rules(fare_class: str) -> dict:
    """Retrieve fare rules for a fare class: change fees, refund eligibility, conditions.

    Use after get_booking, which gives you the fare class.
    Does NOT know about a specific booking's status.
    """
    return rules_for(fare_class)

llm_with_tools = llm.bind_tools([get_fare_rules])
```

## LangGraph — state machines

```python
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]   # reducer merges across nodes
    citations: list

def triage(state: State) -> dict:
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

def should_continue(state: State) -> str:
    return "tools" if state["messages"][-1].tool_calls else END

g = StateGraph(State)
g.add_node("triage", triage)
g.add_node("tools", tool_node)
g.set_entry_point("triage")
g.add_conditional_edges("triage", should_continue, {"tools": "tools", END: END})
g.add_edge("tools", "triage")
app = g.compile()
```

**The three concepts:** typed state with reducers, nodes that return partial state, conditional edges that
return the next node's name.

## Checkpointing — resumable, and the thing that grows

```python
from langgraph.checkpoint.memory import MemorySaver

app = g.compile(checkpointer=MemorySaver())
app.invoke({"messages": [("user", "Is XY7Q2M refundable?")]},
           config={"configurable": {"thread_id": "session-42"}})
```

State persists per `thread_id`. It is not free: unbounded state is
[cliff 4](../frameworks/cost-cliff-map.md) on the cost map. Cap it.

## Streaming

```python
for chunk in app.stream({"messages": [("user", q)]}, config=cfg, stream_mode="updates"):
    print(chunk)
```

`stream_mode`: `values` (full state), `updates` (deltas), `messages` (token-level).

## LangChain vs Strands — how to choose

| Choose | When |
| --- | --- |
| **Strands** | AWS-native, starting fresh, want the smallest path to a working agent |
| **LangGraph** | Control flow genuinely needs to be explicit; you need checkpointing and resumability |
| **LangChain** | You are joining an existing codebase — which is most people |

Not a rivalry. [Module 08 runs the same task in both](../../modules/08-langchain-and-langgraph/notebooks/06_langchain_vs_strands_side_by_side.ipynb)
and lets the comparison stand.

## Common mistakes

| Symptom | Cause |
| --- | --- |
| Chains everywhere, nothing clearer | Cargo-culting composition; a function would do |
| Checkpoint size climbing | Unbounded state; no reducer trimming |
| Graph loops forever | Conditional edge never returns `END` |
| Cannot tell which node failed | No per-node logging |

## Learn it properly

[Module 08](../../modules/08-langchain-and-langgraph/) ·
[LangGraph: chains to swarms](../../modules/08-langchain-and-langgraph/notebooks/PierPoint_LangGraph_Chains_to_Swarms.ipynb) ·
[Module 08 LLD](../../docs/architecture/lld/08-langchain-and-langgraph.md)
