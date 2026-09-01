"""
model_failover.py
=================
Cross-provider, cross-family failover for TravelMind when the primary model is
down. Runs OFFLINE by default: a mock simulates each provider, and you can force
an outage to watch the chain fall through. The real LiteLLM path is behind LIVE.

The rule this encodes: fail over in the order that keeps the most behavior.
  tier 0  same model, other region   (already inside the us. inference profile)
  tier 1  same family, other deploy  (Bedrock Claude -> Anthropic API / Vertex)
  tier 2  different family           (Claude -> GPT / Gemini), LAST resort, eval'd

Two ways to wire it, both below:
  A) MANUAL chain (answer_with_failover): swaps the PROMPT per family. Use this
     across families, because one prompt does not fit all of them.
  B) LiteLLM Router (build_router): auto-fallback, but it sends the SAME messages
     to every tier. Fine for same-family tiers, risky across families.

Run (VS Code):
  python -m venv .venv && source .venv/bin/activate     # 1. activate venv
  pip install litellm boto3                             # 2. deps (only if LIVE)
  python model_failover.py                              # 3. run (offline demo)

Run (Colab): !pip install litellm boto3 ; put provider keys in Secrets ; run.
"""
import os
import time

LIVE = os.environ.get("LIVE", "0") == "1"

# ---------------------------------------------------------------------------
# The tiered chain: (model_group, litellm_model_string, family).
# Tier 0 is NOT in this list on purpose: the us. inference profile already fails
# over across us-east-1 / us-east-2 / us-west-2 at the AWS layer, no gateway. So
# this chain starts at "Claude-on-Bedrock is down everywhere, now what".
# ---------------------------------------------------------------------------
TIERS = [
    # primary: Bedrock Claude (cross-region already handled by the us. prefix)
    ("claude-bedrock",   "bedrock/us.anthropic.claude-haiku-4-5-20251001-v1:0", "claude"),
    # same family, different deployment: keeps model behavior, your evals hold
    ("claude-anthropic", "anthropic/claude-haiku-4-5-20251001",                 "claude"),
    # different family: availability only. Set this to a model you HAVE evaluated.
    ("gpt-openai",       "openai/gpt-4o",                                       "openai"),
]

# One prompt does not fit all families. The cross-family mistake is reusing a
# Claude-tuned prompt on GPT. Give each family its own, swapped at failover time.
SYSTEM_BY_FAMILY = {
    "claude": (
        "You are TravelMind. Look up the PNR before answering. When a booking is "
        "disrupted, explain why and offer rebooking options. Never invent a PNR "
        "or a flight."
    ),
    "openai": (
        "You are TravelMind, an airline booking assistant. ALWAYS call a tool to "
        "look up the PNR before answering; do not answer from memory. Reply with "
        "status, then reason, then up to two rebooking options as a short list. "
        "If unsure, say so. Never fabricate a PNR or a flight."
    ),
}


# ---------------------------------------------------------------------------
# Circuit breaker, one per target. Stops you from hammering a dead provider.
# Defaults match the production consensus: 5 fails trips a 60s cooldown.
# ---------------------------------------------------------------------------
class CircuitBreaker:
    def __init__(self, threshold=5, cooldown=60.0):
        self.threshold = threshold
        self.cooldown = cooldown
        self.fails = 0
        self.open_until = 0.0

    def call(self, fn, *args, **kwargs):
        if time.time() < self.open_until:
            raise RuntimeError("circuit OPEN: skipping unhealthy target")
        try:
            out = fn(*args, **kwargs)
            self.fails = 0                     # success closes the circuit
            return out
        except Exception:
            self.fails += 1
            if self.fails >= self.threshold:
                self.open_until = time.time() + self.cooldown
            raise


_breakers = {}


def _breaker(group):
    if group not in _breakers:
        _breakers[group] = CircuitBreaker()
    return _breakers[group]


