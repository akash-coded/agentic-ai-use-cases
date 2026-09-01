"""MEM-01 — reference solution.

Eviction policy: the newest message is never evicted; older-but-recent messages
are dropped only after summarisation has already failed to fit; everything older
is summarised. Every drop is counted so the caller can see what it cost.
"""


def trim_history(messages: list, budget_tokens: int, summarise, keep_recent: int = 4) -> dict:
    msgs = list(messages)
    total = sum(m.get("tokens", 0) for m in msgs)

    if total <= budget_tokens:
        return {"messages": msgs, "evicted": 0, "summarised": False, "tokens": total}

    evicted = 0
    summarised = False

    # the newest message is protected regardless of keep_recent: a config value
    # must not be able to summarise away the turn we are answering
    keep = max(1, min(keep_recent, len(msgs))) if msgs else 0
    older = msgs[:len(msgs) - keep]
    recent = msgs[len(msgs) - keep:]
    if older:
        msgs = [summarise(older)] + recent
        summarised = True
        evicted += len(older)

    total = sum(m.get("tokens", 0) for m in msgs)
    # summarising is not guaranteed to be enough
    while total > budget_tokens and len(msgs) > 1:
        msgs.pop(0)                      # oldest first; never the final message
        evicted += 1
        total = sum(m.get("tokens", 0) for m in msgs)

    return {"messages": msgs, "evicted": evicted, "summarised": summarised, "tokens": total}
