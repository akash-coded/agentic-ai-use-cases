from nbtools import md, code, fig, deck, header, recap, write, SETUP

C = []
C += header(1, "Foundations: retrieval sets the ceiling",
            "You build the in-memory system, run the three retrieval modes on one worked question, and learn to score each handoff so a wrong answer points at the stage that owns it.",
            deck("spine_s1", "The evidence pipeline with FIND and JUDGE lit", "The FIND stage and the JUDGE layer are what this notebook exercises."),
            "Every company, person and figure in the corpus is fictional, so nothing here misstates a real fact. The techniques are real.",
            "The session deck, sections 1 and 2.", "Notebook 02, which builds the benchmark you will measure against.")

# ---------------------------------------------------------------- 1 setup
C += [md(f"""
## 1 · Build the system in memory

Everything you retrieve from lives in a SQLite database created in memory. Documents are cut into chunks, the chunks are indexed twice, once as an inverted index for lexical search and once as vectors for semantic search, and a retriever wraps both. Nothing is written to disk, so any state can be inspected with a SQL query.

{fig([("corpus","30 fictional\\ndocuments","data"),("db","SQLite\\n:memory:","data"),("chunk","Chunk\\n(structural)"),("bm25","Inverted index\\n+ BM25","tool"),("lsa","LSA vectors\\n+ flat index","tool"),("ret","Retriever\\nlexical, dense, hybrid","end")],
      [("corpus","db"),("db","chunk"),("chunk","bm25"),("chunk","lsa"),("bm25","ret"),("lsa","ret")], caption="What the setup cell builds. The dense embedder is latent semantic analysis, an established 1990s dense retriever used as a stand-in; a real embedder replaces it through one config line.")}
"""),
      code(SETUP),
      code('''
store, chunks, embedder, retriever, generator, questions = rk.bootstrap(chunker="structural")
print(f"{len(store.docs())} documents, {len(chunks)} chunks, {len(questions)} benchmark questions, embedder = {embedder.name}, generator = {generator.name}")
table(store.sql("SELECT doc_id, title, source, date, tenant FROM docs ORDER BY date").head(8), "First eight documents by date")
'''),
      md("""
| What the store holds | Why it is a table and not a Python list |
|---|---|
| `docs` carry title, source, date, tenant and an access-control list. | Metadata filtering, provenance and permission checks all need these fields at query time. |
| `chunks` carry a stable id built from document id, ordinal and a content hash. | An unchanged chunk keeps its id across rebuilds, which is what makes incremental re-indexing possible in notebook 03. |
| `index_versions` records which chunker and embedder built each version, and which one is live. | A rebuild with a new embedding model becomes a new version you can swap to and roll back from. |
| `traces` stores what each query retrieved, packed and answered. | The trace is the single artefact that lets you localise a failure after the fact. |
""")]

# ---------------------------------------------------------------- 2 worked question
C += [md(f"""
## 2 · One question carried through all eight notebooks

The question needs two facts that live in two different articles, joined only by a person's name. Either article alone yields a confident wrong answer. A third article is a distractor with high word overlap and the wrong company.

{deck("anchorDocs", "The two gold articles, the distractor, and the answer", "Own construction, fictional companies. The answer is Vega Dynamics, 2023.")}
"""),
      code('''
anchor = rk.ANCHOR
print("QUESTION:", anchor.text, "\\nANSWER:  ", anchor.answer, "\\n")
for doc_id in ["a1", "b7", "d3"]:
    d = store.doc(doc_id)
    print(f"[{doc_id}] {d.title}  ({d.source}, {d.date})\\n    {d.body[:230]}...\\n")
gold = rk.resolve_gold(anchor, chunks)
table(pd.DataFrame([{"doc": d, "gold span": s[:70] + "...", "carried by chunk": ", ".join(c) or "NO CHUNK (boundary loss)"} for (d, s), c in gold.items()]),
      "Each gold span resolves to the chunk that carries it whole")
'''),
      md("""
| Planted feature in the example | The technique it exercises | Where it bites if you get it wrong |
|---|---|---|
| The two facts sit in different articles, joined only by the name Elena Ruiz. | Multi-hop retrieval and the missing-hop problem. | One retrieval finds half the chain and the model invents the rest. |
| The proper noun Nord Aerospace appears verbatim in the source. | Lexical retrieval on exact identifiers. | A purely semantic search can drift to similar-sounding firms. |
| The question says became CEO while the source says named as chief executive. | Semantic retrieval across paraphrase. | A purely lexical search misses the relevant passage. |
| A distractor says Vela Systems appointed a new chief executive in 2026. | Reranking and precision under high term overlap. | The distractor outranks the real evidence and pollutes the context. |
| Each article carries a date and a source, and an earlier article names an interim chief executive. | Metadata filtering and provenance. | Undated evidence cannot be filtered, so the 2025 interim appointment beats the 2026 one. |
""")]

