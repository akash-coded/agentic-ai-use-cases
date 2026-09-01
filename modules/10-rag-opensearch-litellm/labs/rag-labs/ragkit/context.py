"""Context design: count tokens, allocate a budget with hard caps, pack whole chunks, order them.

Token counting uses tiktoken's cl100k_base when it is installed and a words-times-1.3
heuristic otherwise. The heuristic is marked in every printout so nobody mistakes it
for a model's real tokenizer.
"""
from dataclasses import dataclass, field

try:
    import tiktoken
    _ENC = tiktoken.get_encoding("cl100k_base")
    TOKENIZER = "tiktoken cl100k_base"
except Exception:                       # tiktoken missing or no cached encoding
    _ENC = None
    TOKENIZER = "heuristic (words x 1.3)"


def count_tokens(text: str) -> int:
    if _ENC is not None:
        return len(_ENC.encode(text))
    return int(len(text.split()) * 1.3 + 0.5)


@dataclass
class Budget:
    """Hard caps per slice of the working context, in tokens."""
    system: int = 2200
    tools: int = 1600
    query: int = 1000
    evidence: int = 18000
    output: int = 4500
    headroom: int = 4700

    @property
    def total(self) -> int:
        return self.system + self.tools + self.query + self.evidence + self.output + self.headroom

    def table(self):
        import pandas as pd
        rows = [("System instructions and output contract", self.system, "Nothing, but every edit invalidates the prompt cache after it."),
                ("Tool and schema definitions", self.tools, "Tool selection degrades before the token limit does."),
                ("User query and conversation state", self.query, "Summarise older turns, never drop the current question."),
                ("Retrieved evidence, k chunks", self.evidence, "Drop whole chunks by rank, never truncate one mid-way."),
                ("Output reserve", self.output, "The answer is cut off mid-sentence."),
                ("Headroom", self.headroom, "Absorbs tokenizer variance and a long retry.")]
        return pd.DataFrame(rows, columns=["slice", "cap_tokens", "what happens when it overflows"])


@dataclass
class Packed:
    chunk_ids: list
    texts: list
    tokens: int
    dropped: list = field(default_factory=list)
    order: str = "rank"


def order_ends_first(ranked: list) -> list:
    """Place the strongest items at the start and the end, weakest in the middle.

    Rank 1 goes first, rank 2 last, rank 3 second, rank 4 second-to-last, and so on.
    This is the practical response to the lost-in-the-middle effect.
    """
    front, back = [], []
    for i, item in enumerate(ranked):
        (front if i % 2 == 0 else back).append(item)
    return front + back[::-1]


def pack(ranked: list, texts: dict, evidence_cap: int, k: int = None, order: str = "rank", dedup_jaccard: float = None) -> Packed:
    """Pack whole chunks by rank until the evidence cap would be exceeded.

    ranked: [(chunk_id, score)] best first. k caps the count; evidence_cap caps tokens.
    A chunk that does not fit is dropped whole, and packing continues with the next one
    only if `order` is 'rank' (so a small chunk can still fit); it never truncates.
    """
    from .fusion import dedup as _dedup
    if dedup_jaccard is not None:
        ranked = _dedup(ranked, texts, jaccard=dedup_jaccard)
    chosen, dropped, used = [], [], 0
    for cid, _ in ranked:
        if k is not None and len(chosen) >= k:
            dropped.append((cid, "over k"))
            continue
        t = count_tokens(texts[cid])
        if used + t > evidence_cap:
            dropped.append((cid, "over token cap"))
            continue
        chosen.append(cid)
        used += t
    if order == "ends":
        chosen = [cid for cid, _ in order_ends_first([(c, 0) for c in chosen])]
    return Packed(chosen, [texts[c] for c in chosen], used, dropped, order)


SYSTEM_CONTRACT = (
    "You answer only from the evidence blocks. Every factual claim must cite the block id in square brackets, "
    "for example [a1:0:1f2e]. If the evidence does not contain the facts needed, reply exactly: "
    "INSUFFICIENT EVIDENCE, followed by which fact is missing. If two blocks conflict, say so and cite both."
)


def skeleton(question: str, packed: Packed, meta: dict, system: str = SYSTEM_CONTRACT) -> str:
    """The prompt as a fixed skeleton: system, query, delimited evidence with provenance, then the contract reminder."""
    blocks = []
    for cid, text in zip(packed.chunk_ids, packed.texts):
        m = meta.get(cid, {})
        blocks.append(f"<evidence id=\"{cid}\" source=\"{m.get('source','')}\" date=\"{m.get('date','')}\">\n{text}\n</evidence>")
    return (f"<system>\n{system}\n</system>\n\n<question>\n{question}\n</question>\n\n" + "\n\n".join(blocks) +
            "\n\n<format>Answer in one or two sentences with citations, or reply INSUFFICIENT EVIDENCE.</format>")


# Test inputs and expected outcomes
# count_tokens("hello world")                        -> 2 with tiktoken, 3 with the heuristic
# Budget().total                                     -> 32000
# order_ends_first([1,2,3,4,5])                      -> [1,3,5,4,2]
# pack([("a",1),("b",1)], {"a":"x "*10,"b":"y "*400}, evidence_cap=50).dropped  -> [("b","over token cap")]
