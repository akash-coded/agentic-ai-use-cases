from nbtools import md, code, fig, deck, header, recap, write, SETUP

C = []
C += header(8, "Agentic search and the end-to-end build: the AGENT layer and the FDE Lab",
            "You run the search loop on the worked question, watch it stop early with full confidence, fix that with a technique rather than a prompt, score the trace instead of the answer, measure when the loop earns its cost, then execute the FDE Lab brief end to end and write the decision record from the numbers.",
            deck("spine_agent", "The evidence pipeline with the AGENT layer lit", "The loop wraps FIND and JUDGE and multiplies their cost by the number of turns."),
            "Offline, the plan comes from the benchmark record and the sufficiency check is a stated heuristic; with a provider configured both are model calls. Everything else in the loop is real code and runs the same way in both modes.",
            "Notebook 07.", "The FDE Lab build, which this notebook is the brief for.")

# ---------------------------------------------------------------- 1 decompose
C += [md(f"""
## 1 · Decompose, and carry the bridge entity forward

{deck("agenticLoop", "Decompose, select a tool, retrieve, check sufficiency, loop or answer", "From the session deck. Each box below becomes a function.")}

{fig([("q","The worked question","start"),("h1","Hop 1: who became chief\\nexecutive of Nord Aerospace\\nin 2026","proc"),("br","Bridge entity from\\nhop 1 evidence","tool"),("h2","Hop 2: which company did\\n{{bridge}} take public,\\nand in what year","proc"),("ans","Answer from both hops","end")],
      [("q","h1"),("h1","br"),("br","h2"),("h2","ans")], caption="The plan for the worked question. Offline it comes from the benchmark record, which is the plan a planner model would produce; the bridge is extracted by code from hop-one evidence.")}
"""),
      code(SETUP),
      code('''
store, chunks, embedder, retriever, generator, questions = rk.bootstrap(chunker="structural")
texts = {c.chunk_id: c.text for c in chunks}; anchor = rk.ANCHOR; answerable = [q for q in questions if q.gold]
display(table(pd.DataFrame(anchor.plan), "The plan for the worked question"))
hop1 = anchor.plan[0]["text"]
top = [cid for cid, _ in retriever.hybrid(hop1, k=5)]
print("hop-one top chunks:", top)
for cid in top[:3]:
    print(f"  entities in {cid}: {rk.entities(texts[cid])}")
bridge = rk.carry_bridge([texts[c] for c in top[:3]], anchor.text, "person")
print("\\nbridge carried into hop two:", bridge, "->", anchor.plan[1]["text"].replace("{bridge}", bridge))
'''),
      md("""
| What goes wrong in a loop | The guard, as a config value in `AgentConfig` |
|---|---|
| Query drift: by turn four the agent searches for something adjacent to the question. | Every hop is written against the original question; the bridge is substituted into a fixed template, not into a rewritten question. |
| Evidence bloat: working evidence grows past the budget and the earliest, often best, results get dropped. | `working_cap` and `token_budget`; drops are recorded so evidence retention can be scored. |
| Tool thrash: the same query re-issued to three tools because none returned a confident result. | `repeat_detector` on the normalised query, and one refinement turn at most. |
| Premature confidence: the sufficiency check passes on partial evidence. | The check is a separate call with a strict schema; section 3 shows it failing anyway and what fixes it. |
| Cost blowout: nothing bounds the loop. | `max_turns`, `token_budget`, `deadline_ms`; a budget stop must produce a partial answer with a stated gap. |
""")]

# ---------------------------------------------------------------- 2 tool selection
C += [md("""
## 2 · Select a tool per hop

Lexical for identifiers and exact names, dense for meaning, grep for repositories, SQL for aggregates, a live API for what the index cannot hold. The cell runs the selector over the sub-queries of the benchmark and scores it against the tool an expert would have picked.
"""),
      code('''
rows = []
for q in questions:
    for h in q.plan:
        text = h["text"].replace("{bridge}", "Elena Ruiz" if q.qid == "q01" else "Brisk Automation" if q.qid == "q02" else "Amir Sadeghi")
        rows.append({"qid": q.qid, "sub-query": text[:60], "selected": rk.select_tool(text), "expert's pick": h["tool"], "match": rk.select_tool(text) == h["tool"]})
sel = pd.DataFrame(rows)
print(f"tool selection accuracy against the expert's pick: {sel['match'].mean():.2f}")
table(sel[~sel["match"]].assign(match="no"), "Where the selector and the expert disagree")
'''),
      md("""
| Tool | Pick it when | Notebook that showed why |
|---|---|---|
| Lexical | The hop hinges on an exact name, code or identifier. | 01 and 04. |
| Dense | The hop is a paraphrase with no shared tokens. | 01. |
| Hybrid, fused | Both signals are present, which is the default for natural sub-questions. | 04. |
| Grep | The source is a repository or a log directory, not an index. | 04. |
| SQL or a live API | The answer is an aggregate or a value the index cannot hold. | Not modelled here; the interface is the same callable. |
""")]

