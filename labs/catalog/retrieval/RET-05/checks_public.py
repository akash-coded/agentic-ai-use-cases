from harness import check, expect, expect_eq, expect_in, expect_not_in
from _fixtures import GOOD, SAME_SOURCE, RAGGED


@check("markers are sequential from 1, in order of appearance")
def t_markers(m):
    r = m.build_context(GOOD)
    expect_in("[1] Involuntary", r["context"], "first chunk gets [1], immediately before its text")
    expect_in("[2] Refunds", r["context"], "second chunk gets [2]")


@check("chunks are separated by a blank line")
def t_sep(m):
    r = m.build_context(GOOD)
    expect_in("\n\n[2]", r["context"], "a blank line between chunks")


@check("the source_id never appears in the context",
       "The model cites the number; the number is what your verifier resolves.",
       teaches="A source path in the prompt invites the model to quote it instead of the marker, and the marker is the checkable part.")
def t_no_source_leak(m):
    r = m.build_context(GOOD)
    expect_not_in("fare-rules#7.3", r["context"], "source ids belong in citations, not context")
    expect_not_in("refund-policy", r["context"], "no source path in the prompt text")


@check("citations map every marker back to its source")
def t_citations(m):
    r = m.build_context(GOOD)
    expect_eq(r["citations"], {1: "fare-rules#7.3", 2: "refund-policy#2.1"},
              "keys are the integer markers used in the context")


@check("two passages from the same source get different markers",
       "They are different passages and resolve independently.",
       teaches="Collapsing them means a verifier cannot tell which passage a claim came from.")
def t_same_source(m):
    r = m.build_context(SAME_SOURCE)
    expect_eq(sorted(r["citations"]), [1, 2], "two chunks, two markers")
    expect_eq(r["citations"][1], r["citations"][2], "both still point at the same document")
    expect_in("[2] Clause B", r["context"])


@check("a chunk with no usable source_id is excluded and recorded",
       "Excluded, not silently dropped — you must be able to explain the gap.",
       teaches="Including it unnumbered lets ungrounded text into the answer; numbering it invents provenance.")
def t_excluded(m):
    r = m.build_context(RAGGED)
    expect_eq(r["chunk_count"], 1, "only the one fully-formed chunk is usable")
    expect(len(r["excluded"]) == 3, f"three chunks should be excluded, got {len(r['excluded'])}")
    for e in r["excluded"]:
        expect("reason" in e, "each exclusion needs a reason")


@check("all-excluded produces empty context and empty citations",
       "The caller must detect 'nothing usable' without parsing the string.")
def t_all_excluded(m):
    r = m.build_context([{"text": "orphan"}, {"text": "another"}])
    expect_eq(r["context"], "", "no usable chunks means no context")
    expect_eq(r["citations"], {}, "and nothing to cite")
