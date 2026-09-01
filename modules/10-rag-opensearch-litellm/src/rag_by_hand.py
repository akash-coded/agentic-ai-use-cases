"""
TravelMind - RAG by hand (no Knowledge Base)
Hit your OpenSearch index directly, then generate with the Converse API.

    query -> embed (Titan) -> kNN on YOUR index (OpenSearch) -> stuff context -> converse -> answer

No KB means no managed retrieval and no KB service role. So the two locks land on YOU:
    Lock 1 (IAM):  aoss:APIAccessAll on your identity
    Lock 2 (data): your ARN listed in the collection's data access policy
Miss either and the search 403s. With a KB, the KB role held these; here you hold both.

------------------------------------------------------------------------------
RUN IT  (pick one)
------------------------------------------------------------------------------
VS Code
  1. python -m venv .venv && source .venv/bin/activate     # Win: .venv\\Scripts\\activate
     pip install opensearch-py boto3
  2. aws configure   (or env AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY / AWS_DEFAULT_REGION=us-east-1)
     export AOSS_HOST=<collection-endpoint-host>     # bare host, no https://, no port
     export MY_NAME=<you>                            # picks your index travelmind-<you>
     then select .venv as the interpreter and run
  3. fill GEN_MODEL with your exact inference-profile id, run

Google Colab
  1. !pip install opensearch-py boto3
  2. creds via Colab secrets -> os.environ; then
        os.environ["AOSS_HOST"] = "<collection-endpoint-host>"
        os.environ["MY_NAME"]   = "<you>"
        os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
  3. run

AWS CloudShell
  1. pip install opensearch-py --user      # boto3 + creds already present
  2. export AOSS_HOST=<host> ; export MY_NAME=<you> ; python rag_by_hand.py
"""

import os
import json
import boto3
from botocore.config import Config
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth

# --------------------------------------------------------------------------
# CONFIG
# --------------------------------------------------------------------------
REGION      = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
HOST        = os.environ["AOSS_HOST"]                       # bare hostname, no scheme, no port
INDEX       = f"travelmind-{os.environ.get('MY_NAME', 'asha')}"
EMBED_MODEL = "amazon.titan-embed-text-v2:0"                # 1024-dim, matches your index mapping
GEN_MODEL   = "us.anthropic.claude-sonnet-4-REPLACE"        # inference-profile id; us. prefix is mandatory
TOP_K       = 4

# OpenSearch client - SigV4, and the service is "aoss" (NOT "es"). Wrong service = SignatureDoesNotMatch.
auth = AWSV4SignerAuth(boto3.Session().get_credentials(), REGION, "aoss")
oss = OpenSearch(
    hosts=[{"host": HOST, "port": 443}],
    http_auth=auth, use_ssl=True, verify_certs=True,
    connection_class=RequestsHttpConnection,
)
br = boto3.client("bedrock-runtime", region_name=REGION,
                  config=Config(retries={"max_attempts": 5, "mode": "adaptive"}))


# --------------------------------------------------------------------------
# embed -> kNN retrieve, straight against your index
# --------------------------------------------------------------------------
def embed(text):
    r = br.invoke_model(modelId=EMBED_MODEL,
                        body=json.dumps({"inputText": text, "normalize": True}))
    return json.loads(r["body"].read())["embedding"]

def retrieve(query, k=TOP_K):
    qv = embed(query)
    res = oss.search(index=INDEX, body={
        "size": k,
        "query": {"knn": {"embedding": {"vector": qv, "k": k}}},   # field name from your mapping
        "_source": ["text", "source"],
    })
    return [h["_source"] for h in res["hits"]["hits"]]


# --------------------------------------------------------------------------
# converse for the answer (model-agnostic; same shape for any text model)
# --------------------------------------------------------------------------
def answer(query):
    chunks = retrieve(query)
    context = "\n\n".join(f"[{i+1}] {c['text']}" for i, c in enumerate(chunks))
    r = br.converse(
        modelId=GEN_MODEL,
        system=[{"text": "Answer only from the context. Cite sources as [n]. "
                         "If the answer is not in the context, say you don't know."}],
        messages=[{"role": "user",
                   "content": [{"text": f"Context:\n{context}\n\nQuestion: {query}"}]}],
        inferenceConfig={"maxTokens": 400, "temperature": 0},
    )
    print(r["output"]["message"]["content"][0]["text"])
    return r

# WHAT CHANGES IN PRODUCTION
#  - IAM role, not keys: scope bedrock:InvokeModel to the two model ARNs, aoss:APIAccessAll to the collection
#  - read HOST / INDEX / GEN_MODEL from env or SSM; nothing hardcoded
#  - cap k and chunk size to your context + cost budget; do not dump the whole index into the prompt
#  - add timeouts; catch ClientError and back off on throttling
#  - newly ingested docs lag ~30s before they are searchable (matters on write, not on this read)
#  - do not log raw user queries or retrieved chunks if they can contain PII


if __name__ == "__main__":
    answer("How much checked baggage is included on a TravelMind economy fare?")