# ---------------------------------------------------------------------------
# Offline mock so this runs with no keys. _DOWN lets the demo force an outage.
# ---------------------------------------------------------------------------
_DOWN = set()     # e.g. {"claude-bedrock"} marks that provider as unavailable


def _mock_call(group, model, system, user):
    if group in _DOWN:
        raise RuntimeError(f"503 {group} unavailable")
    fam = "gpt" if "gpt" in model else "claude"
    # the mock proves the family-correct prompt was used (system[:18])
    return f"[{fam} via {group}] '{system[:18]}...' -> looked up PNR, offered options"


def _one_call(group, model, system, user):
    """Single attempt against one target. Real LiteLLM when LIVE, else the mock."""
    if LIVE:
        from litellm import completion          # provider keys via env / role
        r = completion(model=model, messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ])
        return r.choices[0].message.content
    return _mock_call(group, model, system, user)


# ---------------------------------------------------------------------------
# A) MANUAL chain. Swaps the prompt per family. Use across families.
# ---------------------------------------------------------------------------
def answer_with_failover(user_text, alert=print):
    """Try each tier in order with its family-correct prompt and circuit breaker.

    Returns the first success. Alerts when a fallback tier served the request, so
    a fallback that fires often shows up instead of hiding.
    """
    last = None
    for i, (group, model, fam) in enumerate(TIERS):
        system = SYSTEM_BY_FAMILY[fam]          # family-correct prompt
        try:
            out = _breaker(group).call(_one_call, group, model, system, user_text)
            if i > 0:
                alert(f"  ALERT served by fallback tier {i} ({group}); primary unhealthy")
            return out
        except Exception as e:
            print(f"  tier {i} {group}: {e} -> next")
            last = e
    raise RuntimeError(f"all tiers failed; last error: {last}")


# ---------------------------------------------------------------------------
# B) LiteLLM Router. Auto-fallback, same messages to every tier. Simpler.
# ---------------------------------------------------------------------------
def build_router():
    """Same-family auto-fallback via LiteLLM Router (runs only when LIVE).

    Test the fallback path WITHOUT a real outage:
        router.completion(model="claude-bedrock",
                          messages=[...],
                          mock_testing_fallbacks=True)
    """
    from litellm import Router
    model_list = [{"model_name": g, "litellm_params": {"model": m}} for g, m, _ in TIERS]
    return Router(
        model_list=model_list,
        # if the primary group fails, try these groups in order
        fallbacks=[{"claude-bedrock": ["claude-anthropic", "gpt-openai"]}],
        num_retries=2,            # retry the same target before falling over
        timeout=20,               # per-call ceiling; a slow call can trip a false fallback
        allowed_fails=5,          # fails before a target is cooled down
        cooldown_time=60,         # seconds a cooled-down target is skipped
    )


# What changes in production:
#   - provider keys come from the execution role / secret store, never hardcoded
#   - alert routes to your pager when tier > 0 serves more than ~5% of traffic
#   - the cross-family tier (gpt-openai) is gated on your golden set before it
#     ships, exactly like a release; an unevaluated fallback is not resilience
#   - for a tool-using agent, confirm tool-call schemas match on the fallback
#     family, or the fallback answers prose while silently dropping tool calls


if __name__ == "__main__":
    q = "My flight on JX48Q2 was cancelled. Options?"

    print("=== all healthy: primary serves it ===")
    print(answer_with_failover(q), "\n")

    print("=== Claude down on Bedrock AND Anthropic API: cross-family takes over ===")
    _DOWN.update({"claude-bedrock", "claude-anthropic"})
    print(answer_with_failover(q), "\n")

    print("=== circuit breaker: primary keeps failing, breaker opens ===")
    _DOWN.clear()
    _breakers.clear()                         # fresh state for a clean count
    _DOWN.add("claude-bedrock")               # primary down, tier 1 healthy
    for _ in range(6):
        answer_with_failover(q, alert=lambda *_: None)
    state = {g: ("open" if time.time() < b.open_until else "closed")
             for g, b in _breakers.items()}
    print("  breaker state:", state)
