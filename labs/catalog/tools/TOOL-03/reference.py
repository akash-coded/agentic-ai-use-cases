"""TOOL-03 — reference solution.

Every return carries an explicit status and, when it is not "ok", advice in the
imperative. The advice field exists to remove a decision from the model that it
reliably gets wrong: what an absence means.
"""


def search_policy(query: str, corpus: list, index_status: str = "ready") -> dict:
    if not query or not query.strip():
        return {"status": "invalid_query",
                "advice": "The query was empty. Ask the user what they want checked; "
                          "do not answer from memory."}

    if index_status != "ready":
        return {"status": "unavailable",
                "reason": f"policy index is {index_status!r}, not ready",
                "query": query,
                "advice": "The policy corpus was NOT searched. Do not state what policy says. "
                          "Tell the user you could not check and escalate."}

    terms = [t.lower() for t in query.split()]
    matches = [{"id": p.get("id"), "text": p.get("text", "")}
               for p in corpus
               if all(t in p.get("text", "").lower() for t in terms)]

    if not matches:
        return {"status": "no_matches",
                "query": query,
                "searched_count": len(corpus),
                "advice": "The corpus was searched and held nothing relevant. Do NOT conclude that no "
                          "policy applies — say you could not find one, and escalate."}

    return {"status": "ok", "query": query, "matches": matches, "searched_count": len(corpus)}
