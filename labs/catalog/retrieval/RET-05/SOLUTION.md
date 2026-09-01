# RET-05 · Solution

## Why this returns a dict, not a string

The common version of this exercise returns a formatted string. That is the whole bug.

A string carries the markers and throws away what they mean. Once `build_context` returns
`"[1] Involuntary cancellation…"`, the association between `1` and `fare-rules#7.3` exists nowhere. When
the model later writes "refundable [1]", nobody can check it — not your evaluator, not an auditor, not the
ops agent reading the answer.

You have produced a citation that cannot be wrong. That is not the same as one that is right; it is a
citation that is not *load-bearing*. It looks like grounding and provides none.

The mapping is the deliverable. The string is just the part the model reads.

## The exclusion decision

A chunk with no `source_id` has three possible fates, and only one is defensible:

- **Include unnumbered** — the model has text it cannot attribute, sitting right next to text it can. It
  will use both. Ungrounded content enters the answer wearing the same clothes as grounded content.
- **Number it anyway** — you have asserted provenance you do not have. This is worse than the first
  option, because now it survives an audit that only checks whether markers resolve.
- **Exclude and record** — the context is smaller, and you can say exactly what was dropped and why.

The third costs recall. That cost is visible and arguable. The other two cost correctness invisibly.

## The embedded-marker trap

The Break phase feeds you a chunk whose own text contains `[1]` — a footnote marker from the source
document. Solutions that build the context by regex-rewriting bracketed numbers, or that renumber after
assembly, corrupt the mapping here: chunk two's marker shifts, and every claim attributed to it now points
at the wrong passage.

The fix is structural rather than clever: assign markers **as you iterate**, before any string exists, and
never parse the assembled context to work out what the markers were. Prefix, do not rewrite.

## Two passages, one document, two markers

`SAME_SOURCE` is not an edge case, it is the normal case — retrieval routinely returns several chunks from
one policy document. If they share a marker, a verifier resolving "refundable [1]" cannot tell which of
two passages the model actually used, and the answer becomes uncheckable exactly where documents are long
enough for it to matter.

Two markers, both pointing at the same `source_id`, is correct. The marker identifies the *passage in
context*; the `source_id` identifies the *document*. Different jobs.

## What this buys you

With the mapping in hand, a grounding check is about fifteen lines: extract every `[n]` from the answer,
look each up, fetch the source text, and ask whether it entails the claim. That moves you from
[E2 to E4](../../../../cheatsheets/frameworks/evidence-ladder.md) on the evidence ladder — from "we have
citations" to "citation accuracy is 0.94 on a 130-case set".

Without the mapping, that check cannot be written at all, at any budget.

## Field guide

[Grounding Triangle](../../../../cheatsheets/frameworks/grounding-triangle.md) — this lab is side ③ ·
[Evidence Ladder](../../../../cheatsheets/frameworks/evidence-ladder.md) ·
[RAG pipeline](../../../../cheatsheets/quick-reference/rag-pipeline.md)