# ---------------------------------------------------------------- 3 the loop on the anchor
C += [md(f"""
## 3 · The loop on the worked question: stopping early with full confidence

{deck("agenticTrace", "Turn one finds the appointment, turn two carries the name and finds the IPO", "From the session deck. The first run below does not get there, and the trace shows why.")}
"""),
      code('''
naive = rk.run_agent(anchor, retriever, texts, generator, rk.AgentConfig())
def show_trace(tr):
    rows = [{"turn": t["turn"], "tool": t["tool"], "query": t["query"][:58], "bridge": t["bridge"], "new evidence": ", ".join(t["new_evidence"][:3]) + ("..." if len(t["new_evidence"]) > 3 else ""), "working": t["working_size"], "tokens": t["evidence_tokens"]} for t in tr.turns]
    display(table(pd.DataFrame(rows), f"stop: {tr.stop_reason} | sufficiency check: {tr.sufficient} | simulated {tr.simulated_ms:.0f} ms"))
    print("answer:", tr.answer)
show_trace(naive)
gs = rk.gold_chunk_sets(anchor, chunks)
print("coverage of the gold spans in the packed context:", rk.coverage(gs, naive.packed), "| the check said sufficient:", naive.sufficient)
'''),
      md("""
The check passed because the hop-two chunk it found mentions Ruiz taking the company public and carries a year, 2020. The fact the question needs, the IPO date, sits in the sibling chunk that never entered the pool. This is premature confidence, and it is not fixed by a better prompt. It is fixed by reading the neighbours of a hit, which is parent-document retrieval, an established technique: retrieve by chunk, read by document.
"""),
      code('''
fixed = rk.run_agent(anchor, retriever, texts, generator, rk.AgentConfig(expand_neighbours=True))
show_trace(fixed)
print("coverage now:", rk.coverage(gs, fixed.packed))
'''),
      md("""
| Trace field | Why it is recorded |
|---|---|
| Per turn: query, tool, top ids, new evidence ids, working size, tokens, bridge | Q2 of the fault tree per hop, tool-selection scoring, and the query-drift check. |
| Working evidence in arrival order, never overwritten, plus the drops | Evidence retention: found it, then threw it away. |
| The sufficiency verdict and the stop reason | Stop-decision quality, and the audit line the UI usually shows. |
| Packed ids and the answer with citations | Faithfulness scoring and replay under a different model. |
| Simulated milliseconds and the generation count | The cost multiplier the next section measures. |
""")]

