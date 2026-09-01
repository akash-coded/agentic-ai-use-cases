# Authoring a lab

A lab is seven files in `labs/catalog/<track>/<ID>/`. `labctl verify` will not let a broken one ship, so
write the reference first and let the gate tell you when you are done.

---

## The seven files

```
catalog/<track>/<ID>/
├── lab.toml           metadata: difficulty, prerequisites, PDLC stage, frameworks
├── README.md          the brief — Learn / Apply / Break
├── starter.py         real TODOs. It MUST fail the public checks
├── reference.py       your solution. It MUST pass all three phases
├── checks_public.py   visible on `run`
├── checks_hidden.py   revealed on `submit`
├── checks_break.py    the Break phase (optional, but a lab without one is usually shallow)
└── _fixtures.py       optional shared test data
```

## The three phases, and what belongs in each

**Learn** — a mental model, a diagram, and **one decision with the answer withheld**. If you find yourself
writing "you should do X", you are writing Apply. Give the options and their consequences; let the checks
enforce the outcome, not the brief.

**Apply** — a spec precise enough to implement, with the *reason* for each requirement. "Return a dict"
is a requirement. "Return a dict, because a string cannot carry the mapping a verifier needs" is a lab.

**Break** — failures from real systems, not invented difficulty. The bar: *has this ended a real run?*
`SystemExit` from a library. A chunk larger than the whole budget. A footnote `[1]` inside retrieved text.
If you cannot name where you have seen it, it probably does not belong.

## Writing checks

```python
from harness import check, expect, expect_eq

@check("an unknown tool becomes an error result, not an exception",
       "The loop must survive the model inventing a tool.",
       teaches="Raising here turns a recoverable turn into an outage.")
def t_unknown(m):
    r = m.dispatch({"toolUseId": "t", "name": "nope", "input": {}}, {})["toolResult"]
    expect_eq(r["status"], "error", "an unknown tool is an error result")
```

- **Name the behaviour, not the function.** "carries the toolUseId through unchanged", not "test_id".
- **`teaches` is for the checks that matter.** It prints only on failure, and it is the sentence the
  learner remembers.
- **Assertion messages state the expectation.** `expect_eq(x, y, "toolUseId must be echoed exactly")`.
- **Never require a network call.** Every lab must run offline and deterministically, or it cannot run in
  CI. Script the model as a fixture.

## The two rules `verify` enforces

1. **`reference.py` passes public, hidden and Break.** If it does not, either your reference is wrong or
   your check is. Both happen — four of these labs' references were fixed this way.
2. **`starter.py` fails the public checks.** A starter that passes has TODOs that do not need doing.

```bash
python labs/runner/labctl.py verify           # both rules, every lab
python labs/runner/labctl.py run <ID> --reference
python labs/runner/labctl.py index --write    # refresh the catalog table
```

## Difficulty

By judgement withheld, not lines of code:

| | The lab supplies | The learner supplies |
| --- | --- | --- |
| `easy` | The rule and the shape | The implementation |
| `medium` | Requirements and trade-offs | The decision and its consequences |
| `hard` | The situation | Requirements, decision, and evidence |

## Wiring it in

- Set `prerequisites` to labs whose ideas you assume. The DAG must stay acyclic; `verify` checks.
- Set `[pdlc]` — the stage and the artefact fragment the decision produces. This is what keeps the
  [PDLC thread](PATHWAY.md#the-pdlc-thread) real rather than decorative.
- Set `[frameworks].read` to the [field guide](../cheatsheets/) pages the lab depends on, and link them
  from the brief and the solution.
- Link the [module](../modules/) that teaches the concept.
- Run `labctl index --write` and commit the refreshed table.
- Add a row to [PATHWAY.md](PATHWAY.md) and mark it ✅.

## SOLUTION.md

Not a code dump — the code is in `reference.py`. Write the *reasoning*: why the decision went the way it
did, what the tempting wrong answer costs, and which single line most people get wrong. Assume it is read
after a failed attempt, by someone who wants to know whether they were close.

---

[⬅️ L.A.B. Simulator](README.md) · [🗺️ Pathway](PATHWAY.md) · [🤝 CONTRIBUTING](../CONTRIBUTING.md)
