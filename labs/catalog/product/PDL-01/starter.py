"""PDL-01 — agent, workflow, or script."""


def classify(use_case: dict) -> dict:
    """Decide the least autonomous shape that does the job."""
    known = use_case.get("steps_known_upfront", False)
    language = use_case.get("needs_language", False)
    branches = use_case.get("branches_on_tool_output", False)
    hot = use_case.get("hot_path_share", 0.0)
    irreversible = use_case.get("irreversible_actions", False)

    reasons, warnings = [], []

    # TODO 1 — steps known: script if no language is involved, workflow if there is.

    # TODO 2 — steps not known: still only a workflow unless the next step
    #          depends on what the last tool returned. Apparent complexity is
    #          not autonomy.

    # TODO 3 — route the hot path away from the agent when it is worth it.

    # TODO 4 — irreversible actions get a warning, whatever the verdict.

    raise NotImplementedError("implement classify()")
