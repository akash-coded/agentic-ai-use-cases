"""TravelMind flight-status agent, packaged for AgentCore Runtime."""
from bedrock_agentcore import BedrockAgentCoreApp          # <-- 1) the runtime app
from strands import Agent, tool

MODEL_HAIKU = "us.anthropic.claude-haiku-4-5-20251001-v1:0"

FLIGHTS = {
    "BA117": {"flight": "BA117", "status": "Delayed", "from": "LHR", "to": "JFK", "delay_min": 75},
    "AA100": {"flight": "AA100", "status": "On time", "from": "JFK", "to": "LHR", "delay_min": 0},
    "AI191": {"flight": "AI191", "status": "Cancelled", "from": "DEL", "to": "SFO", "delay_min": None},
}

@tool
def get_flight_status(flight_number: str) -> dict:
    """Look up the current status of a flight by its flight number (e.g. BA117)."""
    return FLIGHTS.get(flight_number.upper().replace(" ", ""), {"status": "Unknown flight"})

agent = Agent(
    model=MODEL_HAIKU,
    tools=[get_flight_status],
    system_prompt="You are TravelMind, a flight status assistant. Use the tool, then answer plainly.",
)

app = BedrockAgentCoreApp()                                # <-- 2) create the app

@app.entrypoint                                            # <-- 3) this fn handles /invocations
def invoke(payload):
    user_message = payload.get("prompt", "")
    result = agent(user_message)
    return {"result": str(result)}

if __name__ == "__main__":
    app.run()                                              # serve locally on :8080
