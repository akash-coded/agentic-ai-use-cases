# AWS Account Setup

Do this **before** Module 02. Model access approval is not always instant, and discovering that on a
Saturday morning wastes the morning.

## 1. An account you are allowed to spend on

Use a personal or sandbox account, not a production one. You will create knowledge bases, Lambda functions
and agent runtimes. Set a budget alarm first — see [cost controls](cost-controls.md).

## 2. Pick a region and stay in it

Most of this curriculum is developed against `us-east-1`. Model and feature availability differs by region,
and AgentCore is not available everywhere. If you choose a different region, verify your models are there
before you start.

```bash
aws bedrock list-foundation-models --region us-east-1 --query 'modelSummaries[].modelId' --output table
```

An empty or short list is a permissions state, not an outage — go to step 3.

## 3. Request model access

Bedrock model access is granted **per model, per region**, on request, in the console:

**Amazon Bedrock → Model access → Modify model access → select models → submit**

Request at minimum an Anthropic Claude model and an Amazon Titan or Nova embedding model. Some models are
approved instantly; others are not.

## 4. Understand inference profiles before your first error

Many models are invoked through a **cross-Region inference profile** rather than the bare model ID. The
profile ID carries a geography prefix — `us.`, `eu.` and others depending on the geography.

```bash
aws bedrock list-inference-profiles --region us-east-1 \
  --query 'inferenceProfileSummaries[].inferenceProfileId' --output table
```

Use the ID this command returns as your `modelId`. Passing a bare model ID where a profile is required is
the single most common first-day error in this curriculum. When you use a geographic profile, you need
model access enabled in **every** region the profile routes to.

## 5. Credentials

```bash
aws configure
aws sts get-caller-identity
```

If the second command names your account, you are ready. Never put credentials in a notebook — the
`.gitignore` in this repo blocks `.env` files, but it cannot unstage a key you pasted into a cell.

## 6. Permissions

For learning, an IAM user or role with these managed policies is enough:

- `AmazonBedrockFullAccess`
- `AWSLambda_FullAccess` (Modules 03–04)
- `IAMFullAccess` (creating agent execution roles — scope this down outside a sandbox)
- `CloudWatchLogsFullAccess`
- `AmazonOpenSearchServiceFullAccess` (Module 10)

These are deliberately broad because you are learning. Module 11 teaches you to scope them properly, and
[the Module 11 LLD](../architecture/lld/11-bedrock-agentcore.md) explains why over-broad roles are the
default production mistake.

## 7. Verify

Run [`PreWave5_Bedrock_Onboarding.ipynb`](../../modules/02-bedrock-essentials/notebooks/PreWave5_Bedrock_Onboarding.ipynb).
It checks access, invokes a model and prints token usage. If it runs clean, you are set up.

---

**Next:** [local environment](local-environment.md) · [cost controls](cost-controls.md) ·
[troubleshooting](troubleshooting.md)
