from harness import check, expect, expect_eq
CORPUS = [{"id": "a", "text": "Carrier cancellations are refundable."}]

@check("a hit is still status ok")
def t_ok(m):
    expect_eq(m.search_policy("carrier", CORPUS)["status"], "ok")

@check("blank 1 — an unsearched corpus has its own status, not a placeholder")
def t_b1(m):
    s = m.search_policy("x", CORPUS, index_ready=False)["status"]
    expect(isinstance(s, str) and s and "____" not in s and s not in ("ok", "no_matches"),
           f"blank 1 should be a distinct 'not searched' status, got {s!r}")

@check("blank 2 — searched-and-empty has a status that differs from blank 1",
       teaches="If these two serialise the same, the model cannot tell 'nothing applies' from 'could not check'.")
def t_b2(m):
    a = m.search_policy("zzz", CORPUS)["status"]; b = m.search_policy("zzz", CORPUS, index_ready=False)["status"]
    expect(a and "____" not in a and a != b and a != "ok", f"blank 2 must be distinct: got {a!r} vs {b!r}")

@check("blank 3 — searched_count is the number of passages searched",
       teaches="It proves the search happened; a count of 0 vs 3 distinguishes an empty corpus from a missing one.")
def t_b3(m):
    expect_eq(m.search_policy("zzz", CORPUS)["searched_count"], 1)
    expect_eq(m.search_policy("zzz", [])["searched_count"], 0)

@check("blank 4 — the advice forbids the wrong conclusion and names a next action",
       teaches="Advice that only reports an absence still leaves the model to interpret it — and it interprets absence as permission.")
def t_b4(m):
    adv = m.search_policy("zzz", CORPUS)["advice"].lower()
    expect("____" not in adv and len(adv) > 30, "blank 4 needs a real sentence")
    expect(any(w in adv for w in ("do not", "don't", "never", "must not")), "advice must forbid the wrong conclusion")
    expect(any(w in adv for w in ("escalate", "ask", "human", "could not", "cannot")), "advice must name the next action")
