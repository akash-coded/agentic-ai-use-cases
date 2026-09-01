def msg(role, text, tokens):
    return {"role": role, "content": [{"text": text}], "tokens": tokens}


def history(n=10, tokens=100):
    return [msg("user" if i % 2 == 0 else "assistant", f"turn {i}", tokens) for i in range(n)]


def make_summariser(tokens=80):
    calls = {"n": 0}

    def summarise(msgs):
        calls["n"] += 1
        return {"role": "user", "content": [{"text": f"summary of {len(msgs)} turns"}],
                "tokens": tokens, "is_summary": True}
    summarise.calls = calls
    return summarise
