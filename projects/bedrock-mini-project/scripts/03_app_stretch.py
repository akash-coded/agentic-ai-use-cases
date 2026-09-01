"""
Stretch tier — multi-turn conversation with one custom tool.

This is what 03_app.py becomes when you complete the Stretch tier.

Two big changes vs Core:
  1) conversation_history is now MULTI-TURN (history grows turn over turn)
  2) The app routes between KB (retrieve_and_generate) and TOOL (Converse + toolConfig)
     based on whether the model decides to use a tool

For a clean implementation, this STRETCH version uses plain Converse + the @tool you
defined in tools.py. The KB is exposed as another tool the model can call.

Run:
    python 03_app_stretch.py
"""

import os
import json
import time
from datetime import datetime
import boto3

from tools import TOOL_CONFIG, run_tool

REGION = os.getenv("AWS_REGION", "us-east-1")
KB_ID = os.environ["KB_ID"]
GUARDRAIL_ID = os.environ["GUARDRAIL_ID"]
GUARDRAIL_VERSION = os.environ.get("GUARDRAIL_VERSION", "1")
MODEL_ID = "us.amazon.nova-lite-v1:0"
COST_LOG_PATH = "cost_log.json"

INPUT_PRICE_PER_MTOK = 0.06
OUTPUT_PRICE_PER_MTOK = 0.24


# ─── System prompt — explicit tool routing ────────────────────────────
SYSTEM_PROMPT = """You are an internal assistant.

Tool selection rules:
- For employee-specific data (vacation balance, order status, dates), use the available tools.
- For policy questions or anything that would be in our docs, retrieve from the knowledge base by calling retrieve_kb.
- Cite sources when you reference policy or documents.
- If unsure, say so. Do not invent specifics."""


# ─── Wrap the KB as a tool too (so the model decides per turn) ─────────
KB_TOOL_SPEC = {
    "toolSpec": {
        "name": "retrieve_kb",
        "description": (
            "Search the internal knowledge base for policy/document content. "
            "Use this for any question about company policies, processes, or documented procedures. "
            "Returns relevant document snippets with their source URIs."
        ),
        "inputSchema": {
            "json": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query — a natural-language question or phrase.",
                    },
                },
                "required": ["query"],
            }
        },
    }
}


def retrieve_from_kb(query: str) -> dict:
    """Call Bedrock KB retrieve (not retrieve_and_generate — we want raw chunks)."""
    agent = boto3.client("bedrock-agent-runtime", region_name=REGION)
    response = agent.retrieve(
        knowledgeBaseId=KB_ID,
        retrievalQuery={"text": query},
        retrievalConfiguration={
            "vectorSearchConfiguration": {"numberOfResults": 4}
        },
    )
    results = []
    for r in response.get("retrievalResults", []):
        results.append({
            "text": r.get("content", {}).get("text", ""),
            "source": r.get("location", {}).get("s3Location", {}).get("uri", "unknown"),
        })
    return {"results": results}


# ─── Extend the tool dispatch to include KB ────────────────────────────
def dispatch(tool_name: str, tool_input: dict) -> dict:
    if tool_name == "retrieve_kb":
        return retrieve_from_kb(tool_input["query"])
    return run_tool(tool_name, tool_input)


def make_full_tool_config():
    """Combine the custom tools from tools.py with our KB-as-a-tool."""
    return {"tools": TOOL_CONFIG["tools"] + [KB_TOOL_SPEC]}


# ─── Conversation loop ────────────────────────────────────────────────
def main():
    client = boto3.client("bedrock-runtime", region_name=REGION)
    full_tool_config = make_full_tool_config()
    conversation_history: list = []

    print("Bedrock Stretch app — multi-turn + tool routing. Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("quit", "exit", ""):
            print("Bye.")
            break

        # Add the user message to history
        conversation_history.append({
            "role": "user",
            "content": [{"text": user_input}],
        })

        # First Converse call — model may request a tool
        try:
            response = client.converse(
                modelId=MODEL_ID,
                system=[{"text": SYSTEM_PROMPT}],
                messages=conversation_history,
                toolConfig=full_tool_config,
                inferenceConfig={"temperature": 0.3, "maxTokens": 800},
                guardrailConfig={
                    "guardrailIdentifier": GUARDRAIL_ID,
                    "guardrailVersion": GUARDRAIL_VERSION,
                },
            )
        except Exception as e:
            print(f"\nERROR on first call: {e}\n")
            conversation_history.pop()  # remove the unanswered user message
            continue

        stop_reason = response["stopReason"]
        assistant_message = response["output"]["message"]

        # If the model requested a tool, run it and feed the result back
        while stop_reason == "tool_use":
            # Append the model's tool-use message FIRST (critical — easy to forget)
            conversation_history.append(assistant_message)

            # Find the toolUse block(s) — there can be more than one
            tool_use_blocks = [b["toolUse"] for b in assistant_message["content"] if "toolUse" in b]

            # Run all requested tools and build the toolResult content array
            tool_result_content = []
            for tub in tool_use_blocks:
                result = dispatch(tub["name"], tub["input"])
                tool_result_content.append({
                    "toolResult": {
                        "toolUseId": tub["toolUseId"],
                        "content": [{"json": result}],
                    }
                })

            # Append a user message containing all tool results
            conversation_history.append({
                "role": "user",
                "content": tool_result_content,
            })

            # Second Converse call — model uses the tool result to write the final answer
            try:
                response = client.converse(
                    modelId=MODEL_ID,
                    system=[{"text": SYSTEM_PROMPT}],
                    messages=conversation_history,
                    toolConfig=full_tool_config,
                    inferenceConfig={"temperature": 0.3, "maxTokens": 800},
                    guardrailConfig={
                        "guardrailIdentifier": GUARDRAIL_ID,
                        "guardrailVersion": GUARDRAIL_VERSION,
                    },
                )
            except Exception as e:
                print(f"\nERROR on second call: {e}\n")
                break

            stop_reason = response["stopReason"]
            assistant_message = response["output"]["message"]

        # Append the final assistant message to history (also easy to forget)
        conversation_history.append(assistant_message)

        # Extract the final text
        final_text = ""
        for block in assistant_message["content"]:
            if "text" in block:
                final_text += block["text"]
        print(f"\nAssistant: {final_text}\n")

        # Log cost
        usage = response.get("usage", {})
        cost = (
            (usage.get("inputTokens", 0) / 1_000_000) * INPUT_PRICE_PER_MTOK
            + (usage.get("outputTokens", 0) / 1_000_000) * OUTPUT_PRICE_PER_MTOK
        )
        record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "user_input": user_input[:120],
            "input_tokens": usage.get("inputTokens"),
            "output_tokens": usage.get("outputTokens"),
            "tool_used": stop_reason != "end_turn",
            "cost_usd": round(cost, 6),
        }
        with open(COST_LOG_PATH, "a") as f:
            f.write(json.dumps(record) + "\n")


if __name__ == "__main__":
    main()
