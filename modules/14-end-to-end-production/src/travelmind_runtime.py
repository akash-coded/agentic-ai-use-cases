"""
travelmind_runtime.py
=====================
The AgentCore Runtime entrypoint. This is the ONLY new code needed to turn the
working local agent into something AgentCore Runtime can host.

The contract you are honoring:
  - One app object: BedrockAgentCoreApp()
  - One entrypoint function decorated with @app.entrypoint, which receives the
    JSON request body (payload) and returns the response.
  - app.run() starts a server that exposes:
        POST /invocations   -> your entrypoint
        GET  /ping          -> health check
    on port 8080. Port 8080 is non-negotiable; it is how Runtime reaches you.

Run it locally (VS Code, 3 steps):
  1. python -m venv .venv && source .venv/bin/activate     # activate venv
  2. aws configure                                         # set creds (workshop)
  3. pip install -r requirements.txt                       # install deps
  then:  python travelmind_runtime.py

Test the running server from another terminal:
  curl localhost:8080/ping
  curl -X POST localhost:8080/invocations \
       -H 'Content-Type: application/json' \
       -d '{"prompt":"Status of PNR JX48Q2?"}'

No terminal (Colab) or no creds? You do not need to run the server to test the
logic. Import this file and call the entrypoint in-process:
      from travelmind_runtime import invoke
      print(invoke({"prompt": "Status of PNR JX48Q2?"}))
With LIVE=False (below) that path uses the offline mock and needs no AWS.
"""
import os

# LIVE flag: False uses the offline mock agent (no AWS). Set to "1" in the
# environment, or flip the default, when you have credentials and want the
# real model in the loop.
LIVE = os.environ.get("LIVE", "0") == "1"

# Import the agent pieces. The tool functions and mock are pure Python.
# build_agent()/get_agent() import Strands lazily, only used when LIVE is True.
from travelmind_agent import get_agent, mock_agent

# ----------------------------------------------------------------------------
# The AgentCore app. Importing bedrock_agentcore is guarded so this file can be
# imported for in-process testing even where the SDK is not installed. On a
# real deploy the SDK IS installed (it is in requirements.txt) and app is real.
# ----------------------------------------------------------------------------
try:
    from bedrock_agentcore.runtime import BedrockAgentCoreApp
    app = BedrockAgentCoreApp()
except Exception:                      # SDK not present (e.g. local notebook)
    app = None                          # the @app.entrypoint decorator below no-ops


def _entrypoint(payload):
    """The function AgentCore calls for every POST /invocations.

    payload is the parsed JSON request body, a dict. We read 'prompt' and return
    the agent's answer as a string. Returning a plain string is fine; a dict
    would be returned as JSON.

    What changes in production:
      - validate payload (missing/oversized 'prompt'), return a clean error
      - add a request id to every log line for tracing
      - wrap the agent call in a timeout and a retry on throttling
    """
    user_text = (payload or {}).get("prompt", "")
    if LIVE:
        return str(get_agent()(user_text))   # real model via Bedrock
    return mock_agent(user_text)             # offline, deterministic


# Register the entrypoint if the SDK is available; otherwise expose it plainly
# so `from travelmind_runtime import invoke` works for in-process tests.
if app is not None:
    invoke = app.entrypoint(_entrypoint)
else:
    invoke = _entrypoint


if __name__ == "__main__":
    if app is not None:
        # Starts the server on port 8080 (POST /invocations, GET /ping).
        # This call blocks; stop with Ctrl+C.
        app.run()
    else:
        # No SDK installed: demonstrate the entrypoint contract in-process.
        print("bedrock-agentcore not installed; running the entrypoint directly.\n")
        for q in ["Status of PNR JX48Q2?", "Rebook JX48Q2"]:
            print(q, "->", invoke({"prompt": q}))