# ---------------------------------------------------------------- 3 ceiling
C += [md(f"""
## 3 · Retrieval sets the ceiling before the model writes a word

The generator can only work with what retrieval hands it. The cell below runs the same generator twice on the same question. The only thing that changes is the evidence it is given.

{fig([("q","Question","start"),("r","Hybrid retrieve\\ntop 5"),("p1","Pack what\\nwas found"),("g1","Generate","proc"),("a1","Answer or\\nabstain","end"),("gold","Pack the two\\ngold chunks","ok"),("g2","Same generator","proc"),("a2","Answer","end")],
      [("q","r"),("r","p1"),("p1","g1"),("g1","a1"),("q","gold"),("gold","g2"),("g2","a2")], caption="Two runs, one generator. The generator is a documented mock here: it answers only when every required fact is present, and abstains with a stated gap otherwise.")}
"""),
      code('''
texts = {c.chunk_id: c.text for c in chunks}
gold_sets = rk.gold_chunk_sets(anchor, chunks)

pool = retriever.hybrid(anchor.text, k=50)
top5 = [cid for cid, _ in pool[:5]]
print("top-5 chunk ids:", top5)
print("coverage of gold spans in the top 5:", rk.coverage(gold_sets, top5))
print("answer from the top 5 :", generator.answer(anchor, top5, texts).text, "\\n")

gold_ids = [sorted(s)[0] for s in gold_sets]
print("coverage when the two gold chunks are packed:", rk.coverage(gold_sets, gold_ids))
print("answer from the gold chunks:", generator.answer(anchor, gold_ids, texts).text)
'''),
      md(f"""
{deck("answerSpace", "Each narrowing step limits what the answer can reach", "Established idea, own drawing. Anything dropped early cannot reappear later.")}

| Run | Evidence handed to the generator | Outcome | What it proves |
|---|---|---|---|
| Top 5 from hybrid retrieval | The right documents rank near the top, but not the chunks that carry the two facts. | An abstention with a stated gap. | The ceiling was set at the retrieve and select steps, not in generation. |
| The two gold chunks, packed by hand | Both facts, each with a source id. | The correct answer with two citations. | The same generator is fully capable once the evidence arrives. |

The number to remember from this run is the coverage. It moved from 0.0 to 1.0 and nothing else changed.
""")]

