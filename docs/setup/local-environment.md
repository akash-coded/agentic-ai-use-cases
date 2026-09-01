# Local Environment

## Quick start

```bash
git clone https://github.com/akash-coded/aws-bedrock-agentcore-strands.git
cd aws-bedrock-agentcore-strands
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

Python 3.11 or newer. Some AgentCore tooling expects 3.11+.

## Per-module requirements

Several modules pin their own dependencies. Prefer those when working inside that module:

| Module | File |
| --- | --- |
| [06 Strands](../../modules/06-strands-foundations/) | `src/requirements.txt` |
| [07 Multi-agent](../../modules/07-strands-multi-agent-patterns/) | `notebooks/requirements-strands-patterns.txt` |
| [10 RAG labs](../../modules/10-rag-opensearch-litellm/) | `labs/rag-labs/requirements.txt` |
| [11 AgentCore](../../modules/11-bedrock-agentcore/) | `notebooks/requirements.txt` |
| [12 A2A / A2UI](../../modules/12-a2a-and-a2ui-interop/) | `notebooks/requirements.txt` |
| [13 QA](../../modules/13-agentic-qa-and-evaluation/) | `src/requirements.txt` |
| [14 Production](../../modules/14-end-to-end-production/) | `src/requirements.txt` |

A separate virtual environment per module is not overkill — the LangChain and Strands tracks pull different
dependency trees.

## Environment variables

Copy the example where one exists (for instance
[`modules/07-strands-multi-agent-patterns/notebooks/.env.example`](../../modules/07-strands-multi-agent-patterns/notebooks/.env.example))
to `.env` in the same folder. `.env` is git-ignored.

Never hard-code a region, model ID or account ID in a notebook cell you intend to commit.

## Notebook hygiene before committing

Notebook *outputs* are committed in this repo on purpose — seeing expected output is part of the teaching.
But outputs leak things. Before you commit a notebook you have run:

```bash
grep -l "$(whoami)" **/*.ipynb          # local paths in tracebacks or pip output
grep -lE '[0-9]{12}' **/*.ipynb          # AWS account ids in ARNs
```

Anything found should be scrubbed. Account IDs in this repo are the placeholder `123456789012`.

## Running without AWS

Some material runs with no cloud at all: all of [Module 00](../../modules/00-agentic-foundations/), the
[intuition bank](../../modules/01-llm-and-aws-bridge/exercises/LLM_Intuition_Bank.md),
[`rag_by_hand.py`](../../modules/10-rag-opensearch-litellm/src/rag_by_hand.py),
[`quality_gate.py`](../../modules/13-agentic-qa-and-evaluation/src/quality_gate.py) (it only reads JSON
files), and all of [Module 15](../../modules/15-agentic-product-lifecycle/).

---

**Next:** [cost controls](cost-controls.md) · [troubleshooting](troubleshooting.md)
