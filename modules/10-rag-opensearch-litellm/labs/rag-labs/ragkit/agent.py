"""Agentic search: decompose, select a tool, retrieve, check sufficiency, stop, answer. Every stop condition is a config value.

Offline, the plan comes from the benchmark record (the plan a planner model would produce) and the
sufficiency check is a heuristic with a stated rule. With a provider configured, both are model calls.
The loop mechanics, the bridge-entity carry, the working-evidence guard, the stop conditions and the
trace metrics are real code and run the same way in both modes.
"""
import re
import time
from dataclasses import dataclass, field
import numpy as np
from .lexical import tokenize
from .context import pack, count_tokens
from .chunking import gold_chunk_sets
from .evals import coverage, correctness

COMPANY_SUFFIX = {"Dynamics", "Automation", "Bio", "Systems", "Networks", "Foods", "Energy", "Robotics", "Aerospace", "Diagnostics", "Pharma", "Ventures", "Spectrum", "Courier", "Wire"}
STOP_START = {"The", "Shares", "Chief", "Before", "Version", "Known", "Nasdaq", "European", "Venture", "Markets", "Interim", "Bankers", "Late", "Thursday", "Wednesday", "Tuesday", "Series", "Profile", "Nordic", "Turin", "Oslo", "Bergen", "Gdansk", "Eindhoven", "Germany", "Poland", "New", "York", "Stock", "Exchange", "United", "States"}


@dataclass
class AgentConfig:
    max_turns: int = 6
    token_budget: int = 6000        # cumulative evidence tokens across the whole trace
    deadline_ms: float = 4000.0     # simulated wall clock: retrieval measured, generation illustrative
    per_hop_k: int = 5
    n_pool: int = 30
    working_cap: int = 12           # guard against evidence bloat
    repeat_detector: bool = True
    no_new_info_stop: bool = True
    plateau_stop: bool = True
    refine_once: bool = True        # one refinement turn when the sufficiency check fails
    expand_neighbours: bool = False # parent-document retrieval: read the sibling chunks of each hop's best hits
    expand_top: int = 2             # how many top hits' documents to expand
    ms_per_turn: float = 350.0      # illustrative floor per retrieval turn (embed, retrieve, fuse, read), from the latency budget
    ms_generation: float = 1550.0   # illustrative, from the latency budget
    ms_sufficiency: float = 250.0   # illustrative: a small strict-schema model call


@dataclass
class Trace:
    qid: str
    question: str
    turns: list = field(default_factory=list)
    working: list = field(default_factory=list)     # chunk ids in arrival order, never overwritten
    dropped: list = field(default_factory=list)     # evidence-bloat drops
    packed: list = field(default_factory=list)
    answer: str = ""
    stop_reason: str = ""
    sufficient: bool = False
    evidence_tokens: int = 0
    simulated_ms: float = 0.0
    generations: int = 0
    scores: dict = field(default_factory=dict)
    hop_of: dict = field(default_factory=dict)      # chunk id -> hop that first added it


def entities(text: str) -> dict:
    """Capitalised runs, sorted into person-like and company-like. Deliberately simple and transparent."""
    out = {"person": [], "company": []}
    for m in re.finditer(r"\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)\b", text):
        words = m.group(1).split()
        if words[0] in STOP_START:
            words = words[1:]
        if len(words) < 2:
            continue
        name = " ".join(words[:2]) if words[-1] not in COMPANY_SUFFIX else " ".join(words)
        kind = "company" if words[-1] in COMPANY_SUFFIX or words[1] in COMPANY_SUFFIX else "person"
        if kind == "company":
            name = " ".join(w for w in words)
            for i, w in enumerate(words):
                if w in COMPANY_SUFFIX:
                    name = " ".join(words[max(0, i - 1):i + 1]); break
        out[kind].append(name)
    return out


