# Setup

Do these in order. The first one has a waiting step, so start it early.

| | | |
| --- | --- | --- |
| 1️⃣ | **[AWS account setup](aws-account-setup.md)** | Model access is per model, **per region**, and requested manually — approval is not always instant |
| 2️⃣ | **[Cost controls](cost-controls.md)** | Budget alarm and the teardown checklist. **Read before you create anything** |
| 3️⃣ | **[Local environment](local-environment.md)** | Python, virtual environments, per-module requirements, notebook hygiene |
| 🧯 | **[Troubleshooting](troubleshooting.md)** | The errors this curriculum actually produces, in the order you meet them |

---

## The three things that catch everyone

**1. Model access is not on by default.** It is granted per model, per region, on request. An empty model
list is a permissions state, not an outage.

**2. Many models need an inference profile ID, not the bare model ID.** The ID carries a geography prefix
(`us.`, `eu.`, …). This is the single most common first-day error.

```bash
aws bedrock list-inference-profiles --region us-east-1 \
  --query 'inferenceProfileSummaries[].inferenceProfileId' --output table
```

**3. Two things bill for *existing*, not for use.** OpenSearch Serverless collections and AgentCore
runtimes. They are what people leave running by accident.
[Teardown checklist](cost-controls.md#teardown-checklist).

## No AWS account yet?

Start with [Module 00](../../modules/00-agentic-foundations/),
[Module 01](../../modules/01-llm-and-aws-bridge/) and
[Module 15](../../modules/15-agentic-product-lifecycle/) — none need one. So do
[`rag_by_hand.py`](../../modules/10-rag-opensearch-litellm/src/rag_by_hand.py) and
[`quality_gate.py`](../../modules/13-agentic-qa-and-evaluation/src/quality_gate.py).

## Verify you are ready

Run [`00_Bedrock_Onboarding.ipynb`](../../modules/02-bedrock-essentials/notebooks/00_Bedrock_Onboarding.ipynb).
It checks access, invokes a model and prints token usage. Clean run means you are set up.

---

[⬅️ Docs](../) · [▶️ START-HERE](../START-HERE.md) · [🧯 Troubleshooting](troubleshooting.md)
