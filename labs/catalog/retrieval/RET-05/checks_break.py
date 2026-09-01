"""RET-05 · Break phase — run a verifier over the output.

These checks stand in for a grounding checker: take an answer containing
markers and resolve every one back to source text.
"""
from harness import check, expect, expect_eq
from _fixtures import GOOD, SAME_SOURCE, verify

RESOLVE = {"fare-rules#7.3": "…", "refund-policy#2.1": "…", "fare-rules#7": "…", "doc#1": "…"}


@check("every marker in a model answer resolves to a source",
       "The whole point of the mapping.",
       teaches="An unresolvable marker is citation theatre: it looks grounded and cannot be checked.")
def t_resolves(m):
    r = m.build_context(GOOD)
    answer = "The fare is refundable [1] and the refund takes up to 21 days [2]."
    problems = verify(answer, r["citations"], RESOLVE)
    expect(not problems, "verifier found: " + "; ".join(problems))


@check("a marker the model invented is detectable as unresolvable",
       "Models cite passages that were never in context.",
       teaches="If your map is complete, an invented [3] fails loudly instead of passing review.")
def t_invented_marker(m):
    r = m.build_context(GOOD)
    problems = verify("Also, cancellations are free [3].", r["citations"], RESOLVE)
    expect(problems, "an out-of-range marker must not silently resolve")


@check("markers already present in the chunk text do not corrupt the mapping",
       "Real documents contain '[1]' as footnote markers.",
       teaches="Renumbering or regex-rewriting chunk text makes your citations point at the wrong passage.")
def t_embedded_markers(m):
    chunks = [{"text": "See footnote [1] for the exception.", "source_id": "doc#1"},
              {"text": "The standard rule applies.", "source_id": "doc#2"}]
    r = m.build_context(chunks)
    expect_eq(sorted(r["citations"]), [1, 2], "two chunks still get markers 1 and 2")
    expect_eq(r["citations"][2], "doc#2",
              "the embedded [1] in chunk one must not shift chunk two's provenance")
    expect(r["context"].startswith("[1] See footnote [1]"),
           "the chunk's own text is preserved verbatim, including its footnote marker")


@check("the mapping is injective per marker",
       "One marker, one source. Never a list, never a merge.",
       teaches="A marker pointing at two sources cannot be verified — which one made the claim?")
def t_injective(m):
    r = m.build_context(SAME_SOURCE)
    for k, v in r["citations"].items():
        expect(isinstance(v, str), f"citations[{k}] is {type(v).__name__}; one marker maps to one source id")


@check("excluded chunks never leak into the context",
       "The text you refused to cite must not be in the prompt.",
       teaches="Ungrounded text in context is what the model quotes when it has nothing else.")
def t_no_leak(m):
    chunks = [{"text": "GROUNDED passage.", "source_id": "doc#1"},
              {"text": "UNGROUNDED passage with no provenance."}]
    r = m.build_context(chunks)
    expect("UNGROUNDED" not in r["context"],
           "a chunk you could not cite must not reach the prompt at all")
