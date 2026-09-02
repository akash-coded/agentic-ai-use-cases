from harness import check, expect, expect_eq
RESP = {"usage": {"inputTokens": 1200, "outputTokens": 340}, "stopReason": "end_turn"}

@check("all required keys are present")
def t_keys(m):
    r = m.log_record(RESP, "claude-fallback", "claude-primary", "t-1")
    for k in ("trace_id", "model_id", "degraded", "tokens_in", "tokens_out", "stop_reason"): expect(k in r, f"missing {k}")

@check("degraded is True when the fallback answered",
       teaches="This is the field. Without it, fallback share is unmeasurable and quality drops with no signal.")
def t_degraded(m): expect_eq(m.log_record(RESP, "claude-fallback", "claude-primary", "t")["degraded"], True)

@check("degraded is False when the primary answered")
def t_not_degraded(m): expect_eq(m.log_record(RESP, "claude-primary", "claude-primary", "t")["degraded"], False)

@check("token counts come from usage")
def t_tokens(m):
    r = m.log_record(RESP, "p", "p", "t"); expect_eq((r["tokens_in"], r["tokens_out"]), (1200, 340))

@check("a response with no usage does not crash the request",
       teaches="A log call that raises turns a successful answer into a 500. Logging is a boundary; it defaults, it does not throw.")
def t_partial(m):
    r = m.log_record({}, "p", "p", "t"); expect_eq((r["tokens_in"], r["tokens_out"], r["stop_reason"]), (0, 0, ""))
