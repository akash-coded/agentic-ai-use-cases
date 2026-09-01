"""
OpenSearch Serverless (AOSS) vector search - student lab
Agentic AI Practitioner Bootcamp - Day 3, Amazon Bedrock

What you build: a tiny vector index inside the SHARED collection, ingest a few
TravelMind FAQ snippets embedded with Amazon Titan, then run a kNN search.

You do NOT create a collection. Your instructor created one shared collection.
You create your OWN index inside it, namespaced with your name.

==================================================================
RUN STEPS
==================================================================
CloudShell (easiest - credentials already present):
  1. pip install opensearch-py boto3 --quiet
  2. export AOSS_HOST=<id>.us-east-1.aoss.amazonaws.com   # from your instructor
  3. export MY_NAME=<your-first-name>
  4. python opensearch_lab.py

VS Code (local):
  1. python -m venv .venv && source .venv/bin/activate    # Win: .venv\\Scripts\\activate
  2. pip install opensearch-py boto3
  3. aws configure        # or set AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY
  4. set AOSS_HOST and MY_NAME, select .venv as the interpreter, run

Google Colab:
  1. !pip install opensearch-py boto3 --quiet
  2. import os; os.environ["AWS_ACCESS_KEY_ID"]=...   # use Colab secrets, not hardcoded keys
  3. os.environ["AOSS_HOST"]=...; os.environ["MY_NAME"]=...
  4. run the cells
"""

import os, json, time
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth

REGION      = "us-east-1"
SERVICE     = "aoss"                  # LOCK 1 detail: serverless is "aoss", NOT "es"
HOST        = os.environ["AOSS_HOST"] # bare host, e.g. abc123.us-east-1.aoss.amazonaws.com
MY_NAME     = os.environ.get("MY_NAME", "demo").lower()
INDEX       = f"travelmind-{MY_NAME}" # your own index inside the shared collection
EMBED_MODEL = "amazon.titan-embed-text-v2:0"
DIM         = 1024                    # Titan V2 default; MUST match the mapping

# ---- clients -----------------------------------------------------
creds = boto3.Session().get_credentials()
auth  = AWSV4SignerAuth(creds, REGION, SERVICE)
client = OpenSearch(
    hosts=[{"host": HOST, "port": 443}],
    http_auth=auth, use_ssl=True, verify_certs=True,
    connection_class=RequestsHttpConnection, pool_maxsize=20,
)
brt = boto3.client("bedrock-runtime", region_name=REGION)

def embed(text: str):
    body = json.dumps({"inputText": text, "dimensions": DIM, "normalize": True})
    r = brt.invoke_model(modelId=EMBED_MODEL, body=body)
    return json.loads(r["body"].read())["embedding"]

# ---- 1. index mapping --------------------------------------------
MAPPING = {
    "settings": {"index.knn": True},
    "mappings": {
        "properties": {
            "embedding": {
                "type": "knn_vector",
                "dimension": DIM,
                "method": {"name": "hnsw", "engine": "faiss", "space_type": "l2"},
            },
            "text":   {"type": "text"},
            "source": {"type": "keyword"},
        }
    },
}

def create_index():
    if client.indices.exists(INDEX):
        print(f"index {INDEX} already exists, skipping create")
        return
    client.indices.create(index=INDEX, body=MAPPING)
    print(f"created index {INDEX}")
    time.sleep(5)   # AOSS is near-real-time; give the new index a moment

# ---- 2. ingest ---------------------------------------------------
DOCS = [
    ("Checked bags over 23 kg incur an excess weight fee per piece.", "baggage-policy"),
    ("Free date changes are allowed on flexible fares up to 24h before departure.", "fare-rules"),
    ("Meal preferences must be set at least 24 hours before the flight.", "meals"),
    ("Lounge access is included for business class and gold-tier members.", "loyalty"),
    ("Cabin pets are limited to one carrier per passenger under 8 kg.", "pets"),
]

def ingest():
    for text, source in DOCS:
        client.index(index=INDEX, body={"text": text, "source": source, "embedding": embed(text)})
    print(f"ingested {len(DOCS)} docs")
    time.sleep(30)  # wait for them to become searchable (not instant)

# ---- 3. kNN query ------------------------------------------------
def search(question: str, k: int = 3):
    qvec = embed(question)
    body = {
        "size": k,
        "query": {"knn": {"embedding": {"vector": qvec, "k": k}}},
        "_source": ["text", "source"],
    }
    res = client.search(index=INDEX, body=body)
    print(f"\nQ: {question}")
    for hit in res["hits"]["hits"]:
        print(f"  {hit['_score']:.3f}  [{hit['_source']['source']}]  {hit['_source']['text']}")

if __name__ == "__main__":
    create_index()
    ingest()
    search("how much luggage can I bring?")
    search("can I change my flight date?")

# ==================================================================
# WHAT CHANGES IN PRODUCTION
# ==================================================================
# - Credentials: use an IAM role (Lambda / ECS task role), never access keys
#   or the long-lived keys you minted for this lab.
# - service stays "aoss" for Serverless; it is "es" only for managed domains.
# - Data access policy: list only the exact roles that need it, and split read
#   vs write principals. Do not grant the whole class write like the lab does.
# - Network policy: AllowFromPublic is fine for a lab. In prod use a VPC /
#   private network policy so the collection is not internet-facing.
# - Ingest with the _bulk helper, add retries, and tune the HNSW method
#   (ef_construction, m) for your recall and latency target.