# ---------------------------------------------------------------- 4 stop conditions
C += [md(f"""
## 4 · Stop conditions are config, and a budget stop must still answer honestly

{fig([("ok","STOP BECAUSE YOU SUCCEEDED","start"),("s1","Sufficiency satisfied:\\nevery hop supported","ok"),("s2","No new information\\nin the last turn","ok"),("s3","Confidence plateau after\\none refinement","ok"),("out","STOP BECAUSE YOU RAN OUT","start"),("b1","Turn cap","cost"),("b2","Token budget across\\nthe whole trace","cost"),("b3","Wall-clock deadline","cost"),("b4","Repeat detector","cost"),("part","Explicit partial answer\\nwith a stated gap","end")],
      [("ok","s1"),("ok","s2"),("ok","s3"),("out","b1"),("out","b2"),("out","b3"),("out","b4"),("b1","part"),("b2","part"),("b3","part"),("b4","part")], rankdir="LR", caption="From the advanced-track deck. Every box is a field of AgentConfig.")}
"""),
      code('''
configs = {
    "default, neighbours": rk.AgentConfig(expand_neighbours=True),
    "turn cap 1": rk.AgentConfig(expand_neighbours=True, max_turns=1),
    "token budget 150": rk.AgentConfig(expand_neighbours=True, token_budget=150),
    "deadline 2,000 ms": rk.AgentConfig(expand_neighbours=True, deadline_ms=2000),
    "no refinement": rk.AgentConfig(expand_neighbours=True, refine_once=False),
}
rows = []
for name, cfg in configs.items():
    tr = rk.run_agent(anchor, retriever, texts, generator, cfg)
    rows.append({"config": name, "turns": len(tr.turns), "stop reason": tr.stop_reason, "simulated ms": round(tr.simulated_ms), "answer": tr.answer[:75] + ("..." if len(tr.answer) > 75 else "")})
table(pd.DataFrame(rows), "The worked question under five stop configurations")
'''),
      md("""
| If the loop stopped because | Then the answer must be | Because |
|---|---|---|
| Sufficiency was satisfied. | A full answer with a citation per fact. | That is the only stop that licenses a confident synthesis. |
| A budget ran out (turns, tokens, deadline). | An explicit partial answer with the gap named, as the table shows: found A, could not confirm B. | A confident synthesis of half the evidence is the worst outcome a loop can produce. |
| The same query came back, or nothing new arrived. | The same partial answer, and the stop reason in the trace. | Tool thrash and no-progress loops are cost with no information. |

Every one of these is a config value with a default. Write them down before you write the loop.
""")]

# ---------------------------------------------------------------- 5 evaluate the trace
C += [md(f"""
## 5 · Evaluate the trace, not just the answer

{fig([("t","One trace","start"),("m1","Decomposition coverage:\\ndid the hops reach every\\ngold span?","proc"),("m2","Tool accuracy:\\nturns using the tool an\\nexpert would","proc"),("m3","Turn efficiency:\\nturns over minimum turns","proc"),("m4","Cumulative recall:\\ngold found anywhere\\nin the trace","proc"),("m5","Evidence retention:\\ngold found early that\\nsurvived to the context","cost"),("m6","Stop quality:\\nsufficiency verdict against\\nreal coverage","proc")],
      [("t","m1"),("t","m2"),("t","m3"),("t","m4"),("t","m5"),("t","m6")], caption="From the advanced-track deck. Answer-only scoring cannot tell a lucky agent from a good one.")}
"""),
      code('''
def trace_table(cfg, label):
    rows = []
    for q in questions:
        tr = rk.run_agent(q, retriever, texts, generator, cfg); m = rk.trace_metrics(tr, q, chunks); m["correct"] = rk.correctness(q, tr.answer); rows.append(m)
    df = pd.DataFrame(rows); s = df.drop(columns=["qid", "stop"]).mean(numeric_only=True).round(2); s.name = label
    return df, s
naive_df, naive_s = trace_table(rk.AgentConfig(), "naive loop")
nb_df, nb_s = trace_table(rk.AgentConfig(expand_neighbours=True), "loop with neighbour expansion")
cap_df, cap_s = trace_table(rk.AgentConfig(expand_neighbours=True, working_cap=4), "neighbours, working cap 4")
display(table(pd.DataFrame([naive_s, nb_s, cap_s]).reset_index().rename(columns={"index": "configuration"}), "Trace metrics averaged over the benchmark; null questions have no gold so their recall columns are excluded from the mean"))
table(nb_df[["qid", "turns", "stop", "decomposition coverage", "cumulative recall", "evidence retention", "stop quality", "correct"]], "Per question, neighbour expansion")
'''),
      md("""
| Trace property | A bad score means | What you saw |
|---|---|---|
| Decomposition coverage | The plan was wrong; no amount of retrieval will rescue it. | 0.89: the sub-questions alone reached both spans for every comparison and temporal question, and for the two dependent questions they reached the right document but not the gold chunk, which neighbour expansion then supplied (cumulative recall 1.0). |
| Tool selection accuracy | Tool descriptions are ambiguous, or there are too many tools. | One disagreement with the expert's pick on a null question. |
| Turn efficiency | Cost is being burned on redundant search. | 1.0: each hop took one turn. |
| Cumulative evidence recall | The loop never reached the second hop. | The naive loop missed a second-hop span on two questions; neighbour expansion found them all. |
| Evidence retention | You found it and then threw it away, the worst and most invisible failure. | With a working cap of four, retention fell: gold found in turn one was evicted by turn two. |
| Stop-decision quality | Premature confidence, or loops that never terminate. | The heuristic check called the null questions answerable because a chunk about some other firm's CFO exists. A strict-schema model call is the production fix; the metric is what catches it either way. |
""")]

