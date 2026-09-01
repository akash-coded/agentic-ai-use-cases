# TravelMind Agent Builder — Action Groups, Lambda, Permissions, Return of Control

Build runbook. Companion to the Day 5 deck and notebook. Every field, body, policy, and step, in order. Nothing skipped.

---

## Fixed identifiers used throughout

| Name | Value |
|---|---|
| Account ID | `123456789012` |
| Region | `us-east-1` |
| Model (inference profile) | `us.anthropic.claude-haiku-4-5-20251001-v1:0` |
| Inference profile ARN | `arn:aws:bedrock:us-east-1:123456789012:inference-profile/us.anthropic.claude-haiku-4-5-20251001-v1:0` |
| Foundation model ARN (for the role) | `arn:aws:bedrock:*::foundation-model/anthropic.claude-haiku-4-5-20251001-v1:0` |
| Agent name | `travelmind-desk` |
| Agent ID | generated at create time, call it `AGENT_ID` |
| Agent ARN | `arn:aws:bedrock:us-east-1:123456789012:agent/AGENT_ID` |
| Tools Lambda (manual path) | `travelmind-tools` |
| Tools Lambda ARN | `arn:aws:lambda:us-east-1:123456789012:function:travelmind-tools` |
| Lambda execution role | `travelmind-lambda-role` |

Two action groups get built:

| Action group | Executor | Functions | Why |
|---|---|---|---|
| `travelmind-actions` | Lambda | `check_entitlements`, `get_booking` | self-contained rules and a lookup, run them in AWS |
| `travelmind-rebooking` | Return of Control | `rebook_flight` | writes to the reservation system your app already owns, and it is irreversible |

**The rule that dictates this split:** the executor is set on the action group, not the function, and it is one or the other. A single action group is either Lambda backed or Return of Control backed. You cannot mix. That is the only reason `rebook_flight` sits in its own group.

---

## 0. Prerequisites

1. Region is `us-east-1` in the console top right.
2. Model access is enabled. Bedrock console, **Model access**, enable **Claude Haiku 4.5** for `us-east-1`. Haiku 4.5 is reachable only through the `us.` cross region inference profile. A bare model id can be rejected.
3. The agent `travelmind-desk` exists. If not, Bedrock console, **Builder tools**, **Agents**, **Create agent**, name it `travelmind-desk`, pick **Create and use a new service role** (this wires the agent role, Door 1), select the Haiku 4.5 inference profile, paste your instructions, **Save**.

Two hard limits to remember:

- A function takes **at most 5 parameters**.
- Every parameter value arrives at your code as a **string**, even numbers. You cast them.

---

# PART A — Action group 1, Lambda, quick created

## A1. Create the action group and quick create the Lambda

1. Open the agent `travelmind-desk`. Choose **Edit in Agent Builder** if you are on the overview.
2. Scroll to **Action groups**, choose **Add**.
3. **Action group name:** `travelmind-actions`.
4. **Action group type:** choose **Define with function details**. (The other option, Define with API schemas, is the OpenAPI path. You are not using it.)
5. **Action group invocation:** choose **Quick create a new Lambda function - recommended**. This creates a Lambda, its execution role, and both permission doors for you.
6. **Action group function 1:**
   - **Name:** `check_entitlements`
   - **Description:** `Decide meal and hotel voucher eligibility from the delay hours and the fare class.`
   - **Parameters**, choose **Add parameter** twice:

   | Parameter | Description | Type | Required |
   |---|---|---|---|
   | `delay_hours` | Whole or decimal hours of delay, for example 7 | Number | True |
   | `fare_class` | Fare class such as SAVER, FLEX, BUSINESS, FIRST | String | True |

7. Choose **Add action group function** to add the second function in the same group:
   - **Name:** `get_booking`
   - **Description:** `Look up a passenger booking by its PNR and return the itinerary and status.`
   - **Parameters:**

   | Parameter | Description | Type | Required |
   |---|---|---|---|
   | `pnr` | Six character booking reference, for example JX48Q2 | String | True |

