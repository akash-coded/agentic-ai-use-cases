def search_policy(query, corpus, index_ready=True):
    if not index_ready:
        return {"status": "____1____",
                "advice": "The policy corpus was not searched. Do not state what policy says; "
                          "tell the user you could not check and escalate."}
    matches = [p for p in corpus if query.lower() in p["text"].lower()]
    if not matches:
        return {"status": "____2____",
                "searched_count": "____3____",
                "advice": "____4____"}
    return {"status": "ok", "matches": matches}