# ---------------------------------------------------------------- 6 when the loop earns its cost
C += [md(f"""
## 6 · When the loop earns its cost

{deck("agenticVsSingle", "Single-shot, parallel and agentic: when each is the right tool", "From the session deck. The cell measures all three on the benchmark, then measures the escalation policy that runs single-shot by default.")}
"""),
      code('''
RATES = rk.Rates(); PREFIX_TOKENS = 3000; OUT_TOKENS = 150
def parallel_pool(q, r):
    seen, out = set(), []
    for h in (q.plan or [{"text": q.text}]):
        for cid, s in r.search(h["text"].replace("{bridge}", ""), k=5, mode="hybrid"):
            if cid not in seen: seen.add(cid); out.append((cid, s))
    return out
loop_cfg = rk.AgentConfig(expand_neighbours=True)
def loop_pool(q, r): return rk.decompose_pool(q, r, texts, loop_cfg, only_types=("inference", "comparison", "temporal", "null"))
K = 10
modes = {"single-shot, hybrid k=10": (rk.RunConfig("single", mode="hybrid", k=K), 1, 0),
         "parallel sub-queries, fused": (rk.RunConfig("parallel", mode="hybrid", k=K, decompose=parallel_pool), 1, 2),
         "agentic loop": (rk.RunConfig("loop", mode="hybrid", k=K, decompose=loop_pool), 1, 2)}
rows = []
for name, (cfg, gens, turns) in modes.items():
    df = rk.run_benchmark(cfg, retriever, generator, questions, chunks); s = rk.summarize(df)
    ms = 350 * max(1, turns) + (250 if turns else 0) + 1550 * gens
    dollars = np.mean([rk.query_cost(PREFIX_TOKENS, int(e), 30, OUT_TOKENS, RATES, cached=True)["total"] for e in df["evidence_tokens"]])
    rows.append({"mode": name, "full_chain@k": s["full_chain@k"], "correct": s["correct"], "evidence tokens": round(s["evidence_tokens"]), "simulated ms": ms, "dollars per query": round(dollars, 5)})
cmp = pd.DataFrame(rows)
display(table(cmp, "Three modes at k=10. Latency is measured retrieval plus the illustrative per-turn and generation figures from the latency budget", precision=5))
bars(list(cmp["mode"]), list(cmp["correct"]), "Correctness by mode", "correct", fmt="{:.2f}", figsize=(8, 3))
'''),
      code('''
# the escalation policy: single-shot first, escalate to the loop only when the sufficiency check on the single-shot context fails
escalated, rows = 0, []
for q in questions:
    pool = retriever.hybrid(q.text, k=50); packed = rk.pack(pool, texts, evidence_cap=6000, k=K)
    hops = [h["text"].replace("{bridge}", "") for h in (q.plan or [{"text": q.text}])]
    ok, _ = rk.sufficiency_check(hops, packed.chunk_ids, texts)
    if ok:
        ans = generator.answer(q, packed.chunk_ids, texts).text; ms = 350 + 250 + 1550; tokens = packed.tokens
    else:
        escalated += 1; tr = rk.run_agent(q, retriever, texts, generator, loop_cfg); ans = tr.answer; ms = 350 + 250 + tr.simulated_ms; tokens = tr.evidence_tokens
    rows.append({"qid": q.qid, "type": q.qtype, "escalated": not ok, "correct": rk.correctness(q, ans), "ms": round(ms), "tokens": tokens})
esc = pd.DataFrame(rows)
print(f"escalated {escalated} of {len(questions)} questions; correctness {esc['correct'].mean():.3f}; mean simulated latency {esc['ms'].mean():.0f} ms; mean evidence tokens {esc['tokens'].mean():.0f}")
table(esc, "Escalation per question")
'''),
      md("""
| Signal | Single-shot RAG | Agentic search | What this benchmark measured |
|---|---|---|---|
| Question shape | Answerable from evidence one query can surface. | Later hops depend on what earlier hops returned. | The two dependent inference questions are the only ones single-shot could not answer at k=10. |
| Latency | One retrieval and one generation, predictable. | Turns times the pre-generation cost, plus a sufficiency call; high variance. | About 2,500 ms against about 1,900 ms in the simulation. |
| Cost per query | One generation. | More calls, and on hard questions more evidence; the tail is what hurts. | Fewer evidence tokens in the loop at the same k here, since each hop's pool is small and k caps the pack; the cost is in the extra retrieval turn and the sufficiency call. |
| Failure mode | Missing evidence, one bad answer. | Compounding drift, premature confidence. | Stop quality caught the check passing on null questions. |
| What you evaluate | One retrieval and one answer. | The whole trace. | Section 5. |

The useful middle is the escalation policy: single-shot by default, and the loop only when the sufficiency check on the first pass fails. Most traffic pays single-shot cost; the hard questions get the budget they need. The cell above shows its dependency: the heuristic check passed the worked question's single-shot context, so nothing escalated and the question stayed wrong. An escalation policy is only as good as the sufficiency check that triggers it, and stop quality in section 5 is the metric that tells you whether the check can be trusted.
"""),
      code('''
LOOP_TREE = [
    {"q": "Do later hops depend on what earlier hops return?", "test": lambda f: f["dependent"], "yes": None, "no": "single-shot or parallel sub-queries; the loop buys nothing", "show": lambda f: f"dependent={f['dependent']}"},
    {"q": "Is there latency budget for at least two retrieval turns plus a sufficiency call?", "test": lambda f: f["latency_budget_ms"] >= 2 * 350 + 250 + 1550, "yes": None, "no": "single-shot with a wide k and a partial-answer contract", "show": lambda f: f"budget={f['latency_budget_ms']} ms"},
    {"q": "Does the cost ceiling absorb three to twenty times a single generation on hard questions?", "test": lambda f: f["cost_ceiling"] >= 3 * f["single_cost"], "yes": "escalate to the loop when the single-shot sufficiency check fails", "no": "single-shot, and route hard questions to a human or a queue", "show": lambda f: f"ceiling={f['cost_ceiling']}, single={f['single_cost']:.4f}"},
]
single_cost = float(cmp.loc[0, "dollars per query"])
display(table(decision(LOOP_TREE, {"dependent": True, "latency_budget_ms": 4000, "cost_ceiling": 0.03, "single_cost": single_cost}), "The worked question under the FDE Lab constraints"))
table(decision(LOOP_TREE, {"dependent": False, "latency_budget_ms": 1500, "cost_ceiling": 0.005, "single_cost": single_cost}), "A comparison question in a tight interactive product")
''')]

