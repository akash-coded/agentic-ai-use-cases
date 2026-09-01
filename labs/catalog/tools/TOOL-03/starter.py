"""TOOL-03 — fail honestly.

Three outcomes must be unmistakable: found something, found nothing, could not look.
"""


def search_policy(query: str, corpus: list, index_status: str = "ready") -> dict:
    """Search policy passages and return a result the model cannot misread.

    Returns a dict whose "status" is one of:
        "ok" | "no_matches" | "unavailable" | "invalid_query"
    """
    # TODO 1 — an empty or whitespace-only query is not a search. Say so.

    # TODO 2 — if the index is not ready, the corpus was NOT searched. That is
    #          categorically different from searching and finding nothing.

    # TODO 3 — do the search: every term in the query must appear in the passage,
    #          case-insensitively. Preserve corpus order.

    # TODO 4 — no matches is a real, valid result. Return it with enough context
    #          that the model knows the corpus WAS searched, plus advice telling it
    #          what NOT to conclude.

    raise NotImplementedError("implement search_policy()")