# ---------------------------------------------------------------- 4 three ways
C += [md(f"""
## 4 · Three ways to retrieve, and they answer different questions

### 4a · Lexical: an inverted index scored by BM25

{deck("invertedIndex", "Terms map to the chunks that contain them; BM25 scores each match", "Established: Okapi BM25 with k1 for term-frequency saturation and b for length normalisation. The implementation in ragkit prints every term's contribution.")}
"""),
      code('''
hits = retriever.lexical("Nord Aerospace", k=4)
display(table(retriever.show(hits), "BM25 for the exact name"))
display(table(retriever.bm25.explain("Nord Aerospace", hits[0][0]), "Per-term contribution to the top chunk: the rarer term carries the score"))

trap = retriever.lexical("Kestrel engine", k=5)
table(retriever.show(trap), "The Kestrel trap: an engine called Kestrel and a food company called Kestrel compete on the same token")
'''),
      md("""
| BM25 wins when | BM25 loses when | Because |
|---|---|---|
| The query carries an exact name, code, ticker or error string. | The user paraphrases and shares no tokens with the source. | Scoring is over tokens; a token that is absent contributes nothing. |
| A rare term identifies the document, as `nord` does above. | A common token is shared by unrelated documents, as `kestrel` is. | Inverse document frequency rewards rarity, and it cannot tell an engine from a food company. |
"""),
      md(f"""
### 4b · Semantic: encode once, then search by nearest neighbour

{deck("encoderANN", "Documents are embedded offline, the query online, and the closest vectors are returned", "Established shape. Here the encoder is latent semantic analysis fitted on the corpus, so paraphrase is captured only as far as co-occurrence allows. Treat its ranking as a stand-in for a neural embedder, not as its equal.")}
"""),
      code('''
q = "who now runs the launch company after the leadership change"
dense = retriever.dense(q, k=5)
lex = retriever.lexical(q, k=5)
def rank_of(ranked, doc_id):
    r = [i + 1 for i, (cid, _) in enumerate(ranked) if cid.startswith(doc_id + ":")]
    return r[0] if r else "not in top 5"
print(f"a1 (the appointment article) ranks {rank_of(dense,'a1')} in dense and {rank_of(lex,'a1')} in lexical")
display(table(retriever.show(dense), "Dense retrieval on a paraphrase. Notice which article ranks first."))

filtered = retriever.dense(q, k=5, date_from="2026-01-01")
table(retriever.show(filtered), "The same query with a metadata pre-filter: dated on or after 2026-01-01")
'''),
      md("""
| What happened | The lesson |
|---|---|
| Dense retrieval placed the appointment article in its top 5 where lexical retrieval did not, because the query shares almost no tokens with the source. | Semantic retrieval covers the paraphrase blind spot of lexical retrieval. |
| The first result was the 2025 article naming the interim chief executive, not the 2026 appointment. | Semantic closeness is not correctness. The two articles mean almost the same thing and only the date tells them apart. |
| A date pre-filter fixed the ranking without touching the embedder. | Metadata is a retrieval signal in its own right, and filtering before ranking is how you use it. |
"""),
      md("""
### 4c · Grep: literal patterns in files, logs and code

Grep is not a ranking. It answers a different question: does this exact pattern occur, and on which line. Identifiers, error codes and engine designations are where it is the right tool.
"""),
      code('''
display(table(pd.DataFrame(rk.grep(chunks, r"ERR-4471")), "Literal search for an error code"))
display(table(pd.DataFrame(rk.grep(chunks, r"VD-[57]")), "A regular expression over engine designations"))
print("BM25 also finds the identifier, because it is a token:", retriever.lexical("ERR-4471", k=1)[0][0])
print("but grep works on files that were never indexed, and returns the line, not a chunk score.")
'''),
      md(f"""
### 4d · Which mode, decided by the signal in the query

{fig([("q","What does the\\nquery hinge on?","dec"),("id","Exact identifier,\\nname, code","proc"),("mean","Meaning or\\nparaphrase","proc"),("pat","Literal pattern in\\nfiles or logs","proc"),("both","Both an exact term\\nand an idea","proc"),("lex","Lexical, BM25","tool"),("den","Dense, embeddings","tool"),("grep","Grep","tool"),("hyb","Hybrid, then fuse","ok")],
      [("q","id"),("q","mean"),("q","pat"),("q","both"),("id","lex"),("mean","den"),("pat","grep"),("both","hyb")], rankdir="TD", caption="Own construction. The decision runner below executes it on three real queries.")}
""")]
C += [code('''
def signal(query):
    toks = rk.tokenize(query, keep_stop=True)
    has_id = any(t[0].isdigit() or "-" in t or t.isupper() for t in query.split())
    proper = sum(1 for w in query.split()[1:] if w[:1].isupper())
    return {"has_identifier": has_id, "proper_nouns": proper, "n_tokens": len(toks)}

MODE_TREE = [
    {"q": "Does the query contain a literal identifier or code?", "test": lambda f: f["has_identifier"], "yes": "grep, then lexical as a fallback", "no": None,
     "show": lambda f: f"has_identifier={f['has_identifier']}"},
    {"q": "Does it carry a proper noun that will appear verbatim in the source?", "test": lambda f: f["proper_nouns"] >= 1, "yes": None, "no": "dense retrieval, the query is meaning-only",
     "show": lambda f: f"proper_nouns={f['proper_nouns']}"},
    {"q": "Is it also long enough to carry an idea beyond the name?", "test": lambda f: f["n_tokens"] >= 6, "yes": "hybrid, lexical for the name plus dense for the idea, then fuse", "no": "lexical, the name is the whole query",
     "show": lambda f: f"n_tokens={f['n_tokens']}"},
]
for q in ["ERR-4471", "Nord Aerospace", anchor.text]:
    display(table(decision(MODE_TREE, signal(q)), f"Decision path for: {q[:60]}"))
'''),
      md("""
| If | Then reach for | Because |
|---|---|---|
| The query hinges on an exact identifier, code, name or error string. | Lexical retrieval with BM25, or grep when the source is a file. | An exact token match is precise and cheap, and it does not drift to lookalikes. |
| The query hinges on meaning, intent or a paraphrase of the source wording. | Semantic retrieval with dense vectors. | Embeddings place related meanings near each other even when the words differ. |
| The query carries both an exact term and a paraphrased idea, as the worked question does. | A hybrid of lexical and semantic, fused by rank. | Each mode covers the other's blind spot, and fusion keeps items that both rank well. |

The runner is a heuristic over surface features and it is written that way on purpose: in production the same decision is usually made per query by a small router, and the router itself needs an evaluation.
""")]

