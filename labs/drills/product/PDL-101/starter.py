def classify(use_case):
    known    = use_case.get("steps_known_upfront", False)
    language = use_case.get("needs_language", True)
    branches = use_case.get("branches_on_tool_output", True)
    if known and not language:
        return "script"
    if known or not branches:
        return "workflow"
    return "agent"
