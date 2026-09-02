def search_policy(query, corpus, index_ready=True):
    if not index_ready:
        return {"status": "unavailable",
                "advice": "The policy corpus was not searched. Do not state what policy says; "
                          "tell the user you could not check and escalate."}
    matches = [p for p in corpus if query.lower() in p["text"].lower()]
    if not matches:
        return {"status": "no_matches",
                "searched_count": len(corpus),
                "advice": "The corpus was searched and held nothing relevant. Do NOT conclude that no "
                          "policy applies — say you could not find one, and escalate."}
    return {"status": "ok", "matches": matches}
