# TravelMind QA kit

The runnable code behind the Agentic QA training. It takes one agent, TravelMind,
from a passing demo to a build you can sign off on, following the same four topics
as the deck and ending with one pipeline that runs the whole flow.

The through-line is simple: **a green demo is not a trustworthy agent.** These
files build the discipline that closes that gap, one layer at a time.

---

## Read in this order

The kit is built to be read top to bottom. Each file assumes the one before it.

| # | File | Topic | What it is |
|---|------|-------|------------|
| 0 | `travelmind_agent.py` | foundation | The agent under test: three tools plus the wired agent. Read first. |
| 0 | `config.py` | foundation | Single source of truth: models, region, log group, thresholds. |
| 1 | `test_contracts.py` | 1 | Deterministic tool-contract tests. No model, no AWS. Runs on every commit. |
| 1 | `test_multiagent.py` | 1 | Behaviour, trajectory, and multi-agent tests. Real model, run on change. |
| 2 | `golden_set.jsonl` | 2 | The evaluation cases: criteria, not exact answers. |
| 2 | `eval_harness.ipynb` | 2 | The three-grader eval: deterministic, LLM-as-judge, RAGAS. |
| 3 | `debug_walkthrough.ipynb` | 3 | Read a failing trace, localise it to one span, cost the run. |
| 3 | `cloudwatch_filters.md` | 3 | The CloudWatch Logs Insights query catalogue. |
| 4 | `quality_gate.py` | 4 | The gate: composes the reports into a block-or-pass decision. |
| 4 | `signoff_report.md` | 4 | A sample sign-off the gate produces. |
| e2e | `run_qa_pipeline.py` | all | The capstone: runs all four stages in order and produces the sign-off. |

---

## The fast way to see it work

Run the whole pipeline with no cloud access. Stage 1 (tests) and stage 4 (gate)
are real; the two AWS-dependent stages use sample numbers:

```
pip install pytest
python run_qa_pipeline.py --offline
```

You will see the four stages run in sequence and a `signoff_report.md` appear.
Then switch to the real path once credentials are set:

```
python run_qa_pipeline.py            # online: stages 2 and 3 call Bedrock
```

---

## Configuration

Everything environment-specific lives in `config.py`. Change it there, never
inline in ten files.

- `AGENT_MODEL_ID` / `JUDGE_MODEL_ID`: Bedrock inference-profile ids. The judge is
  a stronger model than the agent, because a grader should be at least as capable
  as the thing it grades. The `us.` prefix is required for on-demand Claude
  models; a bare id raises a ValidationException.
- `REGION`: the AWS region.
- `SPANS_LOG_GROUP`: where OpenTelemetry spans land (`aws/spans`).
- `PRICES`: token prices used to compute cost. A snapshot; confirm on the Bedrock
  pricing page before quoting.
- `THRESHOLDS`: the bars the gate enforces. Agree these with the client; tightening
  one should be a reviewed change.

---

## Setup

**VS Code (local), three steps:**
1. `python -m venv .venv` then `source .venv/bin/activate`
2. `aws configure` to set credentials (in production, use an IAM role, not keys)
3. `pip install -r requirements.txt`

**Google Colab, three steps:**
1. `!pip install -r requirements.txt`
2. Set `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION` from
   Colab Secrets (do not paste keys into a shared notebook)
3. Upload `config.py`, `travelmind_agent.py`, and `golden_set.jsonl` to the session

---

## What needs AWS, and what does not

| Runs anywhere (no AWS) | Needs AWS credentials |
|------------------------|-----------------------|
| `test_contracts.py` | `test_multiagent.py` (real model) |
| `quality_gate.py` (reads files) | `eval_harness.ipynb` agent and judge cells |
| `run_qa_pipeline.py --offline` | `debug_walkthrough.ipynb` (Bedrock + CloudWatch) |
| the pure-logic self-checks inside the notebooks | `run_qa_pipeline.py` online |

The split is deliberate. The deterministic layer is what you run on every commit;
the model-dependent layer runs on change and on a schedule. That is the test
pyramid showing up in the file layout.

---

## One note on the code vs the deck

The deck split the tools and the agent across two slides for clarity. Here they
live together in `travelmind_agent.py`, with the tools written as plain functions
that the agent wraps at wiring time. That separation is what makes the bottom of
the test pyramid (the contract tests) cheap to run with no model. It is the same
design the deck argued for, shown in one file.

---

## How the files connect

```
test_contracts.py  ──▶ test_report.json   ┐
eval_harness.ipynb ──▶ eval_report.json   ├──▶ quality_gate.py ──▶ signoff_report.md
debug_walkthrough  ──▶ cost_latency.json  ┘

run_qa_pipeline.py orchestrates all of the above in order.
```

Each stage writes a small JSON report; the gate reads them. The reports are the
contract between stages, which is why a stage can run on a different machine or at
a different time and the gate still works.
