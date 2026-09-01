import os
from strands import Agent, tool
from strands.multiagent.a2a import A2AServer
from strands.models import BedrockModel
from fastapi import FastAPI
import uvicorn

@tool
def look_up_booking(pnr: str) -> dict:
    """Look up an airline booking by PNR. Returns fare and refund eligibility."""
    return {"pnr": pnr, "fare_usd": 420.0, "refundable": True, "penalty_usd": 50.0}

@tool
def process_refund(pnr: str, amount_usd: float) -> dict:
    """Process a refund for a booking. Returns a confirmation id."""
    return {"pnr": pnr, "refunded_usd": amount_usd, "confirmation": "RF-" + pnr}

# Port: AgentCore expects 9000 in the deployed container, so default to it.
# Locally we set PORT=9005 to dodge clashes. PORT drives both the bind and the card url.
PORT = int(os.environ.get("PORT", "9000"))

# Addition 1: advertise the real URL when AgentCore sets it; fall back to the local port.
runtime_url = os.environ.get("AGENTCORE_RUNTIME_URL", f"http://127.0.0.1:{PORT}/")

agent = Agent(
    name="Refund Agent",
    description="Handles airline refund eligibility and processing.",
    model=BedrockModel(model_id="us.anthropic.claude-haiku-4-5-20251001-v1:0"),
    tools=[look_up_booking, process_refund],
    callback_handler=None,
)

a2a_server = A2AServer(agent=agent, http_url=runtime_url, serve_at_root=True)

app = FastAPI()

# Addition 2: health check for the AgentCore container.
@app.get("/ping")
def ping():
    return {"status": "healthy"}

# Addition 3: mount the A2A app at root.
app.mount("/", a2a_server.to_fastapi_app())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