8. Choose **Create**. The console provisions the Lambda. Note the function name it generates, usually derived from the action group.

## A2. The two functions as JSON

This is exactly what the console form above encodes. The same JSON is what the API and CLI use for this action group.

```json
{
  "functions": [
    {
      "name": "check_entitlements",
      "description": "Decide meal and hotel voucher eligibility from the delay hours and the fare class.",
      "requireConfirmation": "DISABLED",
      "parameters": {
        "delay_hours": {
          "type": "number",
          "description": "Whole or decimal hours of delay, for example 7",
          "required": true
        },
        "fare_class": {
          "type": "string",
          "description": "Fare class such as SAVER, FLEX, BUSINESS, FIRST",
          "required": true
        }
      }
    },
    {
      "name": "get_booking",
      "description": "Look up a passenger booking by its PNR and return the itinerary and status.",
      "requireConfirmation": "DISABLED",
      "parameters": {
        "pnr": {
          "type": "string",
          "description": "Six character booking reference, for example JX48Q2",
          "required": true
        }
      }
    }
  ]
}
```

Field notes: `type` is one of `string`, `number`, `integer`, `boolean`, `array`. `required` is a boolean. `requireConfirmation` is `DISABLED` here because these two functions only read, they change nothing.

## A3. The Lambda body

Open the created Lambda (there is a link on the action group, or Lambda console). Replace the entire stub in `lambda_function.py` with this, then choose **Deploy**. This one handler serves both functions by reading `event["function"]`.

```python
import json

# ---- tools -------------------------------------------------------------

def check_entitlements(delay_hours, fare_class):
    hours = float(delay_hours)                    # arrives as a string, cast it
    fare = fare_class.strip().upper()
    return {
        "meal_voucher":  hours >= 2,              # 2h or more gets a meal
        "hotel_voucher": hours >= 6,              # 6h or more gets a hotel
        "priority_rebooking": fare in ("FLEX", "BUSINESS", "FIRST"),
        "delay_hours": hours,
        "fare_class": fare,
    }

def get_booking(pnr):
    code = pnr.strip().upper()
    bookings = {
        "JX48Q2": {
            "pnr": "JX48Q2", "origin": "BLR", "destination": "SIN",
            "fare_class": "FLEX", "flight": "TM482", "status": "CANCELLED",
        },
    }
    if code not in bookings:
        return {"error": "PNR not found. Ask the passenger to recheck the six character code."}
    return bookings[code]

DISPATCH = {
    "check_entitlements": check_entitlements,
    "get_booking": get_booking,
}

# ---- the contract ------------------------------------------------------

def lambda_handler(event, context):
    action_group = event["actionGroup"]
    function     = event["function"]
    params       = {p["name"]: p["value"] for p in event.get("parameters", [])}

    response_state = None                         # None means success
    try:
        fn = DISPATCH.get(function)
        if fn is None:
            result = {"error": "unknown function: " + str(function)}
            response_state = "FAILURE"            # abort this turn
        else:
            result = fn(**params)                 # param names must match the schema
    except Exception as exc:
        result = {"error": str(exc)}              # never let the handler raise
        response_state = "REPROMPT"               # bad input, let the model try again

    function_response = {"responseBody": {"TEXT": {"body": json.dumps(result)}}}
    if response_state:
        function_response["responseState"] = response_state

    return {
        "messageVersion": "1.0",
        "response": {
            "actionGroup": action_group,          # echo, never hardcode
            "function": function,                 # echo, never hardcode
            "functionResponse": function_response,
        },
        "sessionAttributes": event.get("sessionAttributes", {}),
        "promptSessionAttributes": event.get("promptSessionAttributes", {}),
    }
```

The five things this body gets right, which are the five ways a first Lambda breaks:

1. `body` is a **string**, built with `json.dumps(...)`, never a raw dict.
2. Content type is `TEXT`. That is the only supported key inside `responseBody`.
3. `actionGroup` and `function` are echoed back from the event, not hardcoded.
4. `delay_hours` is cast with `float(...)` because it arrives as `"7"`.
5. The handler never raises. On a bad call it returns a structured error and sets `responseState` to `FAILURE` or `REPROMPT`. Omit `responseState` on success, do not set it to `SUCCESS`, that value is not valid.

