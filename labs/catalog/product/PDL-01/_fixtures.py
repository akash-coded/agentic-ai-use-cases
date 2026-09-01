def case(name, known, language, branches, hot=0.0, irreversible=False):
    return {"name": name, "steps_known_upfront": known, "needs_language": language,
            "branches_on_tool_output": branches, "hot_path_share": hot,
            "irreversible_actions": irreversible}


NIGHTLY_RECONCILE = case("Nightly ledger reconciliation", True, False, False)
TICKET_SUMMARY = case("Summarise each closed ticket", True, True, False)
REFUND_DESK = case("Refund eligibility desk", False, True, True, hot=0.72)
ONBOARD_PACK = case("Assemble an onboarding pack", False, True, False)
PAYMENT_AGENT = case("Process refunds end to end", False, True, True, hot=0.3, irreversible=True)
