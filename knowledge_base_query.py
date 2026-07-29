"""
Query an Amazon Bedrock MANAGED Knowledge Base (managed vector store + S3 data source).

Note:
    retrieve_and_generate() is NOT supported on Managed Knowledge Bases.
    It throws: ValidationException: This operation is not supported for managed knowledge bases.

Managed KBs expose two query surfaces:
    1. retrieve()                -> raw chunks. You generate the answer yourself. (used below)
    2. agentic_retrieve_stream() -> planner loop + optional grounded answer, streaming.

Requires boto3 >= 1.43
"""

import boto3
from botocore.exceptions import ClientError

REGION = "us-east-1"
KNOWLEDGE_BASE_ID = "FDTMUR7OOR"
MODEL_ID = "us.amazon.nova-lite-v1:0"   # inference profile ID, 'us.' prefix is mandatory

agent_runtime = boto3.client("bedrock-agent-runtime", region_name=REGION)
bedrock_runtime = boto3.client("bedrock-runtime", region_name=REGION)


# ----------------------------------------------------------------------
# Option 1: Retrieve + Converse  (RAG, done in two explicit steps)
# ----------------------------------------------------------------------
def query_knowledge_base(question, num_results=5):
    print("Querying Bedrock Managed Knowledge Base")
    print("=" * 60)
    print(f"Knowledge Base ID: {KNOWLEDGE_BASE_ID}")
    print(f"Question: {question}\n")

    try:
        # STEP 1 - retrieve chunks
        # managedSearchConfiguration, NOT vectorSearchConfiguration.
        # vectorSearchConfiguration is for customer-managed (OpenSearch/Aurora/Pinecone) KBs.
        retrieval = agent_runtime.retrieve(
            knowledgeBaseId=KNOWLEDGE_BASE_ID,
            retrievalQuery={"text": question},
            retrievalConfiguration={
                "managedSearchConfiguration": {
                    "numberOfResults": num_results,
                    # "rerankingModelType": "MANAGED",  # default; NONE or CUSTOM also valid
                }
            },
        )

        chunks = retrieval.get("retrievalResults", [])
        if not chunks:
            print("No chunks retrieved. Check that the data source has finished syncing.")
            return

        context = "\n\n".join(c["content"]["text"] for c in chunks)

        # STEP 2 - generate the answer with the retrieved context
        prompt = (
            "Answer the question using ONLY the context below. "
            "If the context does not contain the answer, say so.\n\n"
            f"<context>\n{context}\n</context>\n\n"
            f"Question: {question}"
        )

        generation = bedrock_runtime.converse(
            modelId=MODEL_ID,
            messages=[{"role": "user", "content": [{"text": prompt}]}],
            inferenceConfig={"maxTokens": 512, "temperature": 0.2},
        )

        answer = generation["output"]["message"]["content"][0]["text"]

        print("Answer:")
        print(answer)
        print("\nSources:")
        for i, c in enumerate(chunks, 1):
            uri = c.get("location", {}).get("s3Location", {}).get("uri", "unknown")
            print(f"  [{i}] score={c.get('score'):.4f}  {uri}")

    except ClientError as e:
        print(f"Error querying Knowledge Base: {e}")
        print("\nCheck:")
        print("  1. KB status is Available and the S3 data source sync completed")
        print("  2. IAM allows bedrock:Retrieve on the KB ARN and bedrock:InvokeModel")
        print("  3. boto3 >= 1.43 (pip install -U boto3 botocore)")


# ----------------------------------------------------------------------
# Option 2: Agentic retrieval  (planner loop, generates the answer itself)
# Use for multi-part / comparative questions. Costs more, higher latency.
# ----------------------------------------------------------------------
def query_agentic(question, max_results=10, max_iterations=3):
    print(f"Question: {question}\n")

    response = agent_runtime.agentic_retrieve_stream(
        messages=[{"role": "user", "content": {"text": question}}],
        retrievers=[
            {
                "configuration": {
                    "knowledgeBase": {
                        "knowledgeBaseId": KNOWLEDGE_BASE_ID,
                        "retrievalOverrides": {"maxNumberOfResults": max_results},
                    }
                }
            }
        ],
        agenticRetrieveConfiguration={
            "foundationModelType": "MANAGED",   # service-managed planner; no modelArn needed
            "maxAgentIteration": max_iterations,
        },
    )

    for event in response["stream"]:
        if "traceEvent" in event:
            attrs = event["traceEvent"]["attributes"]
            print(f"[TRACE] step={attrs.get('step')} status={attrs.get('status')}")
        elif "responseEvent" in event:
            print(event["responseEvent"]["text"], end="", flush=True)
        elif "result" in event:
            print("\n\nSources:")
            for c in event["result"].get("results", []):
                uri = c.get("location", {}).get("s3Location", {}).get("uri", "unknown")
                print(f"  - {uri}")


if __name__ == "__main__":
    query_knowledge_base("When is spring break this year?")
    # query_agentic("Compare the spring break and winter break policies.")