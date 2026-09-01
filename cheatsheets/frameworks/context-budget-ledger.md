# The Context Budget Ledger

> **One line:** the context window is a budget you allocate, not a container you fill.

Nobody decides how to spend the window. It fills up by accident, and then something important gets pushed
out by something unimportant. This ledger makes the allocation a decision.

---

## The allocation

Start from your window size and allocate **before** you build. Leave real headroom.

| Segment | Share | Notes |
| --- | --- | --- |
| System instructions | 5–10% | Fixed. Charged every turn |
| Tool schemas | 5–15% | Fixed per route. Prune per route |
| Conversation history | 15–25% | **Capped.** Summarise past the cap |
| Retrieved context | 25–40% | The main variable. Cap by token count, not by k |
| Output reservation | 15–25% | The model needs room to answer |
| **Headroom** | **15%** | For the turn that is longer than you expected |

If any segment has no cap, it will eventually consume the headroom and then someone else's share.

## Worked example — 200k window

| Segment | Budget | Enforcement |
| --- | --- | --- |
| Instructions | 12k | Reviewed; fails CI if it grows past |
| Tool schemas | 15k | Route-specific attachment |
| History | 40k | Summarise when exceeded |
| Retrieval | 70k | Pack to budget; drop lowest-ranked |
| Output | 40k | `maxTokens` |
| Headroom | 23k | Alert at p99 > 85% used |

## The two enforcement points

**1. Pack retrieval to a token budget, not a document count.**

`top_k=5` is not a budget. Five long passages can be four times five short ones. Pack by tokens:

```python
def pack(passages, budget):
    out, used = [], 0
    for p in passages:                    # already ranked
        t = count_tokens(p.text)
        if used + t > budget: break
        out.append(p); used += t
    return out, used
```

**2. Summarise history at a threshold, not on a schedule.**

Summarising every turn costs a model call every turn. Summarise when the buffer crosses its cap.

## The dilution effect

Filling the window is not free even when it fits. Attention degrades across a long context, and material
in the middle is used least. Two consequences:

- **Rank matters more than recall.** A relevant passage placed 40th is close to absent.
- **More context can lower accuracy.** If your golden-set score drops when you raise `top_k`, that is
  dilution, and it is a real result — not noise.

Measure it: run the golden set at k = 3, 5, 10, 20 and plot. The curve usually peaks and then falls. Most
teams never look and sit on the wrong side of the peak.

## The overflow protocol

Decide in advance what gets dropped, because something will:

| Priority | Segment | Drop order |
| --- | --- | --- |
| 1 — never drop | System instructions, current message | — |
| 2 | Tool schemas for the current route | — |
| 3 | Retrieved context | Drop lowest-ranked first |
| 4 | Conversation history | Summarise oldest first |

A system that silently truncates has an accidental protocol. Make yours deliberate — and log when it fires.

## Where this shows up

- [Module 09](../../modules/09-llm-memory/) — memory strategies and what each drops
- [Module 10 · context packing](../../modules/10-rag-opensearch-litellm/labs/rag-labs/05_context_generation.ipynb)
- `ragkit.context` — [the packing implementation](../../modules/10-rag-opensearch-litellm/labs/rag-labs/ragkit/context.py)

**Related:** [Token Tax Ledger](token-tax-ledger.md) · [Silent Degradation Watchlist](silent-degradation-watchlist.md)
