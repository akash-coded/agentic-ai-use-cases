"""MAS-02 — cost a topology before you build it."""


def estimate_topology(spec: dict) -> dict:
    """Compute total tokens, H×, a breakdown, and warnings."""
    shape = spec.get("shape", "single")
    n = spec.get("specialists", 0)
    base = spec.get("base_context_tokens", 0)
    handoff = spec.get("handoff_context_tokens", 0)
    result = spec.get("result_tokens", 0)
    orch_turns = spec.get("orchestrator_turns", 0)
    rounds = spec.get("rounds", 1)

    # TODO 1 — single is the baseline: total == base, H× == 1.0, no warnings.

    # TODO 2 — delegation: orchestrator context + its reasoning turns
    #          + per-specialist (handoff context + result) + the merge call.
    #          The merge carries EVERY result — that is the term people forget.

    # TODO 3 — critique is delegation with one specialist, repeated `rounds`.
    #          swarm is delegation repeated `rounds`, merged once at the end.

    # TODO 4 — warn above H× 4, and warn when rounds are unbounded on a
    #          shape that can run forever.

    raise NotImplementedError("implement estimate_topology()")
