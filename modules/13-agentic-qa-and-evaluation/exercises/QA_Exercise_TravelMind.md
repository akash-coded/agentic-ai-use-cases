# Hands-on QA Lab: test TravelMind end to end

You are the QA engineer on TravelMind, an airline booking-exception agent. A
teammate wants to ship a prompt change. Your job is to prove the build is safe
before it reaches customers, using the four QA disciplines, and to produce a
sign-off you would stand behind.

You will write the QA yourself. By the end you will have run the full loop:
tests, evaluation, observability, and a gate that blocks a bad build.

| | |
|---|---|
| Time | about 90 minutes |
| You need | Python 3.10+, the kit files `travelmind_agent.py` and `config.py`, AWS credentials for the model stages |
| Two tracks | **Local** (non-AgentCore) and **AgentCore**. Labs 1 to 4 and 6 are identical in both. Lab 5 (observability) is where they differ, and both paths are spelled out. |
| Answer key | The kit you already have. Every reveal matches it. Try first, then check. |

> If you do not have the kit, a minimal stand-in agent is in the reveal at the
> end of "The agent under test". Everything else still works.

---

## The agent under test

TravelMind has three tools, all plain functions that the agent wraps with
`tool(...)` at wiring time:

| Tool | Returns |
|------|---------|
| `lookup_booking(pnr)` | `{pnr, status, flight, date}`; `status` is one of CONFIRMED, CANCELLED, DELAYED, NOT_FOUND |
| `get_disruption_reason(pnr)` | `{pnr, reason, detail}`; `reason` is None for a healthy booking |
| `get_rebooking_options(pnr)` | a list of `{flight, dep}`; empty list means none |

Fixed test data: `JX48Q2` is CANCELLED (weather), `AB12CD` is CONFIRMED,
`DL99XY` is DELAYED (crew), anything else is NOT_FOUND.

**Run it (Local track):**

```bash
python -m venv .venv && source .venv/bin/activate
aws configure                       # workshop creds; production uses an IAM role
pip install strands-agents boto3 pytest ragas langchain-aws
python -c "from travelmind_agent import get_agent; print(get_agent()('Status of PNR JX48Q2?'))"
```

**Run it (AgentCore track):** wrap the same agent as a Runtime entrypoint and
invoke it. The agent logic does not change; only how it is hosted does.

<details><summary>AgentCore entrypoint and deploy (click to expand)</summary>

```python
# travelmind_runtime.py
from bedrock_agentcore import BedrockAgentCoreApp
from travelmind_agent import build_agent

app = BedrockAgentCoreApp()
agent = build_agent()

@app.entrypoint
def invoke(payload):
    # payload is the JSON request body; the entrypoint is also callable directly
    # in tests, e.g. invoke({"prompt": "..."})
    return str(agent(payload.get("prompt", "")))

if __name__ == "__main__":
    app.run()      # serves POST /invocations and GET /ping on port 8080
```

```bash
agentcore configure -e travelmind_runtime.py
agentcore launch
agentcore invoke '{"prompt": "Status of PNR JX48Q2?"}'
```
</details>

<details><summary>No kit? Minimal stand-in agent (click to expand)</summary>

Save this as `travelmind_agent.py` and you can do every lab.

```python
from strands import Agent, tool
from strands.models import BedrockModel

_DB = {"JX48Q2": ("CANCELLED", "AI-302", "weather"),
       "AB12CD": ("CONFIRMED", "6E-220", None),
       "DL99XY": ("DELAYED", "AI-415", "crew")}
_OPTS = {"JX48Q2": [{"flight": "AI-318", "dep": "18:40"}, {"flight": "6E-552", "dep": "21:15"}]}

def lookup_booking(pnr: str) -> dict:
    """Look up a booking by PNR."""
    k = pnr.strip().upper().replace(" ", "")
    if k not in _DB: return {"pnr": k, "status": "NOT_FOUND"}
    s, f, _ = _DB[k]; return {"pnr": k, "status": s, "flight": f}

def get_rebooking_options(pnr: str) -> list:
    """Alternative flights for a disrupted booking."""
    return list(_OPTS.get(pnr.strip().upper().replace(" ", ""), []))

SYSTEM = ("You are TravelMind. Always look up the PNR before answering. "
          "Offer rebooking options when disrupted. Never invent a PNR or flight.")

def build_agent():
    m = BedrockModel(model_id="us.anthropic.claude-haiku-4-5-20251001-v1:0", region_name="us-east-1")
    return Agent(model=m, tools=[tool(lookup_booking), tool(get_rebooking_options)], system_prompt=SYSTEM)

_a = None
def get_agent():
    global _a
    if _a is None: _a = build_agent()
    return _a
```
</details>

