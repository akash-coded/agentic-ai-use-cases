from harness import check, expect, expect_eq, expect_in
from _fixtures import CORPUS


@check("a hit returns status ok with the matching passages")
def t_ok(m):
    r = m.search_policy("carrier refundable", CORPUS)
    expect_eq(r["status"], "ok")
    expect_eq([x["id"] for x in r["matches"]], ["fr-7.3"], "only the passage with every term matches")


@check("matches preserve corpus order")
def t_order(m):
    r = m.search_policy("refund", [{"id": "b", "text": "refund b"}, {"id": "a", "text": "refund a"}])
    expect_eq([x["id"] for x in r["matches"]], ["b", "a"], "do not re-sort the corpus")


@check("finding nothing is status no_matches — never a bare empty",
       "The corpus was searched and held nothing. That is a result.",
       teaches="Returning [] here is how 'I found nothing' becomes 'nothing applies'.")
def t_no_matches(m):
    r = m.search_policy("zeppelin insurance", CORPUS)
    expect(isinstance(r, dict), "always return a dict with a status, never a bare list")
    expect_eq(r["status"], "no_matches")
    expect_eq(r["searched_count"], 3, "say how much was searched — it proves the search happened")


@check("an unready index is unavailable, not no_matches",
       "One means searched-and-empty, the other means not searched.",
       teaches="Collapsing these two is the bug: the model cannot recover a distinction you did not encode.")
def t_unavailable(m):
    r = m.search_policy("refund", CORPUS, index_status="rebuilding")
    expect_eq(r["status"], "unavailable")
    expect(r["status"] != "no_matches", "an unsearched corpus is not an empty corpus")


@check("every non-ok result carries advice in the imperative",
       "The field that stops the model inventing a conclusion.")
def t_advice(m):
    for r in (m.search_policy("nothing matches here", CORPUS),
              m.search_policy("refund", CORPUS, index_status="down"),
              m.search_policy("   ", CORPUS)):
        expect("advice" in r, f"{r['status']} needs advice telling the model what to do")
        expect(len(r["advice"].strip()) > 20, "advice should be a usable sentence")


@check("an empty query is rejected, not searched")
def t_invalid(m):
    expect_eq(m.search_policy("", CORPUS)["status"], "invalid_query")
    expect_eq(m.search_policy("   ", CORPUS)["status"], "invalid_query")
