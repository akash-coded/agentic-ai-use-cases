from harness import check, expect, expect_eq
def a(m):
    v = getattr(m, "answer", None); expect(isinstance(v, list), f"answer must be a list, got {v!r}"); return v
@check("the newest message survives", teaches="Whatever else happens, the message being answered is never evicted.")
def t_newest(m): expect("t6" in a(m), "t6 must survive")
@check("the summary is present, at the front", teaches="Over budget means the older turns collapse into one summary message placed first.")
def t_summary(m): v = a(m); expect(v and v[0] == "S", "S should be the first element")
@check("t1–t4 are gone as individual turns", teaches="They were summarised, not kept — only the summary carries them now.")
def t_older(m): expect(not any(x in a(m) for x in ("t1", "t2", "t3", "t4")), "older turns should be inside S, not listed")
@check("no eviction was needed after summarising",
       teaches="80 + 150 + 100 = 330 ≤ 500. Step 3 never fires here — a common slip is evicting t5 anyway.")
def t_no_evict(m): expect("t5" in a(m), "t5 fits and must survive")
@check("exact")
def t_exact(m): expect_eq(a(m), ["S", "t5", "t6"])
