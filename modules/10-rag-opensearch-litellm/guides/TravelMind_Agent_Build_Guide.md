# TravelMind Trip Helper - Agent Build Guide (Bulletproof Edition)

**Individual hands-on · ~60-75 min · Region `us-east-1` · Model: Amazon Nova Lite v1.0 (`amazon.nova-lite-v1:0`, on-demand)**

You will build one Bedrock agent and one simple Lambda, connect them with a function-based action group, then read the agent's trace to see how it reasons, routes to a tool, and handles a request it cannot serve.

---

## Read this first - 4 habits that prevent almost every error

1. **Stay in `us-east-1`.** The Lambda and the agent must be in the same region. Check the region selector (top-right) before you create anything.
2. **Model is Nova Lite v1.0** - `amazon.nova-lite-v1:0`. Do not switch models.
3. **Prepare and Deploy are different buttons.** After any change to the agent or action group, click **Prepare**. After pasting Lambda code, click **Deploy**. Forgetting these is the No. 1 "it didn't change" problem.
4. **Do not edit the Lambda return envelope.** Bedrock requires an exact shape and the content type must be `TEXT`. Change the tool logic, never the wrapper.

---

## Part A - Create the Lambda

1. Console → Lambda → **Create function** → **Author from scratch**.
2. Name: `travelmind-tools`. Runtime: **Python 3.12** (or latest Python).
3. **Execution role:** leave the default **"Create a new role with basic Lambda permissions."** (If your instructor gave you a shared role, you may pick it instead under "Use an existing role" - either works.)
4. Click **Create function**.
5. In the code editor, replace everything with the scaffold in Part B and complete the three TODOs.
6. Click **Deploy**.
7. (Optional) Configuration → General configuration → set Timeout to 15 sec. The stub code is fast, but this avoids surprises.

Keep the default file name `lambda_function.py` and handler `lambda_function.lambda_handler`. If you rename the file, update the handler to match, or you will get a handler error.

---

## Part B - The Lambda code

The return envelope is given - use it exactly. Implement the two TODO tools (copy the `get_weather` pattern) and the **exit/fallback** branch.

```python
import json

# helper: pull a named parameter the agent sent
def get_param(parameters, name, default=None):
    for p in parameters or []:
        if p.get("name") == name:
            return p.get("value", default)
    return default

# --- tool 1: WORKED EXAMPLE (study this pattern) ---
WEATHER = {
    "goa": "32C, humid, light rain likely",
    "leh": "12C, cold and dry, strong sun",
    "bengaluru": "26C, pleasant, light breeze",
}
def get_weather(parameters):
    city = (get_param(parameters, "city") or "").strip().lower()
    if city in WEATHER:
        return f"Weather in {city.title()}: {WEATHER[city]}."
    return f"No weather data for '{city}'. Supported: {', '.join(c.title() for c in WEATHER)}."

# --- tool 2: TODO - implement like get_weather ---
def suggest_packing(parameters):
    # read 'city' and optional 'trip_type' (default 'leisure')
    # build a short packing list (a few items); adjust for city + trip_type
    # return one readable string
    raise NotImplementedError

# --- tool 3: TODO ---
def get_local_time(parameters):
    # read 'city', look up its time zone, return a readable string
    raise NotImplementedError

TOOLS = {
    "get_weather": get_weather,
    "suggest_packing": suggest_packing,
    "get_local_time": get_local_time,
}

def lambda_handler(event, context):
    function = event.get("function", "")
    parameters = event.get("parameters", [])

    if function in TOOLS:
        body = TOOLS[function](parameters)
    else:
        # TODO (EXIT / FALLBACK): the agent asked for a tool that does not exist.
        # Return a clear message that names what IS available, so the agent relays it.
        body = ""  # replace this

    # Return EXACTLY this shape. Bedrock Agents require it. Content type must be "TEXT".
    return {
        "messageVersion": "1.0",
        "response": {
            "actionGroup": event.get("actionGroup", ""),
            "function": function,
            "functionResponse": {
                "responseBody": {"TEXT": {"body": body}}
            }
        },
        "sessionAttributes": event.get("sessionAttributes", {}),
        "promptSessionAttributes": event.get("promptSessionAttributes", {}),
    }
```

The `else` branch is your **exit function** - it runs when the model calls a tool that is not in `TOOLS`. It must return a useful "not available" message, never crash and never stay empty.

---

## Part C - Create the agent

1. Console → Amazon Bedrock → **Agents** → **Create agent**. Name: `travelmind-trip-helper`.
2. **Model: Nova Lite v1.0** (`amazon.nova-lite-v1:0`).
3. **Agent service role:** choose **"Create and use a new service role."**
4. **Instructions** (paste this):

> You are TravelMind Trip Helper, an assistant for travellers preparing for a trip. You can do three things: report the weather for a city, suggest a packing list, and give the local time zone for a city. Always use the available tools to answer. If the user asks for anything outside these three abilities - for example booking or cancelling flights or hotels, payments, or visa help - tell them politely you can only help with weather, packing, and local time, and list what you can do. Keep answers short and practical.

5. Save.

---

## Part D - Action group (function details)

1. In the agent, add an **action group**. Type: **Define with function details** (not OpenAPI).
2. Action group invocation: **Select an existing Lambda function** → `travelmind-tools`.
3. Add these three functions exactly:

| Function | Parameters | Description (the model reads this - keep it clear) |
|---|---|---|
| `get_weather` | `city` (string, required) | Return current weather for a supported city. |
| `suggest_packing` | `city` (string, required), `trip_type` (string, optional) | Suggest a packing list based on the city and trip type (business or leisure). |
| `get_local_time` | `city` (string, required) | Return the local time zone for a supported city. |