---

## Key concepts you will use

Four ideas show up in every lab. Learn the vocabulary once.

**Golden set.** A fixed list of test inputs, each with **acceptance criteria
instead of an exact expected answer**. An agent has no single right reply, so you
cannot diff against a fixed string. You check properties: the reply must mention
"cancelled", must not mention a flight number for a bad PNR, and so on. The
golden set is your regression baseline; you re-run it on every change.

**Facts.** The ground truth you hand an LLM judge so it is not guessing. If you
ask a model to grade whether a reply is correct, the model needs to know what
correct is. The facts are the real tool outputs ("JX48Q2 is CANCELLED due to
weather; options AI-318, 6E-552"). A judge without facts grades vibes.

**LLM-as-judge.** A stronger model scores a reply against a short rubric, for the
things a substring cannot check: completeness, tone, no invention. It is triage,
not an oracle. You keep it honest by grounding it with facts, constraining it to
JSON output, and calibrating it against human labels.

**The stages of QA.** QA is not one step at the end. It threads the lifecycle:

| Stage | Lab | What QA does here |
|-------|-----|-------------------|
| Build | 1 | Tool-contract tests, deterministic |
| Integrate | 2 | Behaviour and trajectory tests, real model |
| Evaluate | 3, 4 | Golden set scored by deterministic checks and a judge |
| Operate | 5 | Read traces, treat cost as a quality signal |
| Deploy | 6 | Gate on thresholds, produce a sign-off |

---

## Lab 1 - Tool-contract tests (deterministic, no AWS)

**Goal.** Catch a broken tool before the agent ever runs.

**Concept.** A contract is a tool's promised **shape** (which keys) and **range**
(which values). The agent is built on that promise. These tests run with no model
and no cloud, so they go on every commit.

**Your task.** Create `test_contracts.py` with assertions that:
1. `lookup_booking("JX48Q2")` returns the keys pnr, status, flight, date.
2. status is always one of the four allowed values, including for a bad PNR.
3. a bad PNR returns NOT_FOUND and does **not** invent a flight.
4. `get_rebooking_options` returns a list whose items have flight and dep.

<details><summary>Hint</summary>

```python
import pytest
from travelmind_agent import lookup_booking, get_rebooking_options

def test_shape():
    out = lookup_booking("JX48Q2")
    assert {"pnr", "status", "flight"} <= set(out)   # subset check

def test_bad_pnr_not_invented():
    out = lookup_booking("ZZZZZZ")
    assert out["status"] == "NOT_FOUND"
    assert "flight" not in out                        # nothing fabricated
```
Run with `pytest test_contracts.py -q`.
</details>

**Done when.** `pytest test_contracts.py` is green, with no AWS configured.

<details><summary>Reveal a fuller solution</summary>

```python
import pytest
from travelmind_agent import lookup_booking, get_rebooking_options

VALID = {"CONFIRMED", "CANCELLED", "DELAYED", "NOT_FOUND"}

def test_lookup_shape():
    out = lookup_booking("JX48Q2")
    assert {"pnr", "status", "flight"} <= set(out)
    assert out["pnr"] == "JX48Q2"

def test_normalises_input():
    assert lookup_booking("  jx 48 q2 ")["status"] == "CANCELLED"

@pytest.mark.parametrize("pnr", ["JX48Q2", "AB12CD", "DL99XY", "ZZZZZZ"])
def test_status_is_known(pnr):
    assert lookup_booking(pnr)["status"] in VALID

def test_bad_pnr_not_invented():
    out = lookup_booking("ZZZZZZ")
    assert out["status"] == "NOT_FOUND"
    assert "flight" not in out

def test_options_shape():
    for o in get_rebooking_options("JX48Q2"):
        assert {"flight", "dep"} <= set(o)
```
</details>

---

## Lab 2 - Behaviour and trajectory tests (real model)

**Goal.** Check what the agent decides, not what it says word for word.

**Concept.** The model is non-deterministic, so the wording changes run to run.
Never assert an exact string. Assert observable, stable properties: which tools
were called (the trajectory) and the end state. To see the tools, wrap each one
in a **spy** that records its name. These are integration tests; they need a real
model and run on a prompt or model change, not on every commit.

**Your task.** Spy the tools, run the agent on a rebooking request, and assert:
- `lookup_booking` was called (it checked before acting), and
- the reply offered a real option (AI-318 or 6E-552) or honestly said none.

Run it on three seeds and require the invariant to hold every time.

<details><summary>Hint</summary>

```python
calls = []
def spy(fn):
    def w(*a, **k): calls.append(fn.__name__); return fn(*a, **k)
    w.__name__, w.__doc__ = fn.__name__, fn.__doc__   # Strands reads these
    return w

from strands import Agent, tool
from strands.models import BedrockModel
from travelmind_agent import lookup_booking, get_rebooking_options, SYSTEM_PROMPT

agent = Agent(model=BedrockModel(model_id="us.anthropic.claude-haiku-4-5-20251001-v1:0",
              region_name="us-east-1"),
              tools=[tool(spy(lookup_booking)), tool(spy(get_rebooking_options))],
              system_prompt=SYSTEM_PROMPT)
```
</details>

**Done when.** The test passes on all three seeds. If it flakes, you are probably
asserting wording somewhere; assert a property instead.

<details><summary>Reveal</summary>

```python
import pytest

@pytest.mark.parametrize("seed", range(3))
def test_rebooks_or_says_none(seed):
    calls.clear()
    out = str(agent("My flight on PNR JX48Q2 was cancelled. Options?")).lower()
    assert "lookup_booking" in calls                       # trajectory invariant
    offered = ("ai-318" in out) or ("6e-552" in out)
    honest_none = "no option" in out or "no alternative" in out
    assert offered or honest_none                          # end-state invariant, every seed

def test_bad_pnr_never_invented():
    out = str(agent("Rebook PNR ZZZZZZ")).lower()
    assert "ai-3" not in out
```

Multi-agent note: if a supervisor routes to specialist sub-agents, spy the
specialists the same way and assert **reachability and end state, not order**.
A Graph has fixed edges so you can assert a node completed; a Swarm decides
hand-offs at runtime so order is not guaranteed.
</details>

---

## Lab 3 - Golden set and deterministic evaluation

**Goal.** Turn "seems fine" into a number you can compare.

**Concept.** Write a **golden set**: inputs with criteria, not answers. Three
rule types cover most cases:

- `must`: every phrase must appear.
- `any_of`: at least one phrase must appear (for several acceptable phrasings).
- `must_not`: no phrase may appear (this catches an invented flight).

**Your task.**
1. Write three golden cases as JSON lines in `golden_set.jsonl`: a disruption
   question, a rebooking question, and a bad-PNR safety case.
2. Write a **pure** checker `substring_check(reply, case)` that applies the rules.
   Pure means it takes a string and a case and returns a boolean; it does not call
   the agent. The agent call is the part that needs AWS; keep it separate.
3. Run the agent over the cases and print the pass rate.

<details><summary>Hint</summary>

```jsonl
{"id": "g1", "input": "Is PNR JX48Q2 affected?", "must": ["cancelled", "weather"], "must_not": ["confirmed"]}
{"id": "g2", "input": "Rebooking options for JX48Q2?", "any_of": ["ai-318", "6e-552"]}
{"id": "g3", "input": "Rebook PNR ZZZZZZ.", "any_of": ["not found", "could not find"], "must_not": ["ai-3"]}
```

```python
def substring_check(reply, case):
    t = reply.lower()
    if not all(p.lower() in t for p in case.get("must", [])): return False
    a = case.get("any_of", [])
    if a and not any(p.lower() in t for p in a): return False
    if any(p.lower() in t for p in case.get("must_not", [])): return False
    return True
```
</details>

**Done when.** You can print something like `pass rate 100% (3/3)`. Then break a
case on purpose (change a `must` to a word the agent will not say) and watch the
rate drop. That drop is the regression signal.

<details><summary>Reveal the run loop</summary>

```python
import json
from travelmind_agent import get_agent

cases = [json.loads(l) for l in open("golden_set.jsonl") if l.strip()]
agent = get_agent()

def run_case(c):
    reply = str(agent(c["input"]))
    return substring_check(reply, c)

passed = sum(run_case(c) for c in cases)
print(f"pass rate {passed/len(cases):.0%} ({passed}/{len(cases)})")
```
</details>

---

## Lab 4 - LLM-as-judge with facts

**Goal.** Grade what a substring cannot: did the reply explain the cause **and**
offer an option, without inventing anything.

**Concept.** Ask a **stronger** model to score the reply 1 to 5 against a rubric.
Ground it with **facts** so it is not guessing. Constrain it to JSON so you can
parse a number. Watch three biases:

| Bias | What it is | Counter |
|------|------------|---------|
| Position | favours whichever answer is first | for pairwise, score both orders and average |
| Verbosity | rewards longer answers | cap length in the rubric |
| Self-preference | flatters its own style | use a different model family as judge |

**Your task.** Write `judge(question, reply, facts, focus)` that returns
`{"score": int, "reason": str}`, then grade this case:

- input: "My flight on PNR JX48Q2 was cancelled. Help me."
- facts: "JX48Q2 is CANCELLED due to weather. Options: AI-318 18:40, 6E-552 21:15."
- focus: "explains the cause AND offers at least one real option"

<details><summary>Hint</summary>

```python
import json
from strands import Agent
from strands.models import BedrockModel

def judge(question, reply, facts, focus):
    rubric = ("You are a strict QA grader. Score the REPLY 1 to 5 on correctness "
              "vs FACTS, completeness, and no invented PNR/flight/policy. "
              f"Focus on: {focus}. "
              'Return ONLY JSON: {"score": <1-5>, "reason": "<one line>"}.')
    g = Agent(model=BedrockModel(model_id="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
              region_name="us-east-1"), system_prompt=rubric)
    raw = str(g(f"QUESTION: {question}\nFACTS: {facts}\nREPLY: {reply}"))
    try: return json.loads(raw)
    except json.JSONDecodeError: return {"score": 0, "reason": "non-JSON output"}
```
</details>

**Done when.** A good reply scores 4 or 5; a reply you deliberately cripple (force
the agent to skip the options) scores lower. The judge moved with quality.

<details><summary>Reveal: grade a case, plus the third grader (RAGAS)</summary>

```python
from travelmind_agent import get_agent
q = "My flight on PNR JX48Q2 was cancelled. Help me."
facts = "JX48Q2 is CANCELLED due to weather. Options: AI-318 18:40, 6E-552 21:15."
reply = str(get_agent()(q))
print(judge(q, reply, facts, "explains the cause AND offers at least one real option"))
```

For answers grounded in a knowledge base (a refund policy, say), use **RAGAS
faithfulness**: the fraction of claims in the reply the retrieved context
supports. It needs the retrieved chunks, so it does not apply to the pure
booking flow.

```python
from ragas.dataset_schema import SingleTurnSample
from ragas.metrics import Faithfulness
from ragas.llms import LangchainLLMWrapper
from langchain_aws import ChatBedrock

evaluator = LangchainLLMWrapper(ChatBedrock(
    model_id="us.anthropic.claude-sonnet-4-5-20250929-v1:0", region_name="us-east-1"))

sample = SingleTurnSample(
    user_input="Refund window for a weather cancellation?",
    response=agent_reply,
    retrieved_contexts=["Weather cancellations get a full refund within 14 days of departure."])

# in a notebook cell you can await directly:
score = await Faithfulness(llm=evaluator).single_turn_ascore(sample)   # 0..1
```
</details>

---

## Lab 5 - Observability and cost

**Goal.** Localise a failing run to one span, and read cost as a quality signal.
This is the lab where the two tracks differ.

**Concept.** You cannot step-debug a non-deterministic agent. You read **traces**.
The hierarchy is **Session -> Trace -> Span**: a session holds traces, a trace
holds spans, and each span is one model call or one tool call with its input,
output, latency, and tokens. Spans land in the CloudWatch Logs group `aws/spans`.
A cost spike is usually retries or a loop, which is a quality bug, so you alarm on
cost the way you alarm on errors.

### Setup differs by track

| | **Local (non-AgentCore)** | **AgentCore** |
|---|---|---|
| Instrument | add `aws-opentelemetry-distro` to requirements, launch with `opentelemetry-instrument python -m travelmind_agent` | automatic on Runtime, nothing to do |
| Enable traces | CloudWatch Console -> Application Signals -> Transaction Search -> enable (once per account and Region) | same, enable Transaction Search once |
| Where spans go | `aws/spans` | `aws/spans` |

> The Transaction Search step is the most common reason a fresh account shows
> empty dashboards. Do it first, in both tracks.

**Your task.**
1. Enable observability for your track and run the agent a few times.
2. With CloudWatch Logs Insights, query `aws/spans` for failed tool spans.
3. Compute the cost of one run from its token counts.

<details><summary>Hint: the query and the cost helper</summary>

Logs Insights query (run against the `aws/spans` log group):

```
fields @timestamp, name, durationNano, status.code
| filter name like /tool/
| filter status.code = "ERROR"
| sort @timestamp desc
| limit 20
```

Run a broad `fields @message | limit 5` first to confirm your real field names;
paths follow the OpenTelemetry GenAI conventions and can vary by setup.

Cost from tokens (prices are USD per 1M tokens):

```python
PRICES = {"haiku-4.5": (1.00, 5.00), "sonnet-4": (3.00, 15.00)}
def run_cost(in_tok, out_tok, key="haiku-4.5"):
    pin, pout = PRICES[key]
    return in_tok/1e6*pin + out_tok/1e6*pout
print(round(run_cost(4200, 380), 5), "USD per resolution")
```
Token counts are on the span, and locally on `result.metrics` from a Strands run.
</details>

**Done when.** You can point at a specific tool span and say "this is where it
failed", and you can state the cost of a typical resolution in dollars.

<details><summary>Reveal: query from Python and find the failing span</summary>

```python
import boto3, time
logs = boto3.client("logs", region_name="us-east-1")

def insights(query, minutes=60, group="aws/spans"):
    end = int(time.time()); start = end - minutes*60
    qid = logs.start_query(logGroupName=group, startTime=start, endTime=end, queryString=query)["queryId"]
    while True:
        r = logs.get_query_results(queryId=qid)
        if r["status"] in ("Complete", "Failed", "Cancelled"): break
        time.sleep(1)
    return [{c["field"]: c["value"] for c in row} for row in r["results"]]

rows = insights('fields @timestamp, name, status.code | filter sessionId = "sess-8841" | sort @timestamp asc')
failing = next((r for r in rows if str(r.get("status.code","")).upper().endswith("ERROR")), {})
print("failing span:", failing)
```

The classic finding: a tool span with status ERROR sitting next to a normal final
model span. The tool failed, the model answered anyway. Fix by returning tool
errors to the model and adding a post-condition check before claiming success.
</details>

---

## Lab 6 - Quality gate and sign-off (the capstone)

**Goal.** Compose Labs 1 to 5 into one decision: promote or block. Then run the
real scenario that started this lab.

**Concept.** A gate reads the numbers the earlier stages produced, checks each
against an agreed threshold, and **exits non-zero to block a deploy** if any bar
is missed. A gate that only warns is not a gate. It also writes a sign-off: the
artifact proving a specific build cleared every bar.

The bars to start with (agree them with the client):

| Bar | Threshold |
|-----|-----------|
| Tool and behaviour tests | 0 failures |
| Eval pass rate | at least 90% |
| Cost per resolution | at most $0.02 |
| p95 latency | at most 4000 ms |
| Safety and PII | 100% |

**Your task.**
1. Write `quality_gate.py` that loads `test_report.json`, `eval_report.json`, and
   `cost_latency.json`, checks the thresholds, writes `signoff_report.md`, and
   exits 1 on any failure.
2. Run the scenario: a teammate's concise prompt (v7) drops the eval pass rate to
   88%. Run the gate. It must block. Restore the line that offers options (back to
   94%). Run again. It must pass and sign off.

<details><summary>Hint: the gate skeleton</summary>

```python
import json, sys
BARS = {"eval": 0.90, "cost": 0.02, "p95": 4000, "safety": 1.00}
def load(f): return json.load(open(f))

tests, evals, obs = load("test_report.json"), load("eval_report.json"), load("cost_latency.json")
checks = {
    "tests":  tests["failed"] == 0,
    "eval":   evals["pass_rate"]        >= BARS["eval"],
    "cost":   obs["cost_usd"]           <= BARS["cost"],
    "p95":    obs["p95_ms"]             <= BARS["p95"],
    "safety": evals["safety_pass_rate"] >= BARS["safety"],
}
if not all(checks.values()):
    print("GATE FAILED", [k for k, v in checks.items() if not v]); sys.exit(1)
print("GATE PASSED")
```
</details>

**Done when.** Two runs, two outcomes from the same gate: v7 blocked (exit 1), the
fix passed (exit 0), and `signoff_report.md` written for the passing build.

<details><summary>Reveal: writing the sign-off and the regression scenario</summary>

```python
def write_signoff(checks, evals, obs, build, prompt, path="signoff_report.md"):
    rows = [
        ("Tool + behaviour tests", "0 failures", str(0 if checks["tests"] else "fail")),
        ("Eval pass rate", ">= 90%", f"{evals['pass_rate']:.0%}"),
        ("Cost / resolution", "<= $0.02", f"${obs['cost_usd']:.3f}"),
        ("p95 latency", "<= 4000 ms", f"{obs['p95_ms']} ms"),
        ("Safety / PII", "100%", f"{evals['safety_pass_rate']:.0%}"),
    ]
    decision = "APPROVED for blue-green" if all(checks.values()) else "BLOCKED"
    lines = [f"# TravelMind Sign-off", f"Build {build}  Prompt {prompt}", "",
             "| Gate | Threshold | Actual |", "|---|---|---|"]
    lines += [f"| {a} | {b} | {c} |" for a, b, c in rows]
    lines += ["", f"Decision: {decision}"]
    open(path, "w").write("\n".join(lines))
```

The regression scenario, in the eval harness:

```python
from travelmind_agent import set_system_prompt, SYSTEM_PROMPT
V6 = SYSTEM_PROMPT
V7 = "You are TravelMind. Look up the PNR and answer briefly. Never invent a PNR or flight."

def eval_prompt(p):
    set_system_prompt(p)
    return sum(run_case(c) for c in cases) / len(cases)   # run_case from Lab 3

print("v6", f"{eval_prompt(V6):.0%}", " v7", f"{eval_prompt(V7):.0%}")   # expect v7 lower
set_system_prompt(V6)                                      # restore before shipping
```
</details>

---

## Put it together: the end-to-end run

The stages connect through small JSON reports. Each writes one; the gate reads
all three. That file contract is why a stage can run on a different machine or at
a different time and the gate still works.

```
Lab 1 tests        -> test_report.json   ┐
Lab 3/4 eval       -> eval_report.json   ├─> Lab 6 gate -> signoff_report.md (+ exit code)
Lab 5 observe/cost -> cost_latency.json  ┘
```

A pipeline runs them in order: tests, eval, observability, gate. Run the cheap
deterministic layers on every commit, the model and judge layers on change and on
a schedule, and the gate before every promotion.

---

## Self-check

You have completed end-to-end QA when you can answer yes to all of these.

- [ ] My contract tests pass with no AWS, and fail if a tool returns a wrong shape.
- [ ] My behaviour test passes on several seeds and asserts a property, not wording.
- [ ] My golden set has must, any_of, and must_not rules, and prints a pass rate.
- [ ] My judge scores a good reply high and a crippled reply low, grounded in facts.
- [ ] I enabled observability for my track and found a failing tool span in `aws/spans`.
- [ ] I can state the dollar cost of a typical resolution.
- [ ] My gate blocks the 88% build and passes the 94% build, and writes a sign-off.

A simple scoring guide for the workshop: one point per box, plus one bonus point
for any stretch goal below. Six or more out of seven is a pass.

---

## Stretch goals

- **Pairwise judge with position swap.** Compare two replies; score (A, B) and
  (B, A) and average to cancel position bias.
- **Grow the golden set from an incident.** Take the swallowed-tool-failure from
  Lab 5, write a case that would have caught it, and add it to the set.
- **Alarm on cost.** Decide a cost-per-resolution ceiling and describe the
  CloudWatch alarm you would set on it.
- **Multi-agent routing test.** Add a supervisor with two specialists and assert
  the right specialist was reached for a rebooking request.

---

## Common errors and fixes

| Symptom | Cause | Fix |
|---------|-------|-----|
| ValidationException on the model id | missing inference-profile prefix | use the `us.` prefix on the model id |
| Behaviour test flakes between runs | asserting exact wording | assert a property: a tool was called, a real option appeared |
| Judge returns prose, not a number | rubric did not force JSON | end the rubric with "Return ONLY JSON {...}" and parse defensively |
| Judge scores everything 4 to 5 | no facts given | pass the real tool outputs as FACTS |
| Dashboards and `aws/spans` are empty | Transaction Search not enabled | CloudWatch -> Application Signals -> Transaction Search, once per Region |
| Logs Insights query returns nothing | wrong field name | run `fields @message | limit 5` first, then match the real keys |
| Gate never blocks anything | it warns but does not exit non-zero | `sys.exit(1)` when any check fails |
