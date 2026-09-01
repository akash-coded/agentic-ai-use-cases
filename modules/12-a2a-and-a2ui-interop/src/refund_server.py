from strands import Agent, tool
from strands.multiagent.a2a import A2AServer
from strands.models import BedrockModel

# @tool is mandatory. Without it the tool never registers
# and the Agent Card advertises zero skills.
@tool
def look_up_booking(pnr: str) -> dict:
    """Look up an airline booking by PNR. Returns fare and refund eligibility."""
    return {"pnr": pnr, "fare_usd": 420.0, "refundable": True, "penalty_usd": 50.0}

@tool
def process_refund(pnr: str, amount_usd: float) -> dict:
    """Process a refund for a booking. Returns a confirmation id."""
    return {"pnr": pnr, "refunded_usd": amount_usd, "confirmation": "RF-" + pnr}

agent = Agent(
    name="Refund Agent",
    description="Handles airline refund eligibility and processing.",
    model=BedrockModel(model_id="us.anthropic.claude-haiku-4-5-20251001-v1:0"),
    tools=[look_up_booking, process_refund],
    callback_handler=None,   # quiet: no streaming prints from the server-side agent
)

# Listens on 9005 to match SERVER_URL. Pass port explicitly; the A2AServer default is 9000.
# The Agent Card auto-advertises this port, so discovery stays consistent.
server = A2AServer(agent=agent, port=9005)

if __name__ == "__main__":
    server.serve()
