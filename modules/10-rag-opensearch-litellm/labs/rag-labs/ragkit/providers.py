"""Provider switch. Offline by default; AWS Bedrock when configured.

Set environment variables before importing, or call configure() in a cell:

    RAGKIT_PROVIDER=mock                      (default, no network, no keys)
    RAGKIT_PROVIDER=bedrock
    AWS_REGION=us-east-1                      (or any region with the models enabled)
    RAGKIT_BEDROCK_KB_ID=<knowledge base id>  (optional: swaps the in-memory retriever for a Bedrock KB)
    RAGKIT_BEDROCK_LLM=<model id>             (default amazon.nova-lite-v1:0)
    RAGKIT_BEDROCK_EMBED=<model id>           (default amazon.titan-embed-text-v2:0)

API surface verified against AWS documentation on 2026-08-31:
  bedrock-agent-runtime.retrieve(knowledgeBaseId, retrievalQuery={"text"}, retrievalConfiguration={"vectorSearchConfiguration": {"numberOfResults", "filter"}})
  bedrock-runtime.converse(modelId, messages=[{"role","content":[{"text"}]}], inferenceConfig={"maxTokens","temperature","topP"})
  bedrock-runtime.invoke_model(modelId="amazon.titan-embed-text-v2:0", body=json.dumps({"inputText": text})) -> {"embedding": [...]}
boto3 is imported lazily so the notebooks never require it.
"""
import json
import os
import numpy as np
from .dense import Embedder, _unit
from .generate import LLM

_CFG = {
    "provider": os.environ.get("RAGKIT_PROVIDER", "mock"),
    "region": os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1")),
    "kb_id": os.environ.get("RAGKIT_BEDROCK_KB_ID", ""),
    "llm_id": os.environ.get("RAGKIT_BEDROCK_LLM", "amazon.nova-lite-v1:0"),
    "embed_id": os.environ.get("RAGKIT_BEDROCK_EMBED", "amazon.titan-embed-text-v2:0"),
}


def configure(**kw):
    """configure(provider="bedrock", region="eu-west-1", kb_id="ABC123XYZ")"""
    _CFG.update({k: v for k, v in kw.items() if k in _CFG})
    return dict(_CFG)


def config() -> dict:
    return dict(_CFG)


def _boto(service: str):
    try:
        import boto3
    except ImportError as e:
        raise RuntimeError("boto3 is not installed. Run: pip install boto3") from e
    return boto3.client(service, region_name=_CFG["region"])


class BedrockEmbedder(Embedder):
    name = "bedrock-titan-v2"

    def __init__(self, model_id: str = None):
        self.model_id = model_id or _CFG["embed_id"]
        self.rt = _boto("bedrock-runtime")

    def fit(self, texts):            # a hosted model has nothing to fit
        return self

    def embed(self, texts: list) -> np.ndarray:
        out = []
        for t in texts:
            r = self.rt.invoke_model(modelId=self.model_id, body=json.dumps({"inputText": t}))
            out.append(json.loads(r["body"].read())["embedding"])
        return _unit(np.asarray(out, dtype=np.float32))


class BedrockLLM(LLM):
    name = "bedrock-converse"

    def __init__(self, model_id: str = None, max_tokens: int = 512, temperature: float = 0.0):
        self.model_id = model_id or _CFG["llm_id"]
        self.max_tokens, self.temperature = max_tokens, temperature
        self.rt = _boto("bedrock-runtime")
        self.last_usage = {}

    def generate(self, prompt: str, **kw) -> str:
        r = self.rt.converse(modelId=self.model_id,
                             messages=[{"role": "user", "content": [{"text": prompt}]}],
                             inferenceConfig={"maxTokens": kw.get("max_tokens", self.max_tokens),
                                              "temperature": kw.get("temperature", self.temperature), "topP": 0.9})
        self.last_usage = r.get("usage", {})
        return r["output"]["message"]["content"][0]["text"]


