"""TOOL-03 · Break phase — can a consumer tell your outcomes apart?

These checks stand in for the agent. They never read prose; they branch on
structure, exactly as real routing code does.
"""
from harness import check, expect, expect_eq
from _fixtures import CORPUS


def _route(result):
    """A plausible downstream router. Returns what the agent would do."""
    status = result.get("status")
    if status == "ok":
        return "answer_from_passages"
    if status == "no_matches":
        return "abstain_not_found"
    if status == "unavailable":
        return "abstain_could_not_check"
    if status == "invalid_query":
        return "ask_user"
    return "unknown"          # a consumer that cannot classify will guess


@check("a downstream router can classify all four outcomes",
       "No branch may fall through to 'unknown'.",
       teaches="If a router cannot classify your return, the model is the router — and it guesses.")
def t_routable(m):
    cases = [(("carrier refundable", CORPUS), "answer_from_passages"),
             (("zeppelin", CORPUS), "abstain_not_found"),
             (("refund", CORPUS, "rebuilding"), "abstain_could_not_check"),
             (("", CORPUS), "ask_user")]
    for args, expected in cases:
        got = _route(m.search_policy(*args))
        expect_eq(got, expected, f"args={args} routed to {got!r}")


@check("no-matches and unavailable serialise differently",
       "Identical JSON means the distinction does not survive the wire.",
       teaches="Whatever you do not encode in the payload, the model cannot recover downstream.")
def t_distinguishable(m):
    import json
    a = json.dumps(m.search_policy("zeppelin", CORPUS), sort_keys=True)
    b = json.dumps(m.search_policy("zeppelin", CORPUS, index_status="down"), sort_keys=True)
    expect(a != b, "searched-and-empty and not-searched produced identical payloads")


@check("the advice is a prohibition, not an assertion about the world",
       "It must tell the model what NOT to conclude.",
       teaches="Advice that merely reports an absence still leaves the model to interpret it — and it interprets absence as permission.")
def t_advice_prohibits(m):
    prohibitions = ("do not", "don't", "never", "must not", "rather than", "instead of")
    for args in [("zeppelin", CORPUS), ("refund", CORPUS, "down")]:
        r = m.search_policy(*args)
        advice = r["advice"].lower()
        expect(any(p in advice for p in prohibitions),
               f"advice for {r['status']!r} states a fact but forbids nothing: {r['advice']!r}\n"
               f"   include an explicit instruction, e.g. \"do not conclude that ...\"")


@check("the advice tells the model where to go instead",
       "Abstention needs a destination or it reads as a dead end.",
       teaches="An agent told only to stop will often answer anyway; told to escalate, it escalates.")
def t_advice_routes(m):
    routes = ("escalate", "ask", "human", "could not", "cannot", "say you")
    for args in [("zeppelin", CORPUS), ("refund", CORPUS, "down"), ("", CORPUS)]:
        r = m.search_policy(*args)
        advice = r["advice"].lower()
        expect(any(x in advice for x in routes),
               f"advice for {r['status']!r} has no next action: {r['advice']!r}")


@check("a corpus entry missing 'text' does not crash the search",
       "Real corpora have holes.",
       teaches="A KeyError inside a tool becomes an error result the model must interpret — avoid it.")
def t_ragged_corpus(m):
    ragged = CORPUS + [{"id": "broken"}]
    r = m.search_policy("refund", ragged)
    expect(isinstance(r, dict) and "status" in r, "a ragged corpus must still produce a status")