While you are in the Lambda console, set a sane **timeout** (30 seconds) and leave memory at 128 MB. The quick create default timeout is often only a few seconds.

## A4. What quick create wired, and how to verify

Quick create opens both doors for you. Confirm them so you know what to reproduce for the existing Lambda path later.

**Door 1, the agent service role.** Agent overview, **Permissions**, open the service role. It has `bedrock:InvokeModel` on the model and `lambda:InvokeFunction` on this Lambda.

**Door 2, the Lambda resource policy.** Lambda console, the function, **Configuration**, **Permissions**, **Resource based policy statements**. There is a statement allowing `bedrock.amazonaws.com` to invoke, scoped by `SourceArn` to this agent. CLI check:

```bash
aws lambda get-policy --function-name <the-quick-created-name> --region us-east-1
```

## A5. Prove it

**In the Lambda console.** Create a test event named `check7h` with this payload, then **Test**. This is the exact shape Bedrock sends.

```json
{
  "messageVersion": "1.0",
  "actionGroup": "travelmind-actions",
  "function": "check_entitlements",
  "parameters": [
    {"name": "delay_hours", "type": "number", "value": "7"},
    {"name": "fare_class", "type": "string", "value": "FLEX"}
  ],
  "sessionAttributes": {},
  "promptSessionAttributes": {}
}
```

Expected response body decodes to `{"meal_voucher": true, "hotel_voucher": true, "priority_rebooking": true, ...}`.

**In the agent.** Back on the agent, **Save**, then **Prepare**. Open the test window and ask: `My flight was delayed 7 hours on a FLEX fare. What am I owed?` If the window reports the Lambda response failed, you broke the contract in A3, not the permissions.

---

# PART B — The same action group with an EXISTING Lambda

Use this path when the function already exists, or you deploy Lambdas from CI rather than clicking. You do the two things quick create did for you: create the function, and open Door 2 yourself.

## B1. Create the Lambda execution role

Every Lambda needs a role that lets it write logs. This is separate from the agent role.

**Console:** IAM, **Roles**, **Create role**, trusted entity **AWS service**, use case **Lambda**, attach **AWSLambdaBasicExecutionRole**, name it `travelmind-lambda-role`.

**CLI:**

```bash
aws iam create-role \
  --role-name travelmind-lambda-role \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "lambda.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

aws iam attach-role-policy \
  --role-name travelmind-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

IAM is eventually consistent. Wait about 10 seconds before using the role.

## B2. Create the Lambda and deploy the code

Put the exact body from A3 in a file named `lambda_function.py`.

**Console:** Lambda, **Create function**, **Author from scratch**, name `travelmind-tools`, runtime **Python 3.12**, under **Change default execution role** choose **Use an existing role** and pick `travelmind-lambda-role`, **Create function**. Paste the A3 code, **Deploy**. Set **Timeout** to 30 seconds in **Configuration**, **General configuration**.

**CLI:**

```bash
zip function.zip lambda_function.py

aws lambda create-function \
  --function-name travelmind-tools \
  --runtime python3.12 \
  --role arn:aws:iam::123456789012:role/travelmind-lambda-role \
  --handler lambda_function.lambda_handler \
  --timeout 30 --memory-size 128 \
  --zip-file fileb://function.zip \
  --region us-east-1
```

If you get `The role defined for the function cannot be assumed by Lambda`, the role has not propagated. Wait and retry. To update code later:

```bash
aws lambda update-function-code \
  --function-name travelmind-tools \
  --zip-file fileb://function.zip --region us-east-1
```

## B3. Open Door 2 yourself, the Lambda resource policy

This is the step quick create did for you and the one people forget with an existing Lambda. It lets Bedrock invoke your function, scoped to this exact agent so no other Bedrock agent in the account can call it.

You need the agent ARN. It is on the agent overview, or:

```bash
aws bedrock-agent get-agent --agent-id AGENT_ID --region us-east-1 \
  --query 'agent.agentArn' --output text
