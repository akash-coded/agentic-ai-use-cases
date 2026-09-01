from harness import check, expect, expect_eq, expect_in
from _fixtures import REGISTRY, scripted, always, alternating, TOOL_A, TOOL_B, DONE

START = [{"role": "user", "content": [{"text": "Is XY7Q2M refundable?"}]}]


@check("a converging run answers", "Two tool calls, then the model finishes.")
def t_answers(m):
    r = m.run_loop(START, scripted(TOOL_A, TOOL_B, DONE), REGISTRY, max_steps=6)
    expect_eq(r["outcome"], "answered")
    expect_in("refundable", r["answer"], "the answer text comes from the final assistant message")


@check("steps counts model calls, not tool calls")
def t_steps(m):
    r = m.run_loop(START, scripted(TOOL_A, TOOL_B, DONE), REGISTRY, max_steps=6)
    expect_eq(r["steps"], 3, "three model calls: two tool turns and the answer")


@check("a model that never finishes is stopped by the budget",
       "The cap binds and the run ends.",
       teaches="Without a cap this loop runs until your budget alert fires — or does not.")
def t_exhausted(m):
    varied = scripted(TOOL_A, TOOL_B, TOOL_A, TOOL_B, TOOL_A, TOOL_B, TOOL_A, TOOL_B)
    r = m.run_loop(START, varied, REGISTRY, max_steps=4)
    expect(r["outcome"] in ("exhausted", "stuck"), f"must not answer; got {r['outcome']!r}")
    expect(r["steps"] <= 4, f"never exceed max_steps; made {r['steps']} calls")


@check("an exhausted run does not produce an answer",
       "Stopping is not answering.",
       teaches="A best-effort string here is indistinguishable from a real answer to the caller.")
def t_no_answer_when_stopped(m):
    r = m.run_loop(START, always(TOOL_A), REGISTRY, max_steps=3)
    expect(r["outcome"] != "answered", "a run that never converged did not answer")
    expect(r.get("answer") in (None, ""), "answer must be empty when the loop did not finish")


@check("oscillation is detected and stops the run early",
       "The same call twice in a row is not progress.",
       teaches="A step cap alone turns a runaway into an expensive runaway; detection makes it cheap.")
def t_stuck(m):
    r = m.run_loop(START, always(TOOL_A), REGISTRY, max_steps=10)
    expect_eq(r["outcome"], "stuck", "repeating one call forever is 'stuck', not 'exhausted'")
    expect(r["steps"] <= 3, f"stop on the repeat, not at the cap — used {r['steps']} steps")


@check("a non-answer carries a reason a human can read")
def t_reason(m):
    r = m.run_loop(START, always(TOOL_A), REGISTRY, max_steps=5)
    expect(isinstance(r.get("reason"), str) and len(r["reason"].strip()) > 20,
           "reason should be a sentence, not a code")
