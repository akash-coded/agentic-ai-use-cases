"""Minimum AgentCore Runtime agent: Strands + Amazon Bedrock.

Contract: POST /invocations with {"prompt": "..."} -> {"result": "..."}
Run locally:  agentcore dev
Deploy:       agentcore deploy
"""

import json
import os

from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands import Agent, tool
from strands.models import BedrockModel

MODEL_ID = "us.anthropic.claude-haiku-4-5-20251001-v1:0"
REGION = os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1"))

SYSTEM_PROMPT = (
    "You are TravelMind, an airline support agent. "
    "Use get_pnr for any question about a booking. "
    "Answer in three sentences or fewer. Never invent a booking."
)

# --- built once at import: cheap to share, no per-caller state ---
app = BedrockAgentCoreApp()
model = BedrockModel(model_id=MODEL_ID, region_name=REGION)

_BOOKINGS = {
    "JX48Q2": {"passenger": "Rao", "tier": "Gold",
               "segment": "BLR-DEL", "status": "CANCELLED"},
}


@tool
def get_pnr(pnr: str) -> str:
    """Look up an airline booking by its PNR code."""
    return json.dumps(_BOOKINGS.get(pnr.strip().upper(), {"error": "PNR not found"}))


@app.entrypoint
def invoke(payload, context):
    """Entrypoint. Validate input, run one stateless agent turn, return JSON."""
    prompt = payload.get("prompt") if isinstance(payload, dict) else None
    if not isinstance(prompt, str) or not prompt.strip():
        return {"error": "payload must contain a non-empty 'prompt' string"}

    agent = Agent(model=model, tools=[get_pnr], system_prompt=SYSTEM_PROMPT)
    result = agent(prompt)

    return {
        "result": str(result),
        "session_id": getattr(context, "session_id", None),
        "model": MODEL_ID,
    }


if __name__ == "__main__":
    app.run()