# ---------------------------------------------------------------- 7 end-to-end and bedrock
C += [md(f"""
## 7 · The whole system on one page, and the provider swap

{deck("endToEndHLD", "Index path, stores, query path, control plane", "The whiteboard to draw from memory. Everything above the query path is a batch job with a deploy step; everything on the query path has a p95; the control plane lets you change either without guessing.")}

With `RAGKIT_PROVIDER=bedrock` and `RAGKIT_BEDROCK_KB_ID` set, `rk.get_kb()` returns a Bedrock Knowledge Base as a retriever with the same `search(query, k)` shape, so the loop above runs against it unchanged. Verified 2026-08-31: `bedrock-agent-runtime.retrieve` with `knowledgeBaseId`, `retrievalQuery` and a `vectorSearchConfiguration` carrying `numberOfResults` and an optional metadata `filter`.
"""),
      code('''
kb = rk.get_kb()
if kb is None:
    print("provider is mock, or no knowledge base id is set. To run the loop against Bedrock:")
    print("  RAGKIT_PROVIDER=bedrock AWS_REGION=<region> RAGKIT_BEDROCK_KB_ID=<kb id>, then rerun this notebook.")
    print("  rk.get_llm() then returns a Converse-API model, rk.get_embedder() Titan V2, and rk.make_reranker('bedrock', ...) the rerank endpoint.")
else:
    hits = kb.search(anchor.text, k=5)
    display(table(pd.DataFrame([{"id": cid, "score": round(s, 3), "text": kb.text(cid)[:90]} for cid, s in hits]), "Bedrock Knowledge Base results for the worked question"))
''')]

