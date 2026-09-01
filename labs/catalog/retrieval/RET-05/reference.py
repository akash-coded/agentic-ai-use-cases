"""RET-05 — reference solution.

A chunk with no usable source_id is excluded and the exclusion is recorded:
including it unnumbered lets ungrounded text into the answer, and giving it a
marker invents provenance, which is worse than having none.
"""


def build_context(chunks: list) -> dict:
    context_parts: list[str] = []
    citations: dict[int, str] = {}
    excluded: list[dict] = []
    marker = 0

    for chunk in chunks:
        source_id = chunk.get("source_id")
        text = chunk.get("text")

        if not isinstance(source_id, str) or not source_id.strip():
            excluded.append({"reason": "missing source_id",
                             "text_preview": _preview(text)})
            continue
        if not isinstance(text, str) or not text.strip():
            excluded.append({"reason": "empty text", "text_preview": _preview(text)})
            continue

        marker += 1
        citations[marker] = source_id
        context_parts.append(f"[{marker}] {text.strip()}")

    return {"context": "\n\n".join(context_parts),
            "citations": citations,
            "excluded": excluded,
            "chunk_count": len(context_parts)}


def _preview(text, limit: int = 60) -> str:
    if not isinstance(text, str):
        return ""
    text = text.strip()
    return text if len(text) <= limit else text[:limit] + "…"
