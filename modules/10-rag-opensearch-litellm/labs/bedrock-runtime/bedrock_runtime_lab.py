"""
TravelMind - Bedrock runtime lab (boto3)
Three ways to consume a Knowledge Base from code, smallest to largest:
    retrieve              -> raw chunks, you build the prompt
    retrieve_and_generate -> chunks + a finished answer in one call
    invoke_agent          -> drive a full Agent-Builder agent (event stream)

Account 123456789012  |  region us-east-1  |  client = bedrock-agent-runtime

------------------------------------------------------------------------------
THE TWO LOCKS, IN THIS LAB
------------------------------------------------------------------------------
You call as YOUR identity. The KB does the vector work on your behalf.

  YOU (your IAM identity)                KB SERVICE ROLE (only if KB is OSS-backed)
  +-------------------------+            +--------------------------------------+
  | Lock 1 - IAM            |            | Lock 1 - aoss:APIAccessAll (IAM)     |
  |  bedrock:Retrieve       |  --KB-->   | Lock 2 - role ARN in the collection  |  --> vectors
  |  bedrock:InvokeAgent    |            |          data access policy          |
  +-------------------------+            +--------------------------------------+
            ^                            (S3 Vectors KB = no Lock 2 at all)
            |
   this is the only lock YOUR code has to clear

If your call 403s -> it is Lock 1 on YOU (missing bedrock:* action).
If the KB's sync/query 403s with "no index access" -> it is Lock 2 on the KB role.

------------------------------------------------------------------------------
RUN IT  (pick one)
------------------------------------------------------------------------------
VS Code
  1. python -m venv .venv && source .venv/bin/activate      # Win: .venv\\Scripts\\activate
     pip install boto3
  2. set creds: aws configure        (or export AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY
                                       / AWS_DEFAULT_REGION=us-east-1)
     then pick .venv as the interpreter (Cmd Palette -> Python: Select Interpreter)
  3. fill KB_ID / AGENT_ID / AGENT_ALIAS_ID below, then run this file

Google Colab
  1. !pip install boto3
  2. creds via Colab secrets (key icon, left bar), then:
        import os
        from google.colab import userdata
        os.environ["AWS_ACCESS_KEY_ID"]     = userdata.get("AWS_ACCESS_KEY_ID")
        os.environ["AWS_SECRET_ACCESS_KEY"] = userdata.get("AWS_SECRET_ACCESS_KEY")
        os.environ["AWS_DEFAULT_REGION"]    = "us-east-1"
  3. fill the IDs, run

AWS CloudShell
  1. boto3 is preinstalled; creds are already present (you are signed in)
  2. fill the IDs, then: python bedrock_runtime_lab.py
"""

import os
import uuid
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

# --------------------------------------------------------------------------
# CONFIG  -  fill these three from the console, leave the rest
# --------------------------------------------------------------------------
REGION         = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
KB_ID          = "REPLACE_KB_ID"          # Bedrock -> Knowledge Bases -> your KB -> Knowledge base ID
AGENT_ID       = "REPLACE_AGENT_ID"       # Bedrock -> Agents -> your agent -> Agent ID
AGENT_ALIAS_ID = "REPLACE_AGENT_ALIAS"    # the alias you made after Prepare (not the draft)

# modelArn for retrieve_and_generate. The us. prefix = cross-region inference profile.
# Forgetting that prefix is the classic break. Copy the exact ARN from the console
# (Bedrock -> Inference profiles) if this version string is stale.
MODEL_ARN = f"arn:aws:bedrock:{REGION}:123456789012:inference-profile/us.anthropic.claude-sonnet-4-REPLACE"

# adaptive retries so throttling does not surface as a hard error
rt = boto3.client(
    "bedrock-agent-runtime",
    region_name=REGION,
    config=Config(retries={"max_attempts": 5, "mode": "adaptive"}),
)


# --------------------------------------------------------------------------
# 1) retrieve  -  raw chunks + scores, you do the generation yourself
# --------------------------------------------------------------------------
def retrieve_chunks(query, top_k=5):
    r = rt.retrieve(
        knowledgeBaseId=KB_ID,
        retrievalQuery={"text": query},
        retrievalConfiguration={
            "vectorSearchConfiguration": {"numberOfResults": top_k}
        },
    )
    results = r["retrievalResults"]
    for i, c in enumerate(results, 1):
        score = c.get("score", 0.0)
        text = c["content"]["text"]
        loc = c.get("location", {})
        print(f"[{i}] score={score:.3f}")
        print(f"    {text[:280].strip()}")
        print(f"    source={loc}\n")
    return results

