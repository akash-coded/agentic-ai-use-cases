"""MAS-02 — reference solution.

Handoffs carry a summary, not the full context: the reference treats
handoff_context_tokens as an independent input precisely so the caller can
model that choice and see what it buys.
"""


def estimate_topology(spec: dict) -> dict:
    shape = spec.get("shape", "single")
    n = max(0, spec.get("specialists", 0) or 0)
    base = spec.get("base_context_tokens", 0) or 0
    handoff = spec.get("handoff_context_tokens", 0) or 0
    result = spec.get("result_tokens", 0) or 0
    orch_turns = spec.get("orchestrator_turns", 0) or 0
    rounds = spec.get("rounds", 1)
    warnings: list[str] = []

    if shape == "single":
        return {"total_tokens": base, "h_multiple": 1.0,
                "breakdown": {"orchestrator": base, "handoffs": 0, "merge": 0},
                "warnings": []}

    if shape == "critique":
        n = 1
    effective_rounds = rounds if isinstance(rounds, int) and rounds > 0 else 1
    if shape in ("swarm", "critique") and not (isinstance(rounds, int) and rounds > 0):
        warnings.append(
            f"{shape} has no bounded round count — an unbounded {shape} is a budget leak with a diagram. "
            f"Set an explicit cap before building it.")

    orchestrator = base + orch_turns * base
    handoffs = n * (handoff + result) * effective_rounds
    merge = base + n * result

    total = orchestrator + handoffs + merge
    h = round(total / base, 2) if base else 0.0

    if h > 4:
        warnings.append(
            f"H× is {h}, meaning this shape costs {h}x a single agent. "
            f"Be ready to say what the extra {h - 1:.2f}x buys.")

    return {"total_tokens": total, "h_multiple": h,
            "breakdown": {"orchestrator": orchestrator, "handoffs": handoffs, "merge": merge},
            "warnings": warnings}
