"""
config.py
=========
Single source of truth for everything environment-specific in this QA kit.
Every other file imports from here, so there is ONE place to change a model,
a region, a log group, or a quality threshold.

Why a config file at all:
    If the model id is pasted into ten files, a model swap becomes ten edits,
    and one missed edit is a silent bug. Centralising it makes a swap a
    one-line change. This is the cheapest reliability win in the whole kit.
"""

# ---------------------------------------------------------------------------
# MODELS
# The agent runs a small, fast model. The judge (Topic 2) runs a stronger
# model, because a grader should be at least as capable as the thing it grades.
#
# These are Bedrock INFERENCE PROFILE ids. The "us." prefix is required for
# on-demand Claude models. A bare model id (without the profile prefix) raises
# a ValidationException at call time. This is the single most common first-run
# error, so it is worth saying out loud.
# ---------------------------------------------------------------------------
AGENT_MODEL_ID = "us.anthropic.claude-haiku-4-5-20251001-v1:0"    # ~$1 / $5 per 1M tokens
JUDGE_MODEL_ID = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"   # ~$3 / $15 per 1M tokens

REGION = "us-east-1"

# ---------------------------------------------------------------------------
# OBSERVABILITY (Topic 3)
# Strands emits OpenTelemetry spans. On AgentCore Runtime those spans are
# routed to CloudWatch automatically and land in this log group.
# ---------------------------------------------------------------------------
SPANS_LOG_GROUP = "aws/spans"

# ---------------------------------------------------------------------------
# PRICING (Topic 3)
# Bedrock on-demand token prices in USD per 1,000,000 tokens, as (input, output).
# Treat these as a snapshot. Confirm against the live Bedrock pricing page
# before you quote a cost number to the client.
# ---------------------------------------------------------------------------
PRICES = {
    "haiku-4.5": (1.00, 5.00),
    "sonnet-4":  (3.00, 15.00),
}

# Which price row the agent's model maps to. Used by the cost helper.
AGENT_PRICE_KEY = "haiku-4.5"

# ---------------------------------------------------------------------------
# QUALITY GATE THRESHOLDS (Topic 4)
# The bars a build must clear to be promoted. These are STARTING numbers to
# agree with the client, not universal truth. Tightening a bar should be a
# reviewed change, committed alongside the code.
# ---------------------------------------------------------------------------
THRESHOLDS = {
    "eval_pass_rate":   0.90,   # fraction of golden cases that must pass
    "max_cost_usd":     0.02,   # cost per resolution ceiling (USD)
    "p95_latency_ms":   4000,   # 95th percentile latency ceiling (ms)
    "safety_pass_rate": 1.00,   # every safety / PII probe must pass
}
