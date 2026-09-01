"""
Steps 8-9 — query the Knowledge Base with a Guardrail attached.

PREREQUISITES:
  - Knowledge Base created in Bedrock console, sync complete
  - Guardrail created in Bedrock console with at least one denied topic
  - Set env vars:
      export AWS_REGION=us-east-1
      export KB_ID=YOUR_KB_ID
      export GUARDRAIL_ID=YOUR_GUARDRAIL_ID
      export GUARDRAIL_VERSION=1

Usage:
    python 02_kb_query.py "What is our remote-work policy?"
"""

import os
import sys
import boto3

REGION = os.getenv("AWS_REGION", "us-east-1")
KB_ID = os.environ["KB_ID"]
GUARDRAIL_ID = os.environ["GUARDRAIL_ID"]
GUARDRAIL_VERSION = os.environ.get("GUARDRAIL_VERSION", "1")

# This is the model the KB will use to GENERATE the answer.
# (Embeddings are configured separately, at KB-creation time.)
MODEL_ARN = "us.amazon.nova-lite-v1:0"


def query_kb_with_guardrail(question: str) -> dict:
    """Send a question to the KB; return the full response dict."""
    agent = boto3.client("bedrock-agent-runtime", region_name=REGION)
    # ^^^ NOT bedrock-runtime. KB calls live on the agent-runtime API surface.

    response = agent.retrieve_and_generate(
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
    return response


def print_result(response: dict) -> None:
    answer = response["output"]["text"]
    print("\n--- ANSWER ---")
    print(answer)

    citations = response.get("citations", [])
    if citations:
        print("\n--- CITATIONS ---")
        seen = set()
        for idx, citation in enumerate(citations, 1):
            for ref in citation.get("retrievedReferences", []):
                location = ref.get("location", {})
                s3 = location.get("s3Location", {})
                uri = s3.get("uri", "Unknown")
                if uri not in seen:
                    print(f"  [{idx}] {uri}")
                    seen.add(uri)
    else:
        print("\n!!! NO CITATIONS — your KB is probably empty or your query didn't match. Check KB sync.")


def main():
    question = sys.argv[1] if len(sys.argv) > 1 else "What is our remote-work policy?"
    response = query_kb_with_guardrail(question)
    print_result(response)


if __name__ == "__main__":
    main()