def carry_bridge(top_texts: list, question_text: str, kind: str) -> str:
    """The entity to carry into the next hop: most frequent candidate across the top chunks, absent from the question."""
    counts = {}
    for rank, t in enumerate(top_texts):
        for name in entities(t)[kind]:
            if name.lower() in question_text.lower():
                continue
            counts[name] = counts.get(name, 0) + (1.0 - 0.05 * rank)
    return max(counts.items(), key=lambda x: x[1])[0] if counts else ""


def select_tool(query: str) -> str:
    """Lexical for identifiers and exact names, dense for meaning-only, hybrid otherwise."""
    if re.search(r"\b[A-Z]{2,}-?\d+\b|\b\d{3,}-\d+\b", query):
        return "lexical"
    proper = sum(1 for w in query.split()[1:] if w[:1].isupper())
    if proper == 0:
        return "dense"
    return "hybrid" if len(tokenize(query, keep_stop=True)) >= 6 else "lexical"


def _answer_type_present(hop_text: str, chunk_text: str) -> bool:
    h = hop_text.lower()
    if "when" in h or "what year" in h or "in what year" in h:
        return bool(re.search(r"\b(19|20)\d\d\b", chunk_text))
    if "how much" in h or "revenue" in h:
        return bool(re.search(r"\d+(\.\d+)? (million|billion)", chunk_text))
    return True


def sufficiency_check(hops: list, working: list, texts: dict, llm=None) -> tuple:
    """Does the working evidence answer every hop? Offline: a stated heuristic. With a provider: a strict-schema model call.

    Heuristic rule: a hop is supported when some chunk carries at least half of the hop's content terms
    and the answer type the hop asks for (a year for when, a sum for how much).
    """
    if llm is not None and getattr(llm, "name", "") != "mock":
        prompt = ("Working evidence:\n" + "\n".join(f"[{c}] {texts[c]}" for c in working) +
                  "\n\nSub-questions:\n" + "\n".join(f"{i}. {h}" for i, h in enumerate(hops)) +
                  "\n\nFor each sub-question reply on its own line with its number and either SUPPORTED <chunk id> or UNSUPPORTED. Nothing else.")
        out = llm.generate(prompt, max_tokens=200)
        per_hop = ["SUPPORTED" in line for line in out.splitlines() if line.strip()[:1].isdigit()]
        return all(per_hop) and len(per_hop) == len(hops), per_hop
    per_hop = []
    for h in hops:
        terms = set(tokenize(h))
        ok = False
        for c in working:
            ct = set(tokenize(texts[c]))
            if terms and len(terms & ct) / len(terms) >= 0.5 and _answer_type_present(h, texts[c]):
                ok = True; break
        per_hop.append(ok)
    return all(per_hop), per_hop


