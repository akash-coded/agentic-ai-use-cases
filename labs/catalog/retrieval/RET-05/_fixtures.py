GOOD = [
    {"text": "Involuntary cancellation by the carrier makes the fare fully refundable.",
     "source_id": "fare-rules#7.3"},
    {"text": "Refunds are processed to the original payment method within 21 days.",
     "source_id": "refund-policy#2.1"},
]

SAME_SOURCE = [
    {"text": "Clause A of the same document.", "source_id": "fare-rules#7"},
    {"text": "Clause B of the same document.", "source_id": "fare-rules#7"},
]

RAGGED = [
    {"text": "Valid passage with provenance.", "source_id": "doc#1"},
    {"text": "Passage with no provenance at all."},
    {"text": "Passage with a blank source.", "source_id": "   "},
    {"text": "", "source_id": "doc#2"},
]


def verify(answer: str, citations: dict, resolve: dict) -> list:
    """Resolve every [n] in an answer back to source text.

    Stands in for a grounding checker. Returns a list of problems.
    """
    import re
    problems = []
    for raw in re.findall(r"\[(\d+)\]", answer):
        n = int(raw)
        if n not in citations:
            problems.append(f"marker [{n}] has no entry in citations")
            continue
        src = citations[n]
        if src not in resolve:
            problems.append(f"marker [{n}] -> {src!r} does not resolve to any source")
    return problems
