from harness import check, expect_eq, expect

def msg(*blocks): return {"role": "assistant", "content": list(blocks)}

@check("returns the text of a single-block message")
def t_single(m):
    expect_eq(m.answer_text(msg({"text": "Refundable."})), "Refundable.")

@check("joins several text blocks in order",
       teaches="The answer is every text block, in order — not the first, not the last.")
def t_join(m):
    r = m.answer_text(msg({"text": "Let me check."},
                          {"toolUse": {"toolUseId": "t", "name": "get_booking", "input": {}}},
                          {"text": "Cancelled by the carrier."}))
    expect_eq(r, "Let me check. Cancelled by the carrier.")

@check("ignores toolUse and other non-text blocks",
       teaches="Models narrate before calling tools; a toolUse block in the middle is normal.")
def t_ignore(m):
    r = m.answer_text(msg({"toolUse": {"toolUseId": "t", "name": "x", "input": {}}}, {"text": "Done."}))
    expect_eq(r, "Done.")

@check("a message with no text returns an empty string, not None",
       teaches="None here becomes an AttributeError two layers up, far from the cause.")
def t_empty(m):
    r = m.answer_text(msg({"toolUse": {"toolUseId": "t", "name": "x", "input": {}}}))
    expect(r == "", f"expected '' for a text-free message, got {r!r}")

@check("strips surrounding whitespace")
def t_strip(m):
    expect_eq(m.answer_text(msg({"text": "  padded  "})), "padded")

@check("does not crash on a message with no content key",
       teaches="Malformed messages arrive from retries and mocks. Read defensively at the boundary.")
def t_missing(m):
    expect_eq(m.answer_text({"role": "assistant"}), "")