def run_agent(question, retriever, texts: dict, generator, cfg: AgentConfig = None, plan: list = None, llm=None) -> Trace:
    cfg = cfg or AgentConfig()
    plan = plan if plan is not None else (question.plan or [{"text": question.text, "depends_on": None, "bridge_kind": "", "tool": "hybrid"}])
    tr = Trace(question.qid, question.text)
    seen_queries, filled = set(), {}
    scores = {}
    t_wall = time.perf_counter()

    by_doc = {}
    for c in retriever.chunks.values():
        by_doc.setdefault(c.doc_id, []).append(c.chunk_id)

    def add_evidence(pool, hop_i):
        top = list(pool[:cfg.per_hop_k])
        if cfg.expand_neighbours and pool:
            expanded = 0
            for hit, s in pool[:cfg.per_hop_k * 2]:
                doc = retriever.chunks[hit].doc_id
                if all(cid in tr.working for cid in by_doc.get(doc, [])):
                    continue                                   # already read this document in full
                top += [(cid, s * 0.9) for cid in by_doc.get(doc, []) if cid not in {c for c, _ in top}]
                expanded += 1
                if expanded >= cfg.expand_top:
                    break
        new = [(cid, s) for cid, s in top if cid not in tr.working]
        for cid, s in new:
            tr.working.append(cid); scores[cid] = max(scores.get(cid, 0.0), s + 1.0 / (hop_i + 1)); tr.hop_of.setdefault(cid, hop_i)
            tr.evidence_tokens += count_tokens(texts[cid])
        while len(tr.working) > cfg.working_cap:      # evidence bloat guard: drop the lowest-scoring chunk
            victim = min(tr.working, key=lambda c: scores[c]); tr.working.remove(victim); tr.dropped.append(victim)
        return [cid for cid, _ in new]

    order = [i for i, h in enumerate(plan) if h["depends_on"] is None] + [i for i, h in enumerate(plan) if h["depends_on"] is not None]
    for hop_i in order:
        if len(tr.turns) >= cfg.max_turns:
            tr.stop_reason = "turn cap"; break
        h = plan[hop_i]; text = h["text"]
        if h["depends_on"] is not None:
            dep_ids = tr.turns[h["depends_on"]]["top"] if h["depends_on"] < len(tr.turns) else []
            bridge = carry_bridge([texts[c] for c in dep_ids[:3]], question.text, h.get("bridge_kind") or "person")
            if not bridge:
                tr.stop_reason = "no bridge entity found for a dependent hop"; break
            text = text.replace("{bridge}", bridge); filled[hop_i] = bridge
        norm = " ".join(tokenize(text))
        if cfg.repeat_detector and norm in seen_queries:
            tr.stop_reason = "repeat detector"; break
        seen_queries.add(norm)
        tool = select_tool(text)
        t0 = time.perf_counter(); pool = retriever.search(text, k=cfg.n_pool, mode=tool); ms = (time.perf_counter() - t0) * 1000
        new_ids = add_evidence(pool, hop_i)
        tr.simulated_ms += ms + cfg.ms_per_turn
        tr.turns.append({"turn": len(tr.turns) + 1, "hop": hop_i, "query": text, "tool": tool, "expected_tool": h.get("tool", "hybrid"), "top": [c for c, _ in pool[:cfg.per_hop_k]],
                         "new_evidence": new_ids, "working_size": len(tr.working), "evidence_tokens": tr.evidence_tokens, "retrieval_ms": round(ms, 2), "bridge": filled.get(hop_i, "")})
        if cfg.no_new_info_stop and not new_ids:
            tr.stop_reason = "no new information"; break
        if tr.evidence_tokens > cfg.token_budget:
            tr.stop_reason = "token budget"; break
        if tr.simulated_ms + cfg.ms_generation > cfg.deadline_ms:
            tr.stop_reason = "wall-clock deadline"; break

    hop_texts = [plan[i]["text"].replace("{bridge}", filled.get(i, "")) for i in range(len(plan))]
    tr.sufficient, per_hop = sufficiency_check(hop_texts, tr.working, texts, llm); tr.simulated_ms += cfg.ms_sufficiency
    if not tr.sufficient and cfg.refine_once and not tr.stop_reason and len(tr.turns) < cfg.max_turns:
        weak = per_hop.index(False); text = hop_texts[weak]
        tool = "lexical" if select_tool(text) != "lexical" else "dense"
        t0 = time.perf_counter(); pool = retriever.search(text, k=cfg.n_pool, mode=tool); ms = (time.perf_counter() - t0) * 1000
        new_ids = add_evidence(pool, weak); tr.simulated_ms += ms + cfg.ms_per_turn
        tr.turns.append({"turn": len(tr.turns) + 1, "hop": weak, "query": text, "tool": tool, "expected_tool": plan[weak].get("tool", "hybrid"), "top": [c for c, _ in pool[:cfg.per_hop_k]],
                         "new_evidence": new_ids, "working_size": len(tr.working), "evidence_tokens": tr.evidence_tokens, "retrieval_ms": round(ms, 2), "bridge": filled.get(weak, ""), "refinement": True})
        tr.sufficient, per_hop = sufficiency_check(hop_texts, tr.working, texts, llm); tr.simulated_ms += cfg.ms_sufficiency
        if not tr.sufficient:
            tr.stop_reason = "confidence plateau after refinement"
    if not tr.stop_reason:
        tr.stop_reason = "sufficiency satisfied" if tr.sufficient else "plan exhausted without sufficiency"
    ranked = sorted(tr.working, key=lambda c: -scores[c])
    packed = pack([(c, scores[c]) for c in ranked], texts, evidence_cap=cfg.token_budget, k=cfg.working_cap)
    tr.packed = packed.chunk_ids; tr.scores = dict(scores)
    tr.answer = generator.answer(question, tr.packed, texts).text
    tr.generations = 1; tr.simulated_ms += cfg.ms_generation
    return tr


