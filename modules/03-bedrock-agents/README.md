# 🤖 Module 03 · Amazon Bedrock Agents

> Console to code: action groups, orchestration, and controlling behaviour.

**Estimated time:** 6–7 hours &nbsp;·&nbsp; **Prerequisites:** Module 02.

Bedrock Agents give you a managed agent loop. You will build one in the console, then rebuild it in code so you understand what the console was doing for you — and then hand-build the loop yourself so nothing is magic.

---

## What you will be able to do

- Create a Bedrock Agent in the console and invoke it from Python
- Define action groups backed by Lambda and a correct OpenAPI schema
- Trace an agent's reasoning and debug a failed orchestration
- Control verbosity, latency and cost through instructions and configuration
- Hand-build the agent loop so the managed one holds no mystery

## Concepts in this module

| Portable GenAI concepts | AWS-specific surface |
| --- | --- |
| Agent loop | Bedrock Agents |
| Tool routing | Action groups |
| ReAct-style orchestration | AWS Lambda |
| Prompt-driven behaviour control | OpenAPI schemas |
|  | Agent tracing |
|  | CloudWatch |

Portable concepts transfer to any stack. The AWS column is where this module touches the cloud — see [`docs/concepts/portability-matrix.md`](../../docs/concepts/portability-matrix.md).

## Run it in this order

| # | | Step | What it is |
| --- | --- | --- | --- |
| 1 | 📖 | [`slides/Day8_Deck1_Console_to_Code.pptx`](slides/Day8_Deck1_Console_to_Code.pptx) | Console to code |
| 2 | 💻 | [`notebooks/00_connect_to_agent.ipynb`](notebooks/00_connect_to_agent.ipynb) | Connect to your agent |
| 3 | 💻 | [`notebooks/01_setup_invoke_trace.ipynb`](notebooks/01_setup_invoke_trace.ipynb) | Setup, invoke, and read the trace |
| 4 | 💻 | [`notebooks/02_handbuilt_loop.ipynb`](notebooks/02_handbuilt_loop.ipynb) | Hand-build the loop — the demystifier |
| 5 | 💻 | [`notebooks/03_action_groups.ipynb`](notebooks/03_action_groups.ipynb) | Action groups with Lambda |
| 6 | ✏️ | [`exercises/Day8_Guided_Practice_Agent_Loops_and_Action_Groups.md`](exercises/Day8_Guided_Practice_Agent_Loops_and_Action_Groups.md) | Guided practice |
| 7 | 📖 | [`slides/Day8_Deck2_Controlling_Behavior.pptx`](slides/Day8_Deck2_Controlling_Behavior.pptx) | Controlling behaviour |
| 8 | 💻 | [`notebooks/04_controlling_behavior.ipynb`](notebooks/04_controlling_behavior.ipynb) | Behaviour control in practice |
| 9 | ✏️ | [`exercises/verbosity_tax_exercise.md`](exercises/verbosity_tax_exercise.md) | The verbosity tax — cost of chatty agents |
| 10 | 💻 | [`notebooks/05_production_and_insights.ipynb`](notebooks/05_production_and_insights.ipynb) | Production patterns and insights |
| 11 | ✏️ | [`exercises/disruption_desk_exercise.md`](exercises/disruption_desk_exercise.md) | Disruption desk — the full scenario |

📖 read &nbsp; 💻 run &nbsp; ✏️ practise &nbsp; 📊 workbook &nbsp; 🔖 reference

## Walkthrough recording

| Session | Recording |
| --- | --- |
| Module 03 — Amazon Bedrock Agents | _link pending_ |

> Recordings are being published progressively. [Track progress in the video index](../../docs/reference/video-index.md).

## Solutions

Worked solutions live in [`solutions/`](solutions/). Attempt every exercise closed-book first — the solutions are written to be read *after* you have a wrong answer to compare against.

## Common mistakes

- An OpenAPI schema the model cannot read. Vague descriptions produce wrong tool calls.
- Forgetting Lambda resource-based permissions for the agent to invoke it.
- Treating verbosity as free. Every extra sentence is tokens on every turn.

## Folder map

```
activities       3 file(s)
exercises        7 file(s)
notebooks        6 file(s)
slides           3 file(s)
solutions        3 file(s)
```

## Field guide for this module

Reference material for the ideas in this module — open these while you work, not before.

**Frameworks**

- [Autonomy Ladder](../../cheatsheets/frameworks/autonomy-ladder.md) — What the managed loop is doing for you
- [Token Tax Ledger](../../cheatsheets/frameworks/token-tax-ledger.md) — The verbosity tax, quantified
- [Failure Signature Catalog](../../cheatsheets/frameworks/failure-signature-catalog.md) — 16 signatures → cause → fix

**Quick reference**

- [Bedrock Converse API](../../cheatsheets/quick-reference/bedrock-converse.md) — The loop underneath the managed agent
- [IAM for agents](../../cheatsheets/quick-reference/iam-for-agents.md) — Agent → Lambda resource policies

**Recipes and procedures**

- [Runbook · runaway loop](../../cheatsheets/runbooks/incident-runaway-loop.md) — When the loop does not converge

---

⬅️ [Module 02 · Amazon Bedrock Essentials](../02-bedrock-essentials/) &nbsp;·&nbsp; 🏠 [All modules](../) &nbsp;·&nbsp; 🗺️ [Learning paths](../../docs/learning-paths/) &nbsp;·&nbsp; [Module 04 · Agent Builder, Knowledge Bases and Guardrails](../04-agent-builder-and-knowledge-bases/) ➡️
