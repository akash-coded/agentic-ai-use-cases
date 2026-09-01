# IAM for Agents — Cheat Sheet

Permissions are the only guard that actually holds. A prompt saying "never issue a refund" is a
suggestion; an IAM policy without that permission is a fact.

---

## The four identities in an agent system

| Identity | Is | Should be able to |
| --- | --- | --- |
| **Developer** | You, building | Broad, in a sandbox account only |
| **Agent execution role** | What the runtime assumes | Invoke models; nothing else by default |
| **Tool roles** | Per-tool credentials | Exactly one job each |
| **Caller** | Whoever invokes the agent | Invoke the agent, nothing behind it |

The mistake that matters: collapsing tool roles into the agent role. Then every tool inherits every
permission, and your [blast radius](../frameworks/blast-radius-grid.md) is the union of all of them.

## Minimum to invoke a model

```json
{ "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"],
    "Resource": [
      "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-*",
      "arn:aws:bedrock:us-east-1:123456789012:inference-profile/us.anthropic.claude-*"
    ]}]}
```

> **Cross-Region inference profiles need both ARNs** — the profile *and* the underlying foundation models
> in every region the profile routes to. Granting only the profile is a very common cause of a confusing
> `AccessDeniedException`.

## Scoping per tool

```
❌ one role for everything
   { "Action": ["dynamodb:*", "s3:*", "lambda:InvokeFunction", "ses:SendEmail"] }

✅ one role per tool
   get_booking    → dynamodb:GetItem  on table/Bookings
   search_policy  → bedrock:Retrieve  on knowledge-base/KB123
   get_disruption → lambda:InvokeFunction on function:disruption-lookup
   draft_response → (no AWS permissions at all)
```

Note the last line. A tool that only formats text should have **no** AWS permissions. Most agents have at
least one such tool, and it is usually granted the same role as everything else.

## Bedrock Agents → Lambda

The agent needs to invoke the Lambda, and the Lambda needs a **resource-based policy** allowing it:

```bash
aws lambda add-permission \
  --function-name travelmind-actions \
  --statement-id bedrock-agent-invoke \
  --action lambda:InvokeFunction \
  --principal bedrock.amazonaws.com \
  --source-arn arn:aws:bedrock:us-east-1:123456789012:agent/AGENTID
```

Missing this is the classic "the agent silently cannot call my action group" — it shows up as
`AccessDeniedException` inside the trace, not as a top-level error.

## Knowledge bases and OpenSearch

```json
{ "Effect": "Allow",
  "Action": ["bedrock:Retrieve", "bedrock:RetrieveAndGenerate"],
  "Resource": "arn:aws:bedrock:us-east-1:123456789012:knowledge-base/KB123" }
```

The KB's *own* service role separately needs `aoss:APIAccessAll` on the collection and `s3:GetObject` on the
data source. Three roles, three jobs — do not merge them.

## Conditions worth using

**Restrict to a specific inference profile:**

```json
{ "Condition": { "StringEquals": {
    "bedrock:InferenceProfileArn":
      "arn:aws:bedrock:us-east-1:123456789012:inference-profile/us.anthropic.claude-sonnet-4-5-20250929-v1:0" }}}
```

**Require a guardrail on every call:**

```json
{ "Effect": "Deny",
  "Action": "bedrock:InvokeModel",
  "Resource": "*",
  "Condition": { "Null": { "bedrock:GuardrailIdentifier": "true" } } }
```

That Deny is one of the highest-value policies you can write: it makes "always apply the guardrail"
structural rather than a convention people forget.

## Learning vs production

| | Learning (sandbox) | Production |
| --- | --- | --- |
| Model access | `bedrock:*` | Specific models + profiles |
| Tools | One role | One role per tool |
| Resources | `*` | Named ARNs |
| Guardrail | Optional | Enforced by Deny |
| Review | None | Change review on every policy |

[The setup guide](../../docs/setup/aws-account-setup.md) deliberately uses broad managed policies for
learning. [Module 11](../../modules/11-bedrock-agentcore/) is where you scope them properly.

## The audit

| Question | If no |
| --- | --- |
| Does any tool have permissions it never uses? | Remove them |
| Could any single tool cause irreversible, wide damage? | Decompose it |
| Is any guard implemented only in the prompt? | Move it to IAM |
| Would you be comfortable if this role leaked? | Scope it down |

**Related:** [Blast Radius Grid](../frameworks/blast-radius-grid.md) ·
[Tool Surface Audit](../frameworks/tool-surface-audit.md) · [AgentCore](agentcore.md)