# ---------------------------------------------------------------- 5 recall budget
C += [md(f"""
## 5 · The pipeline is a recall budget spent on precision

First-stage retrieval buys recall cheaply over the whole corpus. Every later stage can only lose evidence, never recreate it. So the question to ask of stage one is not whether the top 5 is right, but whether the gold evidence is anywhere in a wide candidate pool.

{fig([("s1","Stage 1 · cheap\\nFirst-stage retrieval\\nbuys recall","tool"),("s2","Stage 2 · expensive\\nReranking\\nconverts recall to precision","proc"),("s3","Stage 3 · scarce\\nContext packing\\nfixed token budget","cost"),("s4","Stage 4 · judged\\nGeneration\\nturns evidence into a claim","proc"),("n1","knob: N, hybrid\\nweights, chunking","note"),("n2","knob: model class,\\ncandidate depth","note"),("n3","knob: k, dedup,\\nordering","note"),("n4","knob: instructions,\\nabstention, citations","note")],
      [("s1","s2"),("s2","s3"),("s3","s4"),("n1","s1"),("n2","s2"),("n3","s3"),("n4","s4")], caption="Mental model taken from the advanced-track deck. Anything lost at stage one is lost permanently.")}
""")]
C += [code('''
answerable = [q for q in questions if q.gold]
Ns = [3, 5, 10, 20, 50]
recall_at_N, chain_at_N = [], []
for N in Ns:
    r, ch = [], []
    for q in answerable:
        gs = rk.gold_chunk_sets(q, chunks)
        ids = [cid for cid, _ in retriever.hybrid(q.text, k=50)]
        r.append(rk.evidence_recall_at_k(gs, ids, N)); ch.append(rk.full_chain_recall(gs, ids, N))
    recall_at_N.append(np.mean(r)); chain_at_N.append(np.mean(ch))
lines(Ns, {"span recall @N": recall_at_N, "full-chain recall @N": chain_at_N}, "Recall climbs with the candidate pool, hybrid retrieval, 9 answerable questions", "N candidates", "recall")
table(pd.DataFrame({"N": Ns, "span recall": np.round(recall_at_N, 3), "full-chain recall": np.round(chain_at_N, 3)}), "Measured on this corpus")
'''),
      md("""
| Stage | What it can fix | What it cannot fix | The number to measure before touching it |
|---|---|---|---|
| Stage 1, first-stage retrieval | Whether the gold evidence is in the pool at all. | Nothing downstream; it only supplies candidates. | Full-chain recall at N, with N in the tens, as in the curve above. |
| Stage 2, reranking | The order of the pool, so gold rises above distractors. | A gold chunk that is not in the pool. | Full-chain recall at k after reranking, compared with stage one at the same k. |
| Stage 3, packing | Which of the ranked chunks fit the token budget, and in what order. | Anything the reranker put below the cut. | Coverage of gold spans in the packed context. |
| Stage 4, generation | Whether the claim is grounded, cited and abstains when it should. | Missing evidence. | Correctness and faithfulness, scored together. |

The single most common architectural mistake is tuning stage two or three to fix a recall problem created in stage one. The curve tells you which case you are in: if full-chain recall is low at N=50, the problem is upstream of every reranker.
""")]

