def trim_history(messages, budget_tokens, summarise, keep_recent=4):
    msgs = list(messages)
    if sum(m["tokens"] for m in msgs) <= budget_tokens:
        return msgs                                   # nothing to do, no model call
    keep = max(1, min(keep_recent, len(msgs)))        # the newest message is always protected
    older, recent = msgs[:len(msgs) - keep], msgs[len(msgs) - keep:]
    if older:
        msgs = [summarise(older)] + recent            # exactly one call, only when over budget
    while sum(m["tokens"] for m in msgs) > budget_tokens and len(msgs) > 1:
        msgs.pop(0)                                   # evict the OLDEST, never the newest
    return msgs
