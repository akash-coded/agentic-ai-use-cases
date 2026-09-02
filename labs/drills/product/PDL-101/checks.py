from harness import check, expect, expect_eq

@check("a fully described agent is still an agent")
def t_agent(m): expect_eq(m.classify({"steps_known_upfront": False, "needs_language": True, "branches_on_tool_output": True}), "agent")

@check("a fully described workflow is still a workflow")
def t_wf(m): expect_eq(m.classify({"steps_known_upfront": True, "needs_language": True, "branches_on_tool_output": False}), "workflow")

@check("a fully described script is still a script")
def t_script(m): expect_eq(m.classify({"steps_known_upfront": True, "needs_language": False, "branches_on_tool_output": False}), "script")

@check("the bug — an undescribed use case must NOT classify as an agent",
       teaches="An unanswered question should never promote a use case up the ladder. That is how 'we haven't decided' becomes 'it's an agent' between two meetings.")
def t_empty(m): expect(m.classify({}) != "agent", "an empty description defaulted to agent")

@check("…and defaults all the way down to script",
       teaches="Default down, then let reality push it up. Organisations walk up the ladder easily and down it almost never.")
def t_script_default(m): expect_eq(m.classify({}), "script")