# ---------------------------------------------------------------- 6 three ways to eval
C += [md("""
## 6 · Three ways to tell whether a change helped

| Evaluation mode | The question it answers | What it costs you |
|---|---|---|
| Offline, on a fixed labelled set | Did this change move a metric against known-good answers? | You must build and maintain a labelled set that reflects real queries. Notebook 02 builds one. |
| Online, with real traffic | Do real users behave better with the change than without it? | You need traffic, guardrails, and time for a result to become trustworthy. |
| An LLM as a judge | Does a strong model rate this answer higher on a written rubric? | The judge has its own bias and drift, so it needs calibration. Notebook 06 calibrates one. |

The cell below is the offline mode in its simplest form: the same benchmark, three retrieval modes, one table.
"""),
      code('''
runs = {}
for mode in ["lexical", "dense", "hybrid"]:
    cfg = rk.RunConfig(name=mode, mode=mode, n_pool=50, k=5)
    runs[mode] = rk.summarize(rk.run_benchmark(cfg, retriever, generator, questions, chunks, store), mode)
table(pd.DataFrame(runs).T.reset_index().rename(columns={"index": "mode"}), "Offline evaluation at k=5. Retrieval metrics average the 9 answerable questions; correct and faithful average all 12.")
'''),
      md("""
Read the table across, not down. Full-chain recall at k=5 is the multi-hop number, and it is the one that separates the modes. Correctness follows it almost exactly, because the generator here is grounded by construction. With a real model the two would diverge, and that gap is what faithfulness measures in notebook 06.
""")]