```

**CLI:**

```bash
aws lambda add-permission \
  --function-name travelmind-tools \
  --statement-id allow-bedrock-agent \
  --action lambda:InvokeFunction \
  --principal bedrock.amazonaws.com \
  --source-account 123456789012 \
  --source-arn arn:aws:bedrock:us-east-1:123456789012:agent/AGENT_ID \
  --region us-east-1
```

**Console equivalent:** Lambda, the function, **Configuration**, **Permissions**, **Resource based policy statements**, **Add permissions**, **AWS service**, service **Other**, principal `bedrock.amazonaws.com`, source ARN the agent ARN, action `lambda:InvokeFunction`, statement id `allow-bedrock-agent`.

The statement this produces:

```json
{
  "Sid": "allow-bedrock-agent",
  "Effect": "Allow",
  "Principal": {"Service": "bedrock.amazonaws.com"},
  "Action": "lambda:InvokeFunction",
  "Resource": "arn:aws:lambda:us-east-1:123456789012:function:travelmind-tools",
  "Condition": {
    "StringEquals": {"AWS:SourceAccount": "123456789012"},
    "ArnLike": {"AWS:SourceArn": "arn:aws:bedrock:us-east-1:123456789012:agent/AGENT_ID"}
  }
}
```

## B4. Attach the existing Lambda to the action group

If you have not created the action group yet, follow A1 but at **Action group invocation** choose **Select an existing Lambda function** and pick `travelmind-tools`, then add the two functions exactly as in A1 and A2. If the action group already exists from the quick create path, edit it and switch its Lambda to `travelmind-tools`.

## B5. Confirm Door 1 on the agent role

Attaching an existing Lambda does not always add the invoke permission to your agent role, and it never does if you brought your own role. Verify it, and add it if missing.

- If the agent uses a **console managed** service role, saving the agent usually adds `lambda:InvokeFunction` for the attached function. Open the role and confirm.
- If the agent uses **your own** role, add this statement to the agent role:

```json
{
  "Sid": "InvokeLambda",
  "Effect": "Allow",
  "Action": "lambda:InvokeFunction",
  "Resource": "arn:aws:lambda:us-east-1:123456789012:function:travelmind-tools"
}
```

Then on the agent, **Save**, **Prepare**, and test as in A5.

**Quick create versus existing Lambda, when to use which**

| | Quick create | Existing Lambda |
|---|---|---|
| Door 1 (agent role invoke) | done for you | verify, add if missing |
| Door 2 (resource policy) | done for you | you add it, always |
| Function code | paste, deploy | pre deployed by you or CI |
| Best for | first build, learning | shared function, IaC, CI pipelines |

---

# PART C — Action group 2, Return of Control, rebook_flight

Return of Control hands the tool call back to your application instead of running a Lambda. Reach for it when the action lives in a system your app already talks to, when it can run past the 15 minute Lambda ceiling, when it is async, or when it sits in a private network. Rebooking is all of the above, and it is irreversible, so you also gate it behind a confirmation.

## C1. Create the Return of Control action group

1. On the agent, **Action groups**, **Add**.
2. **Action group name:** `travelmind-rebooking`.
3. **Action group type:** **Define with function details**.
4. **Action group invocation:** choose **Return control**. No Lambda is created or selected for this group.
5. **Action group function 1:**
   - **Name:** `rebook_flight`
   - **Description:** `Rebook a passenger onto a new flight after a disruption. This writes to the reservation system, so it must be confirmed by the passenger first.`
   - **Parameters:**

   | Parameter | Description | Type | Required |
   |---|---|---|---|
   | `pnr` | Six character booking reference to rebook | String | True |
   | `new_flight` | The replacement flight number, for example TM620 | String | True |

   - **User confirmation:** turn this **on** (`requireConfirmation` = `ENABLED`). This forces a confirm or deny before the action is treated as done, which protects against a rebooking triggered by a prompt injection.
6. Choose **Create**.

## C2. The function as JSON

```json
{
  "functions": [
    {
      "name": "rebook_flight",
      "description": "Rebook a passenger onto a new flight after a disruption. This writes to the reservation system, so it must be confirmed by the passenger first.",
      "requireConfirmation": "ENABLED",
      "parameters": {
        "pnr": {
          "type": "string",
          "description": "Six character booking reference to rebook",
          "required": true
        },
        "new_flight": {
          "type": "string",
          "description": "The replacement flight number, for example TM620",
          "required": true
        }
      }
    }
  ]
}
```

## C3. What changes with Return of Control

- **No Lambda.** Nothing to deploy for this group.
- **No resource policy, no Door 2.** Bedrock never calls anything on your side, it returns the request to your `invoke_agent` caller.
- **Door 1 stays.** The agent still needs `bedrock:InvokeModel` to run the model. No `lambda:InvokeFunction` is needed for this group because there is no Lambda.
- **Your calling code does the work.** When the agent decides to call `rebook_flight`, `invoke_agent` returns a `returnControl` event instead of a chunk. You execute the function in your app and call `invoke_agent` again with the result.

## C4. The invoke loop that makes it work

This is the full pattern. It reads the `returnControl` event, honors the confirmation, executes the function in your app, and resumes the same session with the result.

```python
import json, uuid, boto3

