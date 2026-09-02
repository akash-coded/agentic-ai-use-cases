def trim_history(messages, budget_tokens, summarise, keep_recent=4):
    older, recent = messages[:-keep_recent], messages[-keep_recent:]
    summary = summarise(older)
    msgs = [summary] + recent
    while sum(m["tokens"] for m in msgs) > budget_tokens:
        msgs.pop()
    return msgs
