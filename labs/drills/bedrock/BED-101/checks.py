from harness import check, expect, expect_eq
def a(m):
    v = getattr(m, "answer", None); expect(isinstance(v, list), f"answer must be a list, got {v!r}"); return v
@check("six turns: a request, two tool round trips, an answer",
       teaches="Each tool round trip is TWO messages — the model's request and the tool's result. Two tools = four, plus the question and the answer.")
def t_len(m): expect_eq(len(a(m)), 6, f"expected 6 roles, got {len(a(m))}")
@check("roles alternate — no two 'user' turns in a row",
       teaches="['user','user'] is the signature of the skipped assistant message, and the API rejects it.")
def t_alt(m):
    v = a(m); expect(all(v[i] != v[i+1] for i in range(len(v)-1)), f"roles must alternate: {v}")
@check("the tool results are 'user' turns, not 'assistant'",
       teaches="Roles say which side the content came FROM as the model sees it. A tool result is input to the model, so it is 'user'.")
def t_results(m):
    v = a(m); expect(len(v) > 2 and v[2] == "user", "the first tool result is the third message and it is a user turn")
@check("exact sequence")
def t_exact(m): expect_eq(a(m), ["user", "assistant", "user", "assistant", "user", "assistant"])