# ---------------------------------------------------------------- 8 the FDE lab
C += [md(f"""
## 8 · The FDE Lab build brief, executed

{fig([("h","0 · Harness first: runner,\\nmetrics, results table","start"),("b","1 · Baseline: fixed chunking,\\ndense only, k=5, no reranker","proc"),("s2","2 · Change one thing:\\nadd BM25 and RRF","proc"),("s3","3 · Change one thing:\\nreranker over N=50","proc"),("s4","4 · Change one thing:\\ndecomposition for\\ninference questions only","proc"),("d","5 · Decision record:\\nshipped, rejected, the\\nnumber that decided it","end"),("c","Constraints: 6,000 evidence tokens,\\n4 s p95, 0.03 dollars per query,\\nnulls scored, citations resolve,\\nfrozen slice read once at the end","note")],
      [("h","b"),("b","s2"),("s2","s3"),("s3","s4"),("s4","d"),("c","b")], caption="The brief from the advanced-track deck. Each step below re-runs the same harness and records the delta and the cost delta.")}

| Constraint | Value | Why it is there |
|---|---|---|
| Evidence token cap | 6,000 | You cannot buy recall by packing more. |
| p95 latency ceiling | 4 seconds end to end | Retrieval is nearly free; generation and turns are not. |
| Cost ceiling | 0.03 dollars per answered query, measured | Measured from tokens at the stated rates, not estimated. |
| Null questions | Ten injected in the brief, three here; abstention is scored | Answering them is a failure. |
| Citations | Every answer carries source ids that resolve to a chunk in the trace | Traceability is a rubric dimension. |
| Frozen slice | 15 percent held out; looked at once, at the end | The only number tuning cannot have touched. |
"""),
      code('''
# 0 · harness first: the runner and metrics already exist (rk.run_benchmark, rk.summarize); this cell adds the constraint checks and the cost and latency lines
lab_store, lab_chunks, lab_emb, lab_ret, lab_gen, lab_q = rk.bootstrap(chunker="fixed_40")     # fixed chunking, as the brief specifies
lab_texts = {c.chunk_id: c.text for c in lab_chunks}
tuning = [q for q in lab_q if not q.frozen]; frozen = [q for q in lab_q if q.frozen]
CAP, P95_MS, COST_CEIL = 6000, 4000, 0.03
def latency_ms(cfg, df, turns_for_inference=0):
    t = rk.Timer(); per_q = []
    for q in lab_q:
        with t.stage(q.qid):
            pool = lab_ret.search(q.text, k=cfg.n_pool, mode=cfg.mode)
            if cfg.reranker: pool = cfg.reranker(q.text, pool)
            rk.pack(pool, lab_texts, evidence_cap=cfg.evidence_cap, k=cfg.k)
        extra = (350 * turns_for_inference + 250) if (turns_for_inference and q.qtype == "inference") else 0
        per_q.append(t.ms[q.qid] + 350 + 1550 + extra)
    return float(np.percentile(per_q, 95))
def run_step(name, cfg, turns_for_inference=0):
    df = rk.run_benchmark(cfg, lab_ret, lab_gen, tuning, lab_chunks, lab_store); s = rk.summarize(df)
    cost = float(np.mean([rk.query_cost(3000, int(e), 30, 150, RATES, cached=True)["total"] for e in df["evidence_tokens"]]))
    cites_ok = all(all(c in lab_texts for c in rk.citations_in(a)) for a in df["answer"])
    return {"step": name, "full_chain@5": s["full_chain@k"], "recall@pool": s["recall@pool"], "correct": s["correct"], "null_abstained": s["null_abstained"],
            "evidence tokens (max)": int(df["evidence_tokens"].max()), "p95 ms": round(latency_ms(cfg, df, turns_for_inference)), "dollars per query": round(cost, 5), "citations resolve": cites_ok}
steps = []
rr = rk.make_reranker("maxsim", lab_ret, lab_texts, top=50)
lab_loop = rk.AgentConfig(expand_neighbours=True, token_budget=CAP)
decomp = lambda q, r: rk.decompose_pool(q, r, lab_texts, lab_loop)
chain = [("1 · baseline: fixed_40, dense, k=5", dict(mode="dense"), 0),
         ("2 · + BM25 and RRF (hybrid)", dict(mode="hybrid"), 0),
         ("3 · + reranker over N=50", dict(mode="hybrid", reranker=rr), 0),
         ("4 · + decomposition, inference type only", dict(mode="hybrid", reranker=rr, decompose=decomp), 2)]
for name, kw, turns in chain:
    steps.append(run_step(name, rk.RunConfig(name[:1], n_pool=50, k=5, evidence_cap=CAP, **kw), turns))
lab = pd.DataFrame(steps)
lab["delta full_chain@5"] = lab["full_chain@5"].diff().round(3); lab["delta dollars"] = lab["dollars per query"].diff().round(5)
lab["within constraints"] = (lab["evidence tokens (max)"] <= CAP) & (lab["p95 ms"] <= P95_MS) & (lab["dollars per query"] <= COST_CEIL) & (lab["null_abstained"] >= 1.0) & lab["citations resolve"]
# the stack is kept up to the best cumulative step that passed its constraints; ties go to the cheaper step
ok = lab[lab["within constraints"]]
best = int(ok.sort_values(["full_chain@5", "dollars per query"], ascending=[False, True]).index[0])
lab["verdict"] = ["baseline" if i == 0 else ("shipped" if i <= best and (lab.loc[i, "delta full_chain@5"] > 0) else ("carried, zero delta" if i <= best else "rejected")) for i in range(len(lab))]
display(table(lab.drop(columns=["within constraints"]), "The chain, cumulative. Each step adds one change to the previous one, as the brief prescribes.", precision=5))
'''),
      md("""
| Step | What the rule says | Why |
|---|---|---|
| 1, baseline | Record every number before changing anything. | Without it no later delta means anything. |
| 2, hybrid | Write the delta and the cost delta even when one of them is zero; a zero-delta step that later steps build on is carried, not shipped. | Change one thing, and be honest about what it bought. |
| 3, reranker | Judge it on the full-chain delta at k, inside the constraints; the result differs by chunking, as notebook 04 showed on structural chunks. | A step that does not move the number is a finding, not a failure of the lab. |
| 4, decomposition | Applied to the inference type only, so latency rises on those questions alone; judged on the delta on top of the stack it lands on. | Spend the loop where the question shape demands it. |
| The stack that ships | The steps up to the best cumulative number that passed its constraints, ties broken by cost. | That is what a cumulative build is. |
"""),
      code('''
# the frozen slice, looked at once, at the end, on the shipped configuration
shipped_kw = chain[best][1]
shipped = rk.RunConfig("shipped", n_pool=50, k=5, evidence_cap=CAP, **shipped_kw)
baseline = rk.RunConfig("base", mode="dense", n_pool=50, k=5, evidence_cap=CAP)
fz = pd.DataFrame([rk.summarize(rk.run_benchmark(baseline, lab_ret, lab_gen, frozen, lab_chunks), "baseline"), rk.summarize(rk.run_benchmark(shipped, lab_ret, lab_gen, frozen, lab_chunks), "shipped")]).reset_index().rename(columns={"index": "config"})
display(table(fz[["config", "full_chain@k", "correct", "null_abstained", "evidence_tokens"]], "The frozen slice (three questions), read once"))

# 5 · the decision record, generated from the numbers above
import hashlib, datetime as dt
version = hashlib.sha1("".join(d.body for d in lab_store.docs()).encode()).hexdigest()[:10]
def line(i):
    r = lab.iloc[i]; return f"{r['step']}: full-chain recall at 5 moved {r['delta full_chain@5']:+.3f} for {r['delta dollars']:+.5f} dollars per query and p95 {int(r['p95 ms'])} ms"
shipped_lines = [line(i) for i in range(1, len(lab)) if lab.loc[i, "verdict"] == "shipped"]
carried_lines = [line(i) for i in range(1, len(lab)) if lab.loc[i, "verdict"] == "carried, zero delta"]
rejected_lines = [line(i) for i in range(1, len(lab)) if lab.loc[i, "verdict"] == "rejected"]
fin = lab.iloc[best]
record = f"""
# Decision record: FDE Lab build, corpus {version}, {dt.date.today().isoformat()}

**Shipped.** {"; ".join(shipped_lines) if shipped_lines else "nothing beyond the baseline moved the number"}.

**Carried at zero delta**, because a later shipped step builds on it: {"; ".join(carried_lines) if carried_lines else "none"}.

**Rejected.** {"; ".join(rejected_lines) if rejected_lines else "none"}.

**The number that decided it.** Full-chain recall at k=5 on the tuning slice across the chain: {", ".join(f"{v:.3f}" for v in lab["full_chain@5"])}. The stack ships up to step {best + 1}. Frozen slice, read once: {fz.loc[0, "full_chain@k"]:.3f} baseline against {fz.loc[1, "full_chain@k"]:.3f} shipped.

**Constraints, measured on the shipped stack.** Evidence cap 6,000 against a maximum of {int(fin["evidence tokens (max)"])} tokens. p95 {int(fin["p95 ms"])} ms against a 4,000 ms ceiling (retrieval measured, generation and turn costs illustrative). Cost {fin["dollars per query"]:.5f} dollars per query against 0.03 at the stated rates. Null abstention {fin["null_abstained"]:.2f}. Citations resolve: {fin["citations resolve"]}.

**Revisit when.** A trained or hosted reranker is available (rerun step 3 through the same hook, since the offline stand-in's result depends on chunking); the corpus grows past the point where first-stage precision on single-hop facts degrades; the eval set gains production failures that change the type mix; the frozen slice is refreshed; or the rates in `Rates()` move.
"""
from IPython.display import Markdown
display(Markdown(record))
'''),
      md("""
| Rubric dimension | Meets the bar | Exceeds it | Weight | Where this run stands |
|---|---|---|---|---|
| Measurement discipline | Every change has a before and after on the same set. | Run-to-run variance quoted alongside each delta. | 25 | Before and after are in the table; the variance method is in notebook 06 and is not yet applied here, so this run meets rather than exceeds. |
| Retrieval quality | Full-chain recall improves over baseline inside the token cap. | Gains hold on the frozen slice and the hardest type. | 20 | The frozen slice was read once and is in the record; the hardest type is inference, which is where the gain sits. |
| Grounding and abstention | Citations resolve; nulls are refused. | Abstention threshold justified with a precision-recall curve. | 15 | Both bars met; the curve is not drawn. |
| Cost and latency | Inside both ceilings, measured per query. | A cost-quality frontier with the operating point marked. | 15 | Inside both; the frontier is the lever table in notebook 07. |
| Traceability | Any answer can be replayed from its stored trace. | Traces are diffable between two runs of the same query. | 10 | Traces are in `lab_store.traces`; a diff is a SQL join away. |
| Decision record | What shipped, what was rejected, and why. | Names the condition under which the decision should be revisited. | 15 | Generated above, with the revisit conditions. |

The weighting is deliberate: the decision record is worth as much as the retrieval metrics. That is the FDE job.
""")]