rt = boto3.client("bedrock-agent-runtime", region_name="us-east-1")

# The actual work. In production this calls the reservation system or a human queue.
def rebook_flight(pnr, new_flight):
    return {
        "pnr": pnr,
        "rebooked_to": new_flight,
        "new_pnr": "JX9F3K",
        "status": "CONFIRMED",
        "note": "Seat assigned, passenger notified by email.",
    }

ROC = {"rebook_flight": rebook_flight}

def ask_the_passenger(fi):
    # Your UI. Show fi["function"] and fi["parameters"], return True on approve.
    return True

def run(agent_id, alias_id, prompt, session_id=None):
    session_id = session_id or uuid.uuid4().hex
    resp = rt.invoke_agent(
        agentId=agent_id, agentAliasId=alias_id,
        sessionId=session_id, inputText=prompt)

    while True:
        answer, rc = "", None
        for ev in resp["completion"]:
            if "chunk" in ev:
                answer += ev["chunk"]["bytes"].decode()
            elif "returnControl" in ev:
                rc = ev["returnControl"]

        if rc is None:
            return answer                         # agent finished normally

        # The agent handed control back. Build a result for each requested call.
        results = []
        for item in rc["invocationInputs"]:
            fi = item["functionInvocationInput"]
            args = {p["name"]: p["value"] for p in fi.get("parameters", [])}
            kind = fi.get("actionInvocationType", "RESULT")

            entry = {"actionGroup": fi["actionGroup"], "function": fi["function"]}

            if kind == "USER_CONFIRMATION":       # requireConfirmation was ENABLED
                approved = ask_the_passenger(fi)
                entry["confirmationState"] = "CONFIRM" if approved else "DENY"
                if approved:
                    out = ROC[fi["function"]](**args)
                    entry["responseBody"] = {"TEXT": {"body": json.dumps(out)}}
                else:
                    entry["responseBody"] = {"TEXT": {"body": "Passenger declined the rebooking."}}
            else:                                 # RESULT, run it and return the output
                out = ROC[fi["function"]](**args)
                entry["responseBody"] = {"TEXT": {"body": json.dumps(out)}}

            results.append({"functionResult": entry})

        # Resume the SAME session with the results. Send no inputText this time.
        resp = rt.invoke_agent(
            agentId=agent_id, agentAliasId=alias_id, sessionId=session_id,
            sessionState={
                "invocationId": rc["invocationId"],          # must match the event
                "returnControlInvocationResults": results,
            })