# ---------------------------------------------------------------- 7 handoffs + fault tree
C += [md(f"""
## 7 · Measure each handoff, then let a tree name the owning stage

{deck("handoffChecks", "Three checks localise the fault", "A single end score hides which stage failed. Three checks, one per handoff, name it.")}
""")]
C += [code('''
cfg = rk.RunConfig(name="hybrid_k5", mode="hybrid", n_pool=50, k=5)
pool = retriever.hybrid(anchor.text, k=cfg.n_pool)
pool_ids = [cid for cid, _ in pool]
packed = rk.pack(pool, texts, evidence_cap=6000, k=cfg.k)
ans = generator.answer(anchor, packed.chunk_ids, texts)
print("gold chunks rank in the pool:", {sorted(s)[0]: pool_ids.index(sorted(s)[0]) + 1 for s in gold_sets})
display(verdict_style(rk.handoffs(anchor, gold_sets, pool_ids, packed.chunk_ids, ans.text, texts, k_pool=50), "verdict"))
display(table(rk.fault_tree(gold_sets, pool_ids, packed.chunk_ids, ans.text, anchor, texts), "The four-question fault tree, executed on this trace"))

packed20 = rk.pack(pool, texts, evidence_cap=6000, k=20)
ans20 = generator.answer(anchor, packed20.chunk_ids, texts)
print("\\nwith k=20 the same pool yields:", ans20.text)
'''),
      md(f"""
{fig([("q1","Q1 Is every gold span in\\nthe packed context?","dec"),("q2","Q2 Was every gold chunk in\\nthe candidate pool?","dec"),("q3","Q3 Is the answer grounded,\\ncited, not an abstention?","dec"),("q4","Q4 Does the answer match\\nthe gold?","dec"),("f1","First-stage recall fault:\\nchunking, embedding,\\nhybrid weights, filters","fail"),("f2","Ranking or packing fault:\\nreranker, fusion, k,\\ndedup, truncation","fail"),("f3","Generation fault: grounding,\\nabstention, citation contract","fail"),("f4","Generation fault: right evidence,\\nwrong conclusion","fail"),("ok","Pipeline correct. Suspect the\\nlabel, question or rubric","ok")],
      [("q1","q2","no"),("q1","q3","yes"),("q2","f1","no"),("q2","f2","yes"),("q3","f3","no"),("q3","q4","yes"),("q4","f4","no"),("q4","ok","yes")], rankdir="TD",
      caption="The fault-isolation tree from the advanced-track deck. Four questions reach a single owning stage.")}

| If the tree stops at | The fault sits in | So the first fix to try |
|---|---|---|
| Q2 answered no | First-stage recall, and possibly the index behind it. | Widen N, switch to hybrid, or revisit chunking. Notebook 03. |
| Q2 answered yes | Ranking or packing, which is where the worked question failed above: both gold chunks were in the pool of 50, at ranks 7 and 19, and k=5 cut them. | Rerank the pool or raise k. Notebook 04 and 05. |
| Q3 answered no | Generation controls. | Grounding instruction, citation contract, abstention policy. Notebook 05. |
| Q4 answered no | The model read the right evidence and still concluded wrongly. | Model choice, or the rubric itself. Notebook 06. |
| Q4 answered yes | Nothing in the pipeline. | Check the label. Ambiguous gold answers are an under-reported source of regressions. |
""")]

