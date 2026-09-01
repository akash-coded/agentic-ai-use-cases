"""RET-05 — citations that survive verification.

Return a context block AND the mapping that lets someone check it.
"""


def build_context(chunks: list) -> dict:
    """Build a citation-labelled context block plus its provenance map.

    Returns:
        {"context": str, "citations": {int: str}, "excluded": [...], "chunk_count": int}
    """
    # TODO 1 — decide (see the brief) what happens to a chunk with no usable
    #          source_id, and record the exclusion rather than dropping it silently.

    # TODO 2 — assign markers 1, 2, 3 … in order of appearance, only to chunks
    #          you are actually including.

    # TODO 3 — build the context string: "[n] text", blank line between chunks.
    #          The source_id must NOT appear anywhere in it.

    # TODO 4 — build the citations map so a verifier can resolve every marker
    #          in the context back to its source. Same source twice = two markers.

    raise NotImplementedError("implement build_context()")