```

Three things that must be exact, or the resume fails:

1. **Same `sessionId`** as the first call. A new session loses the pending action.
2. **Same `invocationId`** that came in the `returnControl` event, echoed in `sessionState`.
3. **No `inputText`** on the resume call. If `returnControlInvocationResults` is present, `inputText` is ignored, so passing it is a sign you built the call wrong.

## C5. What the two payloads look like

**What the agent returns to you** (inside the `completion` stream):

```json
{
  "returnControl": {
    "invocationId": "79e0feaa-c6f7-49bf-814d-b7c498505172",
    "invocationInputs": [
      {
        "functionInvocationInput": {
          "actionGroup": "travelmind-rebooking",
          "function": "rebook_flight",
          "actionInvocationType": "USER_CONFIRMATION",
          "parameters": [
            {"name": "pnr", "type": "string", "value": "JX48Q2"},
            {"name": "new_flight", "type": "string", "value": "TM620"}
          ]
        }
      }
    ]
  }
}
```

**What you send back** in the second `invoke_agent` call:

```json
{
  "invocationId": "79e0feaa-c6f7-49bf-814d-b7c498505172",
  "returnControlInvocationResults": [
    {
      "functionResult": {
        "actionGroup": "travelmind-rebooking",
        "function": "rebook_flight",
        "confirmationState": "CONFIRM",
        "responseBody": {
          "TEXT": {"body": "{\"status\": \"CONFIRMED\", \"new_pnr\": \"JX9F3K\"}"}
        }
      }
    }
  ]
}
```

Notes: `confirmationState` is only meaningful when `requireConfirmation` is `ENABLED`. With confirmation `DISABLED`, the event carries `actionInvocationType` of `RESULT`, you run the function and return `responseBody` with no `confirmationState`. On a `DENY`, the agent does not treat the function as executed and continues from that fact.

## C6. Prepare and test

On the agent, **Save**, **Prepare**. Then drive it through your `run(...)` loop with a prompt such as: `PNR JX48Q2, please rebook me on TM620.` You will see one `returnControl` round trip, your confirmation, then the final answer built from the result you returned.

---

# PART D — Prepare, version, alias, ship

1. **Prepare.** After any change to instructions, action groups, functions, or the Lambda wiring, choose **Prepare** on the agent. Skip this and the running agent does not see your change. The test window runs a hidden draft alias, `TSTALIASID`.
2. **Version.** When you are happy, create a version. It is a frozen snapshot.
3. **Alias.** Create an alias, for example `live`, pointing at that version. Your application calls the alias, never the draft.
4. As you iterate, move the alias to new versions. The alias is a git tag your deploy tracks.

---

# PART E — Permissions reference

## Door 1, the agent service role

**Trust policy** (who can assume the role). If you let the console create the role, this is done. For your own role:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {"Service": "bedrock.amazonaws.com"},
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {"aws:SourceAccount": "123456789012"},
        "ArnLike": {"aws:SourceArn": "arn:aws:bedrock:us-east-1:123456789012:agent/*"}
      }
    }
  ]
}
```

**Permission policy** (what the agent may do). Scope to specific ARNs, no wildcards on the action side:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "InvokeModel",
      "Effect": "Allow",
      "Action": ["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"],
      "Resource": [
        "arn:aws:bedrock:us-east-1:123456789012:inference-profile/us.anthropic.claude-haiku-4-5-20251001-v1:0",
        "arn:aws:bedrock:*::foundation-model/anthropic.claude-haiku-4-5-20251001-v1:0"
      ]
    },
    {
      "Sid": "InvokeLambda",
      "Effect": "Allow",
      "Action": "lambda:InvokeFunction",
      "Resource": "arn:aws:lambda:us-east-1:123456789012:function:travelmind-tools"
    }
  ]
}
```

The `InvokeLambda` statement is only needed if the agent has a Lambda backed action group. The Return of Control group needs no Lambda permission. For a cross region inference profile you allow the profile ARN plus the underlying foundation model ARN, which is why both entries appear under `InvokeModel`.

If you want the role to show up in the console `Use an existing service role` dropdown, name it with the prefix `AmazonBedrockExecutionRoleForAgents_`. Created through the API, any name works, as long as the trust policy is correct.

## Door 2, the Lambda resource policy

Only for Lambda backed groups. Scoped to this agent so no other Bedrock agent can invoke your function. The exact statement is in B3. Never drop the `SourceArn` condition.

## The caller policy

Whatever runs `invoke_agent`, an app, a service, a script, gets only this, on the one alias, not full access:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "bedrock:InvokeAgent",
      "Resource": "arn:aws:bedrock:us-east-1:123456789012:agent-alias/AGENT_ID/ALIAS_ID"
    }
  ]
}
```

