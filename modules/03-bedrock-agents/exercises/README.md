# TravelMind on Amazon Bedrock — Day 4 Hands-On (Notebooks 1–5)

End-to-end, build-from-scratch walkthrough of calling, building, controlling, and operating a Bedrock agent. Everything runs against one use case (**TravelMind**, an airline booking/disruption assistant) and one region (`us-east-1`). The notebooks pick up from the Day 3 agent you built in the Bedrock console.

## The five notebooks

| # | File | What you build |
|---|---|---|
| 1 | `01_setup_invoke_trace.ipynb` | The four boto3 clients, Converse on Nova and Claude, invoke the managed agent, read the THINK/ACT/OBSERVE trace, session memory |
| 2 | `02_handbuilt_loop.ipynb` | The ReAct loop by hand: tools, `toolConfig`, the 5 loop rules, the happy path, and the 50-loop reproduced on purpose |
| 3 | `03_action_groups.ipynb` | Add an action group two ways: a Lambda executor from scratch (IAM role, function, permission) and a `RETURN_CONTROL` group driven from code |
| 4 | `04_controlling_behavior.ipynb` | Loop guards + spin-detection + fallback tool, inference parameters (and reasoning-model limits), and the 5-layer hallucination defense incl. grounding guardrails |
| 5 | `05_production_and_insights.ipynb` | Roles vs keys, least-privilege IAM, retries/backoff, observability, cost controls, prod aliases, idempotency, an eval harness, and PII/input guards |

Run them in order. Each builds on the last.

## One-time prerequisites

1. **An AWS account** with Bedrock enabled in `us-east-1`.
2. **Model access** granted (Bedrock console → *Model access*) for:
   - `amazon.nova-lite-v1:0` (on-demand)
   - Claude via the cross-region profile `us.anthropic.claude-3-5-haiku-20241022-v1:0`
3. **The Day 3 agent.** Copy its 10-char **Agent ID** from Bedrock → *Agents* → your agent → *Agent overview*. The dev alias is always `TSTALIASID`.
4. **IAM permissions** for your identity: invoke the agent, Converse with the two models, and (for Notebooks 3 and 5) manage Lambda, IAM roles, guardrails, and agent aliases. Notebook 5 prints the least-privilege caller policy you would ship.
5. **boto3** (`pip install boto3`). Nothing else.

## Quickstart

**VS Code**
1. `python -m venv .venv` and activate it.
2. `aws configure` (or set `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` / `AWS_SESSION_TOKEN`); set `AWS_DEFAULT_REGION=us-east-1`.
3. `pip install boto3`, then select the `.venv` kernel.

**Google Colab**
1. `!pip install boto3`
2. Set credentials via Colab **Secrets** or `os.environ` (never paste a key into a cell).
3. Keep `region_name="us-east-1"` everywhere.

## Placeholders you must fill

| Placeholder | Where | What to put |
|---|---|---|
| `AGENT_ID = "XXXXXXXXXX"` | every notebook (cell 1) | your Day 3 Agent ID, or export `TRAVELMIND_AGENT_ID` |
| `GUARDRAIL_ID` | NB4 (create it), NB5 (eval/audit) | the guardrail id created in Notebook 4 |
| Opus model id | NB4 (reasoning-model cell) | the current Opus inference-profile id from the console catalog, if you demo it |
| `PRICE_PER_1K` rates | NB5 (cost section) | live numbers from the Bedrock pricing page (placeholders are zeros on purpose) |
| inference-profile region ARNs | NB5 (IAM policy) | the exact regions your `us.` profile routes to (confirm in the console) |

## A note on cloud resources

Notebooks 3 and 5 can **create** real resources: an IAM role, a Lambda function, an action group, and optionally a production alias. Every create call is **idempotent** (it catches "already exists" and reuses), so re-running is safe. To remove them afterward, delete in reverse order: action group, then Lambda, then the role. Account-level model invocation logging in Notebook 5 is **off by default** behind a flag.

## House rules baked into the code

- `us-east-1` only — the region these materials are scoped to.
- The `us.` prefix on Claude is a cross-region inference profile; the bare id fails. This trap is shown, not hidden.
- Every code path notes **what changes in production**: roles not keys, no hardcoded region/secrets, least privilege, retries, observability.
- Anti-patterns are demonstrated deliberately (missing `us.` prefix, role-mixing in the tool loop, the runaway loop) so you recognise them in the wild.
