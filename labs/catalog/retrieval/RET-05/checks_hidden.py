from harness import check, expect, expect_eq, expect_not_in
from _fixtures import GOOD, RAGGED


@check("an empty chunk list is handled")
def t_empty(m):
    r = m.build_context([])
    expect_eq(r["context"], "")
    expect_eq(r["citations"], {})
    expect_eq(r["chunk_count"], 0)


@check("chunk_count counts included chunks, not input chunks",
       teaches="Reporting the input count hides how much was dropped.")
def t_count(m):
    expect_eq(m.build_context(RAGGED)["chunk_count"], 1)


@check("citation keys are integers, not strings",
       teaches="A verifier parsing [1] gets an int; string keys make every lookup miss silently.")
def t_int_keys(m):
    r = m.build_context(GOOD)
    for k in r["citations"]:
        expect(isinstance(k, int), f"citation key {k!r} is {type(k).__name__}, expected int")


@check("whitespace around chunk text is trimmed")
def t_trim(m):
    r = m.build_context([{"text": "  padded  ", "source_id": "d#1"}])
    expect_eq(r["context"], "[1] padded", "no stray padding in the prompt")


@check("no marker is assigned to an excluded chunk",
       teaches="A gap in the numbering is fine; a marker with no source is not.")
def t_no_orphan_markers(m):
    import re
    r = m.build_context(RAGGED)
    used = {int(x) for x in re.findall(r"\[(\d+)\]", r["context"])}
    expect_eq(used, set(r["citations"]), "every marker in context must exist in citations, and vice versa")