# WHAT CHANGES IN PRODUCTION
#  - scope IAM to the exact KB ARN, not "*": bedrock:Retrieve on
#    arn:aws:bedrock:us-east-1:123456789012:knowledge-base/<KB_ID>
#  - tune numberOfResults to your context budget; do not dump every chunk into the prompt
#  - never log raw chunk text if it can contain PII


# --------------------------------------------------------------------------
# 2) retrieve_and_generate  -  retrieval + a model answer with citations, one call
# --------------------------------------------------------------------------
def answer(query, session_id=None):
    cfg = {
        "type": "KNOWLEDGE_BASE",
        "knowledgeBaseConfiguration": {
            "knowledgeBaseId": KB_ID,
            "modelArn": MODEL_ARN,
        },
    }
    kwargs = {"input": {"text": query}, "retrieveAndGenerateConfiguration": cfg}
    if session_id:                       # reuse to continue a multi-turn session
        kwargs["sessionId"] = session_id

    r = rt.retrieve_and_generate(**kwargs)

    print(r["output"]["text"], "\n")
    for cit in r.get("citations", []):
        for ref in cit.get("retrievedReferences", []):
            snippet = ref["content"]["text"][:110].strip()
            print(f"  cite: {snippet} -> {ref.get('location')}")
    return r["sessionId"], r            # hand sessionId back for the next turn

# WHAT CHANGES IN PRODUCTION
#  - IAM: bedrock:RetrieveAndGenerate + bedrock:InvokeModel on the chosen inference profile
#  - the region must match the KB; cross-region inference adds $0.02/GB data transfer
#  - pick the model deliberately; do not leave a stale or oversized model wired in
#  - catch ClientError (ThrottlingException, AccessDeniedException) and back off


# --------------------------------------------------------------------------
# 3) invoke_agent  -  full Agent-Builder agent, response is an event stream
# --------------------------------------------------------------------------
def ask_agent(text, session_id=None, trace=False):
    session_id = session_id or str(uuid.uuid4())
    resp = rt.invoke_agent(
        agentId=AGENT_ID,
        agentAliasId=AGENT_ALIAS_ID,
        sessionId=session_id,
        inputText=text,
        enableTrace=trace,              # True surfaces the agent's reasoning/tool steps
    )

    chunks = []
    for event in resp["completion"]:    # EventStream - you MUST iterate it
        if "chunk" in event:
            chunks.append(event["chunk"]["bytes"].decode("utf-8"))
        elif "trace" in event and trace:
            # event["trace"]["trace"] holds orchestration / KB-lookup / tool steps
            print("  [trace]", list(event["trace"]["trace"].keys()))
    out = "".join(chunks)
    print(out)
    return session_id, out              # reuse session_id to continue the conversation

# WHAT CHANGES IN PRODUCTION
#  - use a versioned alias, never the draft / TSTALIASID
#  - IAM: bedrock:InvokeAgent on the specific agent-alias ARN
#  - the AGENT runs as its own service role (AmazonBedrockExecutionRoleForAgents_*);
#    your identity only needs InvokeAgent, the agent role needs Retrieve + lambda:InvokeFunction
#  - handle partial failures mid-stream; the stream can error after the first chunk
#  - turn enableTrace off in prod (verbose + costs); keep it for staging debugging


# --------------------------------------------------------------------------
# DEMO
# --------------------------------------------------------------------------
if __name__ == "__main__":
    q = "How much checked baggage is included on a TravelMind economy fare?"
    try:
        print("=== retrieve (chunks only) ===")
        retrieve_chunks(q)

        print("\n=== retrieve_and_generate (answer + citations) ===")
        sid, _ = answer(q)
        # follow-up on the same session:
        # answer("And what about cabin baggage?", session_id=sid)

        print("\n=== invoke_agent (full agent) ===")
        ask_agent(q, trace=False)

    except ClientError as e:
        code = e.response["Error"]["Code"]
        print(f"\nAWS error [{code}]: {e.response['Error']['Message']}")
        if code in ("AccessDeniedException", "AccessDenied"):
            print("Lock 1 on YOU: check bedrock:Retrieve / RetrieveAndGenerate / InvokeAgent.")
        elif code == "ResourceNotFoundException":
            print("Check KB_ID / AGENT_ID / AGENT_ALIAS_ID and the region.")
        elif code in ("ThrottlingException", "TooManyRequestsException"):
            print("Throttled even with adaptive retries; slow down or request a quota bump.")
