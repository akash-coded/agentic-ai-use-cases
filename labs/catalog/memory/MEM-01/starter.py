"""MEM-01 — a buffer that cannot overflow."""


def trim_history(messages: list, budget_tokens: int, summarise, keep_recent: int = 4) -> dict:
    """Bring history under budget with a deliberate eviction policy."""
    total = sum(m.get("tokens", 0) for m in messages)

    # TODO 1 — under budget: return unchanged, and do NOT spend a model call.

    # TODO 2 — over budget: protect the last `keep_recent`, summarise the rest
    #          into ONE message at the front.

    # TODO 3 — still over? drop the oldest of the protected block, one at a time,
    #          counting each drop. Never drop the final message — and note that
    #          keep_recent=0 must not be able to summarise it away either.

    raise NotImplementedError("implement trim_history()")