def trace_metrics(tr: Trace, question, chunks: list) -> dict:
    gs = gold_chunk_sets(question, chunks)
    if not gs:
        return {"qid": tr.qid, "turns": len(tr.turns), "stop": tr.stop_reason, "decomposition coverage": float("nan"), "tool accuracy": np.mean([t["tool"] == t["expected_tool"] for t in tr.turns]) if tr.turns else float("nan"),
                "turn efficiency": len(tr.turns) / max(1, len(question.plan)), "cumulative recall": float("nan"), "evidence retention": float("nan"), "stop quality": float(tr.sufficient == False)}
    pooled = set().union(*[set(t["top"]) for t in tr.turns]) if tr.turns else set()
    found_in_working = set(tr.working) | set(tr.dropped)
    gold_found = [s for s in gs if s & found_in_working]
    retained = [s for s in gold_found if s & set(tr.packed)]
    cov = coverage(gs, tr.packed)
    return {"qid": tr.qid, "turns": len(tr.turns), "stop": tr.stop_reason,
            "decomposition coverage": sum(1 for s in gs if s & pooled) / len(gs),
            "tool accuracy": float(np.mean([t["tool"] == t["expected_tool"] for t in tr.turns])) if tr.turns else float("nan"),
            "turn efficiency": len(tr.turns) / max(1, len(question.plan)),
            "cumulative recall": len(gold_found) / len(gs),
            "evidence retention": (len(retained) / len(gold_found)) if gold_found else float("nan"),
            "stop quality": float(tr.sufficient == (cov >= 1.0))}


def decompose_pool(question, retriever, texts: dict, cfg: AgentConfig = None, only_types=("inference",)) -> list:
    """RunConfig.decompose hook: the loop's working evidence as a ranked pool, for the question types named."""
    if question.qtype not in only_types:
        return retriever.search(question.text, k=(cfg or AgentConfig()).n_pool, mode="hybrid")
    class _NoGen:
        def answer(self, q, ids, t):
            from .generate import Answer
            return Answer("", [], True)
    tr = run_agent(question, retriever, texts, _NoGen(), cfg or AgentConfig())
    # interleave by hop so that each hop's best evidence makes a small k: best of hop 0, best of hop 1, second of hop 0, ...
    by_hop = {}
    for c in tr.working:
        by_hop.setdefault(tr.hop_of.get(c, 0), []).append((c, tr.scores[c]))
    for h in by_hop:
        by_hop[h].sort(key=lambda x: -x[1])
    out, i = [], 0
    while any(by_hop.values()):
        for h in sorted(by_hop):
            if by_hop[h]:
                c, s = by_hop[h].pop(0); out.append((c, 1.0 / (len(out) + 1)))
    return out


# Test inputs and expected outcomes
# entities("Nord Aerospace named Elena Ruiz as chief executive. Ruiz joins from Vega Dynamics")  -> person ["Elena Ruiz"], company ["Nord Aerospace", "Vega Dynamics"]
# select_tool("ERR-4471")  -> "lexical" ; select_tool("who now runs the launch company")  -> "dense"
# tr = run_agent(ANCHOR, retriever, texts, MockGenerator()); tr.turns[1]["bridge"]  -> "Elena Ruiz"; tr.answer startswith "Vega Dynamics, 2023"
# trace_metrics(tr, ANCHOR, chunks)["cumulative recall"]  -> 1.0
