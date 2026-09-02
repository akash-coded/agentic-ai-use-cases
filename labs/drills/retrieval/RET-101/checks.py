from harness import check, expect, expect_eq

EXPECTED = ["c1", "c3", "c4"]

@check("answer is a list of chunk ids")
def t_type(m):
    a = getattr(m, "answer", None)
    expect(isinstance(a, list) and all(isinstance(x, str) for x in a), f"answer must be a list of id strings, got {a!r}")

@check("c2 is skipped — it would blow the budget on its own",
       teaches="400 + 900 > 1000. The packer skips it and keeps looking; it does not stop.")
def t_skip(m):
    expect("c2" not in m.answer, "c2 (900 tokens) cannot fit after c1 (400)")

@check("the packer keeps going after a skip — c3 and c4 get in",
       teaches="`continue` not `break`: a big chunk near the top does not block smaller ones behind it.")
def t_continue(m):
    expect("c3" in m.answer and "c4" in m.answer, "c3 (350) and c4 (200) both fit after c1")

@check("c5 does not fit once c4 is in",
       teaches="400 + 350 + 200 = 950; adding 300 exceeds 1000. Order of arrival decides, not size.")
def t_last(m):
    expect("c5" not in m.answer, "950 + 300 > 1000")

@check("order is rank order, exactly")
def t_exact(m):
    expect_eq(list(m.answer), EXPECTED)
