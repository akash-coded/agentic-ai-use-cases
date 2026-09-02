def classify(use_case):
    # every unanswered question defaults to the LEAST autonomous reading
    known    = use_case.get("steps_known_upfront", True)
    language = use_case.get("needs_language", False)
    branches = use_case.get("branches_on_tool_output", False)
    if known and not language:
        return "script"
    if known or not branches:
        return "workflow"
    return "agent"