class BedrockKB:
    """A Bedrock Knowledge Base as a drop-in retriever: search(query, k) -> [(id, score)] with texts."""
    name = "bedrock-kb"

    def __init__(self, kb_id: str = None):
        self.kb_id = kb_id or _CFG["kb_id"]
        assert self.kb_id, "set RAGKIT_BEDROCK_KB_ID or pass kb_id"
        self.rt = _boto("bedrock-agent-runtime")
        self.chunks = {}

    def search(self, query: str, k: int = 10, mode: str = "kb", metadata_filter: dict = None, **_) -> list:
        cfg = {"vectorSearchConfiguration": {"numberOfResults": k}}
        if metadata_filter:
            cfg["vectorSearchConfiguration"]["filter"] = metadata_filter
        r = self.rt.retrieve(knowledgeBaseId=self.kb_id, retrievalQuery={"text": query}, retrievalConfiguration=cfg)
        out = []
        for i, res in enumerate(r.get("retrievalResults", [])):
            loc = res.get("location", {})
            uri = loc.get("s3Location", {}).get("uri", "") or loc.get("webLocation", {}).get("url", "")
            cid = f"kb:{i}:{abs(hash(uri + res['content']['text'][:40])) % 10**8:08x}"
            self.chunks[cid] = {"text": res["content"]["text"], "uri": uri}
            out.append((cid, float(res.get("score", 0.0))))
        return out

    def text(self, cid: str) -> str:
        return self.chunks[cid]["text"]


class BedrockReranker:
    """Bedrock's native rerank endpoint as a callable(query, ranked) -> ranked.

    Verified 2026-08-31: bedrock-agent-runtime.rerank(queries=[{"type":"TEXT","textQuery":{"text"}}],
    sources=[{"type":"INLINE","inlineDocumentSource":{"type":"TEXT","textDocument":{"text"}}}],
    rerankingConfiguration={"type":"BEDROCK_RERANKING_MODEL","bedrockRerankingConfiguration":{"modelConfiguration":{"modelArn"},"numberOfResults"}})
    -> results[{index, relevanceScore}]. Model ids seen in the docs: cohere.rerank-v3-5:0, amazon.rerank-v1:0.
    """
    name = "bedrock-rerank"

    def __init__(self, model_id: str = "cohere.rerank-v3-5:0"):
        self.model_arn = f"arn:aws:bedrock:{_CFG['region']}::foundation-model/{model_id}"
        self.rt = _boto("bedrock-agent-runtime")

    def bind(self, texts: dict):
        self.texts = texts
        return self

    def __call__(self, query: str, ranked: list, texts: dict = None, top: int = None) -> list:
        texts = texts or self.texts
        pool = ranked[:top] if top else ranked
        r = self.rt.rerank(queries=[{"type": "TEXT", "textQuery": {"text": query}}],
                           sources=[{"type": "INLINE", "inlineDocumentSource": {"type": "TEXT", "textDocument": {"text": texts[cid]}}} for cid, _ in pool],
                           rerankingConfiguration={"type": "BEDROCK_RERANKING_MODEL", "bedrockRerankingConfiguration": {"modelConfiguration": {"modelArn": self.model_arn}, "numberOfResults": len(pool)}})
        rescored = [(pool[res["index"]][0], float(res["relevanceScore"])) for res in r["results"]]
        return rescored + ranked[len(pool):]


def get_embedder(corpus_texts: list = None):
    """The embedder for the configured provider. LSA needs corpus_texts to fit."""
    if _CFG["provider"] == "bedrock":
        return BedrockEmbedder()
    from .dense import LSAEmbedder
    return LSAEmbedder().fit(corpus_texts or [])


def get_llm(**kw):
    if _CFG["provider"] == "bedrock":
        return BedrockLLM(**kw)
    from .generate import MockGenerator
    return MockGenerator(**kw)


def get_kb():
    """A Bedrock Knowledge Base retriever, or None when not configured."""
    if _CFG["provider"] == "bedrock" and _CFG["kb_id"]:
        return BedrockKB()
    return None


# Test inputs and expected outcomes
# config()["provider"]                                    -> "mock" with no env set
# configure(provider="bedrock", kb_id="X")["kb_id"]       -> "X"
# get_llm().name                                          -> "mock" (provider mock) or "bedrock-converse"
# get_kb()                                                -> None unless provider=bedrock and kb_id set
