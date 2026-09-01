"""
Step 10 — the main app (CORE TIER).

A single-turn KB-grounded Q&A loop with guardrail and cost logging.

When this works end-to-end, your Core tier is done.

Usage:
    python 03_app.py
    > Ask: when can I take vacation?
    > (answer with citations)
    > Ask: quit
"""

import os
import json
import time
from datetime import datetime
import boto3

REGION = os.getenv("AWS_REGION", "us-east-1")
KB_ID = os.environ["KB_ID"]
GUARDRAIL_ID = os.environ["GUARDRAIL_ID"]
GUARDRAIL_VERSION = os.environ.get("GUARDRAIL_VERSION", "1")
MODEL_ARN = "us.amazon.nova-lite-v1:0"
COST_LOG_PATH = "cost_log.json"

# Illustrative pricing — replace with your model's actual price.
# Bedrock pricing: https://aws.amazon.com/bedrock/pricing/
INPUT_PRICE_PER_MTOK = 0.06   # $ per 1M input tokens
OUTPUT_PRICE_PER_MTOK = 0.24  # $ per 1M output tokens


def log_cost(question: str, response: dict) -> None:
    """Append a record to cost_log.json for later analysis."""
    # retrieve_and_generate returns usage under a different path than plain Converse.
    # If you don't see usage, log what you can.
    usage = (response.get("guardrailAction") or {})  # placeholder; usage often unavailable here
    # When the underlying generation runs, the agent runtime may not expose token counts
    # the same way Converse does. To get real token numbers, capture them on the call.
    # For Core, we estimate output tokens from response length (~4 chars per token).

    output_text = response.get("output", {}).get("text", "")
    estimated_output_tokens = max(1, len(output_text) // 4)
    estimated_input_tokens = max(1, len(question) // 4)

    cost = (
        (estimated_input_tokens / 1_000_000) * INPUT_PRICE_PER_MTOK
        + (estimated_output_tokens / 1_000_000) * OUTPUT_PRICE_PER_MTOK
    )

    record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "question": question,
        "estimated_input_tokens": estimated_input_tokens,
        "estimated_output_tokens": estimated_output_tokens,
        "cost_usd": round(cost, 6),
        "blocked": _is_blocked(response),
    }

    # Append-only JSONL-style log for easy analysis later
    with open(COST_LOG_PATH, "a") as f:
        f.write(json.dumps(record) + "\n")


def _is_blocked(response: dict) -> bool:
    """Detect whether the guardrail intervened."""
    # Bedrock returns guardrailAction in the response when triggered.
    return response.get("guardrailAction", "NONE") != "NONE"


def ask_kb(question: str) -> dict:
    agent = boto3.client("bedrock-agent-runtime", region_name=REGION)
    return agent.retrieve_and_generate(
        input={"text": question},
        retrieveAndGenerateConfiguration={
            "type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {
                "knowledgeBaseId": KB_ID,
                "modelArn": MODEL_ARN,
                "generationConfiguration": {
                    "guardrailConfiguration": {
                        "guardrailId": GUARDRAIL_ID,
                        "guardrailVersion": GUARDRAIL_VERSION,
                    },
                },
            },
        },
    )


def print_answer(response: dict) -> None:
    print("\n" + response["output"]["text"])

    if _is_blocked(response):
        print("\n[!] Guardrail intervened on this response.")

    citations = response.get("citations", [])
    if citations:
        print("\nSources:")
        seen = set()
        for idx, c in enumerate(citations, 1):
            for ref in c.get("retrievedReferences", []):
                uri = ref.get("location", {}).get("s3Location", {}).get("uri", "?")
                if uri not in seen:
                    print(f"  [{idx}] {uri}")
                    seen.add(uri)


def main():
    print("Bedrock mini-app. Type 'quit' to exit.\n")
    while True:
        question = input("Ask: ").strip()
        if question.lower() in ("quit", "exit", ""):
            print("Bye.")
            break

        try:
            t0 = time.time()
            response = ask_kb(question)
            elapsed = time.time() - t0
            print_answer(response)
            print(f"\n({elapsed:.1f}s)")
            log_cost(question, response)
        except Exception as e:
            print(f"\nERROR: {e}")
            print("Common fixes: confirm KB sync finished; confirm guardrail ID + version; check region.")


if __name__ == "__main__":
    main()
