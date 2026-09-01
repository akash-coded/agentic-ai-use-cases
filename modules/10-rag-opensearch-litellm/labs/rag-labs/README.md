# FDE Academy · Retrieval, RAG and Evals · Lab notebooks

Eight one-click notebooks, one per session section, over a shared in-memory toolkit (`ragkit`). Every notebook runs offline end to end with Run All.

## Run

1. Keep the `ragkit` folder next to the notebooks.
2. Open a notebook in JupyterLab, VS Code or Colab (upload the folder) and choose Run All.
3. Requirements: Python 3.10 or later with numpy, pandas, matplotlib and scikit-learn. `tiktoken` (exact token counts) and `boto3` (AWS Bedrock) are optional and detected automatically.

## Notebooks in this folder

| # | Notebook | What you run |
|---|---|---|
| 01 | `01_foundations.ipynb` | The in-memory system, three retrieval modes on the worked question, the recall budget, the three handoffs, the fault-isolation tree, four silent failures. |
| 02 | `02_multihop_benchmark.ipynb` | The benchmark record, per-type results, dependent against independent hops measured, the eval-set manufacturing pipeline, the frozen slice, a gated loader for the real MultiHop-RAG set. |
| 03 | `03_index_design.ipynb` | Chunking strategies measured, boundary loss, the title-carry trade, query traces, index freshness with a versioned swap and the mixed-vectors outage, permission-aware retrieval, contextual retrieval on this corpus. |
| 04 | `04_retrieval_reranking.ipynb` | BM25's two knobs, cosine geometry on the real index, the ANN recall knob against a flat scan, index and embedding-model decision trees, rank fusion with every contribution shown, grep against indexes, late-interaction reranking measured, the smallest trained reranker and what it learned, the latency budget. |
| 05 | `05_context_generation.ipynb` | The 32k budget with hard caps, the top-k sweep with three fighting curves, packing rules with syndicated duplicates, position and ordering, the prompt skeleton and citation contract, answer-or-abstain with conflict detection, everything-in-context projected. |
| 06 | `06_evaluation_gate.ipynb` | Every layered metric written out, the failure-to-metric map, the attribution 2x2 over the benchmark, judge calibration with Cohen's kappa and a position-swap check, paired against unpaired variance, the release gate and ship tree on two candidates. |
| 07 | `07_tokens_cost.ipynb` | Four token categories on a real request, a prefix-cache simulator against five cache killers and the TTL trap, break-even, verified provider multipliers with dollar rates as parameters, one answer priced as line items, the cost levers pulled in order with quality measured, index-side against query-side spend. |
| 08 | `08_agentic_fde_lab.ipynb` | Decomposition with the bridge entity carried by code, tool selection, the loop on the worked question and its premature-confidence failure fixed by neighbour expansion, stop conditions as config, trace metrics, single-shot against parallel against loop with an escalation policy, the Bedrock swap, and the FDE Lab brief executed with a decision record generated from the numbers. |

## Connecting AWS Bedrock

Set these before opening a notebook, or call `rk.configure(...)` in the setup cell.

| Variable | Meaning | Default |
|---|---|---|
| `RAGKIT_PROVIDER` | `mock` runs offline; `bedrock` uses AWS. | `mock` |
| `AWS_REGION` | Region with the models enabled. | `us-east-1` |
| `RAGKIT_BEDROCK_KB_ID` | A Bedrock Knowledge Base id; when set, `rk.get_kb()` returns a drop-in retriever. | unset |
| `RAGKIT_BEDROCK_LLM` | Model id for the Converse API. | `amazon.nova-lite-v1:0` |
| `RAGKIT_BEDROCK_EMBED` | Embedding model id. | `amazon.titan-embed-text-v2:0` |

`rk.make_reranker("bedrock", ...)` calls Bedrock's rerank endpoint (`cohere.rerank-v3-5:0` by default); `rk.make_reranker("llm", ...)` scores passages with the configured model.

API names in `ragkit/providers.py` were verified against AWS documentation on 2026-08-31. The offline generator is a documented simulator of the generation stage, not a language model; the offline embedder is latent semantic analysis, an established dense retriever used as a stand-in.

## Regenerating the notebooks

`build/` holds the builders. `python3 build/nb01.py` rewrites `01_foundations.ipynb` from its cell spec; `build/diag.py` renders the flowcharts and decision trees with graphviz (`dot` must be on the path) and embeds them with their Mermaid source collapsed beneath; `build/img/` holds the session deck's diagrams as PNG. After rebuilding, execute in place with `jupyter nbconvert --to notebook --execute --inplace <notebook>`.

## The corpus

Thirty fictional documents and twelve benchmark questions live in `ragkit/corpus.py`. Every company, person and figure is invented. Gold evidence is stored as exact sentences, so recall can be scored at chunk level under any chunking strategy.
