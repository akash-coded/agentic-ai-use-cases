
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands import Agent
from strands.models import BedrockModel

# --- build time: constructed once ---
MODEL_ID = "us.anthropic.claude-haiku-4-5-20251001-v1:0"
agent = Agent(
    model=BedrockModel(model_id=MODEL_ID, region_name="us-east-1"),
    system_prompt="You are TravelMind, an airline support agent. Be concise and accurate.",
)

app = BedrockAgentCoreApp()

# --- serve time: tiny entrypoint, runs the already-built agent once ---
@app.entrypoint
def invoke(payload, context=None):
    user_message = payload.get("prompt", "How can I help?")
    result = agent(user_message)
    return {"result": result.message}

if __name__ == "__main__":
    app.run()   # serves /invocations and /ping on :8080
