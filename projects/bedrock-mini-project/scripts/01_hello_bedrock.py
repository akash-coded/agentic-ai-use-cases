"""
Step 7 — your first Bedrock call.

Run this first. Confirm you can reach Bedrock and get a response back.
If this works, your AWS credentials and region are set up correctly.

Usage:
    export AWS_REGION=us-east-1
    python 01_hello_bedrock.py
"""

import os
import boto3

REGION = os.getenv("AWS_REGION", "us-east-1")

# IMPORTANT: the `us.` prefix is the regional inference-profile prefix.
# Without it you'll get ModelNotFoundException. Use `eu.` for EU regions, etc.
MODEL_ID = "us.amazon.nova-lite-v1:0"


def main():
    client = boto3.client("bedrock-runtime", region_name=REGION)

    response = client.converse(
        modelId=MODEL_ID,
        system=[{"text": "You are a helpful technical assistant. Be concise."}],
        messages=[{
            "role": "user",
            "content": [{"text": "Explain Amazon Bedrock in one short paragraph."}]
        }],
        inferenceConfig={"temperature": 0.3, "maxTokens": 300},
    )

    # The output structure: response > output > message > content[0] > text
    answer = response["output"]["message"]["content"][0]["text"]
    usage = response.get("usage", {})

    print("\n--- ANSWER ---")
    print(answer)
    print("\n--- TOKEN USAGE ---")
    print(f"Input tokens:  {usage.get('inputTokens')}")
    print(f"Output tokens: {usage.get('outputTokens')}")
    print(f"Total tokens:  {usage.get('totalTokens')}")


if __name__ == "__main__":
    main()