# ---------------------------------------------------------------- 8 silent failures
C += [md(f"""
## 8 · Four failures that never throw an error

{fig([("s","A plausible,\\nconfident answer","start"),("a","Missing hop:\\nhalf the chain\\nnever retrieved","fail"),("b","Distractor capture:\\nwrong firm outranks\\nthe real one","fail"),("c","Metric masking:\\nthe mean holds while\\none type collapses","fail"),("d","Correct by chance:\\nright answer with no\\nevidence behind it","fail")],
      [("s","a"),("s","b"),("s","c"),("s","d")], caption="Each one shows up as a fluent answer that happens to be wrong, or a right answer that will not survive the next release.")}
"""),
      code('''
# (a) the missing hop: already seen in section 3. Half the chain arrives, the grounded generator abstains, an ungrounded one would guess.

# (b) distractor capture: a query about the 2026 appointment pulls the wrong firm alongside the right one
q = "which aerospace company appointed a new chief executive in 2026"
display(table(retriever.show(retriever.hybrid(q, k=4)), "(b) Vela Systems and Nord Aerospace compete on the same tokens"))

# (c) metric masking: the mean hides the type that fails
df_dense = rk.run_benchmark(rk.RunConfig("dense_k5", mode="dense", k=5), retriever, generator, questions, chunks)
by_type = df_dense.groupby("type")[["full_chain@k", "correct"]].mean().round(2).reset_index()
print(f"(c) mean correctness = {df_dense['correct'].mean():.2f}, but by type:")
display(table(by_type, "(c) The inference type, the dependent multi-hop questions, is where the baseline fails"))

# (d) correct by chance: an ungrounded generator gets q01 right with zero evidence
ungrounded = rk.MockGenerator(p_parametric=1.0)
df_ung = rk.run_benchmark(rk.RunConfig("dense_k5_ungrounded", mode="dense", k=5), retriever, ungrounded, questions, chunks)
cells = df_ung["cell"].value_counts().rename_axis("attribution cell").reset_index(name="questions")
display(table(cells, "(d) With p_parametric=1.0 the answerable questions are all correct; the ones with no evidence are correct by chance, and the null questions are fabricated"))
'''),
      md("""
| Silent failure | What you saw | Which metric catches it |
|---|---|---|
| Missing hop | The pool held one article's chunk in the top 5 and the other at rank 19. | Full-chain recall, not span recall, since the mean of the two spans hides that only one arrived. |
| Distractor capture | Vela Systems ranked next to Nord Aerospace on the same tokens. | Precision at k, and later a reranker that reads query and passage together. |
| Metric masking | Mean correctness of 0.83 hid an inference-type score of 0.33. | Any metric segmented by question type, slice or tenant. |
| Correct by chance | Every answerable question scored correct with no evidence packed. | Faithfulness alongside correctness, which is the attribution 2x2 in notebook 06. |
""")]

# ---------------------------------------------------------------- 9 recap, try it, interview
C += recap([
    "Retrieval sets the ceiling on answer quality, so the generator can only be as good as the evidence it is handed. Coverage went from 0.0 to 1.0 and nothing else changed.",
    "There are three retrieval modes, and you pick among lexical, semantic and grep by the signal the query hinges on. Production runs the first two together and fuses them.",
    "Stage one buys recall over a wide pool; every later stage can only spend it. Measure full-chain recall at N before you touch a reranker.",
    "You measure the three handoffs separately and let the four-question tree name the owning stage. The worked question failed at ranking, not at recall.",
    "Most real failures are silent, so you segment metrics by type and score faithfulness next to correctness.",
], "02 · The MultiHop benchmark", "The eval set you just measured against was handed to you. Notebook 02 shows what a benchmark record is scored against, why the null questions matter, and how to manufacture an eval set from a client corpus that has no labels.")
C += [md("""
## Try it

Change `K` and `MODE` and rerun the cell. Watch full-chain recall and the attribution cells move together.
"""),
      code('''
K, MODE = 8, "hybrid"
df_try = rk.run_benchmark(rk.RunConfig(f"{MODE}_k{K}", mode=MODE, n_pool=50, k=K), retriever, generator, questions, chunks)
display(table(df_try[["qid", "type", "full_chain@k", "coverage", "correct", "cell"]], f"{MODE} at k={K}"))
rk.summarize(df_try, f"{MODE}_k{K}")
'''),
      md("""
## Interview corner

| Question an interviewer may ask | What a strong answer does | Red flag |
|---|---|---|
| Walk me through why retrieval sets the ceiling on answer quality. | Separates the ceiling set by evidence selection from the model's own competence, and names coverage as the number that proves it. | Talks only about prompt wording or model size. |
| Your accuracy metric is flat but users say it got worse. What could be happening? | Segments the metric by type and slice, pulls traces, and walks the handoffs to localise the change. | Concludes nothing changed because the top-line number held. |
| Given a query, how would you choose between lexical and semantic retrieval? | Reads the signal in the query, and defaults to hybrid with fusion when both signals are present. | Picks one mode for every query. |
""")]

write(C, "/home/claude/nb/01_foundations.ipynb", "01 Foundations")
print("built 01 with", len(C), "cells")