4. Save the action group.

---

## Part E - Permission glue

When you selected the Lambda in the action group, the console usually adds a **resource-based policy** to the Lambda automatically so Bedrock can invoke it. If a test later fails with an invoke/AccessDenied error, see Troubleshooting rows 4 and 5.

---

## Part F - Prepare and test

Click **Prepare**. Then in the test panel, try:

1. `What's the weather in Goa?`
2. `I'm going to Leh on a leisure trip. What should I pack?`
3. `What's the local time zone in Bengaluru?`
4. `What's the weather in Goa and what should I pack for a business trip there?`
5. **Exit case:** `Book me a flight to Goa.`
6. **Exit case:** `Cancel my hotel in Leh.`

Prompts 1-4 should answer via your tools. Prompts 5-6 must produce a polite refusal that lists what the agent can do.

---

## Part G - Read the trace

Turn on **Show trace** in the test panel. Expand the orchestration steps and answer:

1. For prompt 4, what **rationale** did the agent state before calling a tool?
2. Which function(s) did it call, and with what parameter values? (the `invocationInput`)
3. What did the Lambda return? (the `observation`)
4. For the exit case (prompt 5), how was it handled - did the agent **call a tool and hit your fallback**, or **decline directly**? Quote the trace line that tells you.
5. Point to where the model is deciding between a tool and answering on its own.

---

## Part H - Extension (optional, if you finish early)

Add a fourth tool end to end: `get_currency(city)` returning the local currency for a supported city. Add it to `TOOLS`, add the matching function in the action group, Prepare, test. Confirm your exit branch still handles a made-up tool like `get_visa_rules`.

---

## Definition of done

- All three tool prompts return correct, readable answers through the agent.
- Both exit prompts produce a graceful refusal, and you can show in the trace how the exit was handled.
- Your Lambda returns the exact required envelope (you did not touch the wrapper or change `TEXT`).
- Trace questions answered with evidence.

**Submit:** a screenshot of a successful tool answer (prompt 4), a trace excerpt for the exit case (prompt 5), your completed Lambda code, and your written answers to the six trace questions.

---

## Troubleshooting - the errors you will probably hit

| Symptom / message | Why it happens | Fix |
|---|---|---|
| `not authorized to perform: iam:CreateRole` while creating the Lambda | You let Lambda create a new execution role and your access didn't allow that role name | This is fixed in the lab policy - retry. If it persists, your instructor needs to push the policy update; meanwhile pick an existing role under "Use an existing role." |
| `not authorized to perform: iam:PassRole on resource .../role/...` | The execution role you selected isn't one you're allowed to hand to Lambda | Fixed in the lab policy - retry. If it persists, pick the role your instructor created, or use the default "Create a new role." |
| `The server encountered an error processing the Lambda response. Check the Lambda response and retry the request` | Your return JSON is malformed or used the wrong content type | Use the exact envelope from Part B. Content type must be `TEXT`, not `text/plain`. `messageVersion` must be `"1.0"`. |
| Agent test fails with an invoke error, or `not authorized ... lambda:InvokeFunction` | The agent's role can't call your Lambda, or the Lambda is missing its resource policy | In the action group, re-select the Lambda and save (this re-adds the Lambda resource policy). If still failing, add `lambda:InvokeFunction` on your function to the agent's service role. |
| Agent answers from its own knowledge and never calls a tool | Function descriptions are too vague, or you didn't Prepare | Make the descriptions specific (Part D), click **Prepare**, test again. |
| Model error like `on-demand throughput isn't supported` | Wrong model or model-id form | Use Nova Lite v1.0 in `us-east-1`. If the builder only surfaces a cross-region profile, that still maps to Nova Lite - select it. |
| Action group can't find the Lambda, or the Lambda isn't listed | The Lambda is in a different region than the agent | Recreate the Lambda in `us-east-1`. Both must be in the same region. |
| Changes don't take effect / old behaviour persists | You didn't click **Prepare** (agent) or **Deploy** (Lambda), or you tested an old version | Deploy the Lambda, Prepare the agent, test the working draft. |
| Handler error in the Lambda logs (cannot find `lambda_handler`) | The handler name doesn't match the file | Keep file `lambda_function.py` and handler `lambda_function.lambda_handler`, or update the handler to match your file. |
| `KeyError` / "Insufficient parameters" reading parameters | You read parameters by position | Read by **name** with the `get_param` helper. The agent may reorder parameters or omit optional ones. |
| AccessDenied right after a policy was updated | IAM is eventually consistent | Wait 30-60 seconds and retry. If needed, sign out and back in. |
| Tool returns nothing / `NotImplementedError` | A TODO tool isn't implemented | Implement `suggest_packing`, `get_local_time`, and the exit branch. |
| No trace shown in the test panel | Trace is toggled off | Turn on **Show trace** in the test panel. |
| Lambda times out | Default timeout is 3 sec | Configuration → General configuration → raise Timeout to 15 sec. |

---

## Final checklist

- [ ] Region is `us-east-1` for both the Lambda and the agent
- [ ] Lambda created, code **Deployed**, all three TODOs done
- [ ] Action group type is **function details**, three functions defined, pointing at `travelmind-tools`
- [ ] Agent model is **Nova Lite v1.0**
- [ ] Clicked **Prepare**
- [ ] Tool prompts (1-4) return real answers
- [ ] Exit prompts (5-6) refuse gracefully
- [ ] Trace read and the six questions answered
