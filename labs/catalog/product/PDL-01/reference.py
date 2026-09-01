"""PDL-01 — reference solution.

Tie-breaker: default DOWN. Building the simpler shape and watching it fail is
cheap and produces evidence; building the agent first is expensive and, once a
team has one, very hard to walk back.
"""


def classify(use_case: dict) -> dict:
    known = use_case.get("steps_known_upfront", False)
    language = use_case.get("needs_language", False)
    branches = use_case.get("branches_on_tool_output", False)
    hot = use_case.get("hot_path_share", 0.0) or 0.0
    irreversible = use_case.get("irreversible_actions", False)

    reasons, warnings = [], []

    if known:
        if not language:
            verdict, rung = "script", "R0"
            reasons.append("The steps are known in advance and nothing needs natural language, "
                           "so no model is required at all.")
        else:
            verdict, rung = "workflow", "R2"
            reasons.append("The steps are known in advance; the model is used inside fixed steps "
                           "rather than choosing them.")
    elif not branches:
        verdict, rung = "workflow", "R2"
        reasons.append("The sequence varies, but nothing branches on what a tool returned — "
                       "that is a parameterised workflow, not autonomy.")
    else:
        verdict, rung = "agent", "R3"
        reasons.append("The next step depends on what the previous tool returned, so the control "
                       "flow can only be decided at runtime.")

    route_hot_path = verdict == "agent" and hot >= 0.6
    if route_hot_path:
        reasons.append(f"{hot:.0%} of traffic follows one common path; route that deterministically "
                       f"and reserve the agent for the remainder.")

    if irreversible:
        warnings.append("This use case has irreversible actions. The agent may recommend, but a human "
                        "must commit — enforce it in permissions, not in the prompt.")
    if verdict == "agent" and not irreversible:
        warnings.append("Confirm every tool is read-only before granting the agent autonomy.")

    return {"verdict": verdict, "rung": rung, "reasons": reasons,
            "route_hot_path": route_hot_path, "warnings": warnings}