# ---------------------------------------------------------------- recap
C += recap([
    "Decompose against the original question, carry the bridge entity by code, and write every stop condition down before you write the loop.",
    "The loop's worst failure is premature confidence, and on this corpus it was fixed by reading the neighbours of a hit, not by a better prompt.",
    "Score the trace: cumulative recall says whether hop two was reached, evidence retention says whether you kept it, stop quality says whether the check can be trusted.",
    "Default to single-shot and escalate only when the sufficiency check fails; the loop is a cost and latency multiplier you should have to justify.",
    "The lab is the job: harness first, one change at a time, constraints that force the trade-offs, a frozen slice read once, and a decision record that names what was rejected and why.",
], "the FDE Lab build", "Take the eight notebooks, the toolkit, and the brief above. Replace the fixed corpus with a client's, replace the simulator with a provider, and the harness, the gate and the decision record run unchanged.")
C += [md("""
## Interview bank

| Question an interviewer may ask | What a strong answer does | Red flag |
|---|---|---|
| Your client's assistant answers correctly about 80 percent of the time and they want 95 in four weeks. What do you do in week one? | Builds the harness and the eval set, segments the 20 percent by type and stage with the fault tree, and refuses to change anything before it can be measured. | Starts tuning prompts on day one. |
| A retrieval change raises average quality 6 percent, but one business unit says it got worse. Ship it? | Blocks by default, measures that slice, and ships behind a canary only with the owner's sign-off. | Ships on the average. |
| Agentic search costs 0.90 a query on hard questions; finance wants 0.15. What do you change, and what do you refuse? | Escalation policy, caching, dedup, output caps and routing; refuses to drop the reranker below proven recall or to lower k past the frozen-slice check. | Turns the loop off for everyone. |
| How would you know if your LLM judge is wrong? | Cohen's kappa against fresh human labels, position swaps, verbosity and self-preference checks, a pinned judge version. | Trusts it because it is a strong model. |
""")]

write(C, "/home/claude/nb/08_agentic_fde_lab.ipynb", "08 Agentic search and the FDE Lab")
print("built 08 with", len(C), "cells")