## The IAM action truth people trip on

`bedrock:Converse` is not a valid IAM action. `bedrock:InvokeModel` already covers the agent calling the model. Do not add `Converse` to the role.

---

# PART F — Build both groups in code

If you prefer code over clicking, these two calls create the groups. The Lambda, its role, and Door 2 for the first group are created exactly as in Part B.

```python
# Action group 1: Lambda backed, two functions
bedrock_agent.create_agent_action_group(
    agentId=AGENT_ID, agentVersion="DRAFT",
    actionGroupName="travelmind-actions",
    actionGroupState="ENABLED",
    actionGroupExecutor={"lambda": "arn:aws:lambda:us-east-1:123456789012:function:travelmind-tools"},
    functionSchema={"functions": [
        {
            "name": "check_entitlements",
            "description": "Decide meal and hotel voucher eligibility from the delay hours and the fare class.",
            "requireConfirmation": "DISABLED",
            "parameters": {
                "delay_hours": {"type": "number", "description": "Whole or decimal hours of delay, for example 7", "required": True},
                "fare_class":  {"type": "string", "description": "Fare class such as SAVER, FLEX, BUSINESS, FIRST", "required": True},
            },
        },
        {
            "name": "get_booking",
            "description": "Look up a passenger booking by its PNR and return the itinerary and status.",
            "requireConfirmation": "DISABLED",
            "parameters": {
                "pnr": {"type": "string", "description": "Six character booking reference, for example JX48Q2", "required": True},
            },
        },
    ]},
)

# Action group 2: Return of Control, one function, confirmation on
bedrock_agent.create_agent_action_group(
    agentId=AGENT_ID, agentVersion="DRAFT",
    actionGroupName="travelmind-rebooking",
    actionGroupState="ENABLED",
    actionGroupExecutor={"customControl": "RETURN_CONTROL"},   # no lambda key
    functionSchema={"functions": [
        {
            "name": "rebook_flight",
            "description": "Rebook a passenger onto a new flight after a disruption. This writes to the reservation system, so it must be confirmed by the passenger first.",
            "requireConfirmation": "ENABLED",
            "parameters": {
                "pnr":        {"type": "string", "description": "Six character booking reference to rebook", "required": True},
                "new_flight": {"type": "string", "description": "The replacement flight number, for example TM620", "required": True},
            },
        },
    ]},
)

bedrock_agent.prepare_agent(agentId=AGENT_ID)   # required after every change
```

`actionGroupExecutor` is a tagged union. Set `lambda` or `customControl`, never both. That single field is the whole difference between a Lambda group and a Return of Control group.

---

# PART G — Do not skip checklist

- One executor per action group. Lambda backed and Return of Control functions cannot share a group.
- `Prepare` after every change, or the running agent does not see it.
- Every parameter arrives as a string. Cast numbers yourself.
- Lambda response: string `body` under `TEXT`, echo `actionGroup` and `function`, omit `responseState` on success, set `FAILURE` or `REPROMPT` on error. `SUCCESS` is not a valid value.
- Existing Lambda: you always add Door 2, the resource policy, with a `SourceArn` scoped to the agent.
- Return of Control: same `sessionId`, same `invocationId`, and no `inputText` on the resume call.
- Confirmation is per function, `requireConfirmation` `ENABLED`. For Return of Control, confirm or deny comes back in `functionResult.confirmationState`.
- Haiku 4.5 is reachable only through the `us.` inference profile. Enable model access in `us-east-1`.
- At most 5 parameters per function.
- Keep function names snake case so they map cleanly to your Python dispatch.
