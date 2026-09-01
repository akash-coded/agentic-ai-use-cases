# Exercise 2: Model access, LiteLLM, orchestration

**Language:** Python (boto3-shaped), IAM JSON  **Topics:** inference profiles, IAM actions, LiteLLM prefixes, `drop_params`, chain vs graph vs agent  **Level:** foundational (read and spot code, no writing)

Second foundation. You read code and spot faults now, but write nothing. Predict-output answers are the exact printed result.

**Q1.** Predict the exact output.

```python
def model_string(caller, base="us.anthropic.claude-haiku-4-5-20251001-v1:0"):
    return ("bedrock/" + base) if caller == "litellm" else base

print(model_string("litellm"))
print(model_string("strands"))
```

- A) `bedrock/us.anthropic.claude-haiku-4-5-20251001-v1:0` then `us.anthropic.claude-haiku-4-5-20251001-v1:0`
- B) both lines print `us.anthropic.claude-haiku-4-5-20251001-v1:0`
- C) both lines print `bedrock/us.anthropic.claude-haiku-4-5-20251001-v1:0`
- D) `us.anthropic.claude-haiku-4-5-20251001-v1:0` then `bedrock/us.anthropic.claude-haiku-4-5-20251001-v1:0`

<details><summary>Show answer</summary>

**A)** LiteLLM needs the `bedrock/` prefix; Strands takes the bare `us.` profile.
</details>

**Q2.** An agent gets 403 on every call. Its IAM policy allows the actions below and nothing else. The minimal fix is:

```json
{ "Effect": "Allow",
  "Action": ["bedrock:Converse", "bedrock:ConverseStream"],
  "Resource": "arn:aws:bedrock:us-east-1::inference-profile/us.anthropic.claude-haiku-4-5-20251001-v1:0" }
```

- A) add the model's cross-region resource ARNs for every region the inference profile is allowed to span
- B) replace the actions with `bedrock:InvokeModel` and `bedrock:InvokeModelWithResponseStream`
- C) attach the policy to a role rather than to a user
- D) add `bedrock:CreateInferenceProfile` to the action list

<details><summary>Show answer</summary>

**B)** `Converse` and `ConverseStream` are API operations, not IAM actions, so they grant nothing. The grantable action is `InvokeModel`.
</details>

**Q3.** This call raises a ValidationException the moment the model is switched. The fix is:

```python
resp = client.converse(
    modelId="anthropic.claude-haiku-4-5-20251001-v1:0",
    messages=messages,
    inferenceConfig={"maxTokens": 400, "temperature": 0.0},
)
```

- A) set the client region to `us-east-1`, then resend the exact same bare model id string with no other change
- B) remove `temperature` from `inferenceConfig` so it stops conflicting
- C) prefix the id with the cross-region inference profile: `us.anthropic.claude-haiku-4-5-20251001-v1:0`
- D) call `invoke_model` instead, since `converse` rejects new model ids

<details><summary>Show answer</summary>

**C)** The bare id needs the mandatory `us.` profile. The symptom is a ValidationException on the id itself, not a region or config error.
</details>

**Q4.** Through LiteLLM a Bedrock call sets both `temperature` and `top_p` and raises an error. Setting `drop_params=True` results in:

- A) both parameters are dropped and provider defaults are used
- B) LiteLLM automatically retries the call with a lower `top_p`
- C) the call still fails, but the conflict is logged as a warning
- D) the unsupported parameter is dropped and the call succeeds

<details><summary>Show answer</summary>

**D)** `drop_params` drops the parameter Bedrock will not accept rather than throwing, so the call goes through.
</details>

**Q5.** A task branches on the input and sometimes retries a step, but never changes its plan based on what the model returns mid-run. The right orchestration is:

- A) graph
- B) chain
- C) agent loop
- D) multi-agent supervisor

<details><summary>Show answer</summary>

**A)** Known branches and retries on a fixed plan are a graph. An agent is only warranted when the model must choose the path.
</details>

**Q6.** Exactly one line is wrong. Which?

```python
1  client = boto3.client("bedrock-runtime", region_name="us-east-1")
2  resp = client.converse(
3      modelId="anthropic.claude-haiku-4-5-20251001-v1:0",
4      messages=messages,
5      toolConfig=TOOL_CONFIG,
6  )
```

- A) line 1, the client should target a different region for Haiku
- B) line 3, the model id is missing the `us.` inference profile
- C) line 5, `toolConfig` is not a valid argument to `converse`
- D) line 2, `converse` is deprecated in favour of `invoke_model`

<details><summary>Show answer</summary>

**B)** The id is bare. `toolConfig` is valid, the region is fine, and `converse` is current.
</details>

**Q7.** An embedding call fails to route to Bedrock. The fix is:

```python
litellm.embedding(model="amazon.titan-embed-text-v2:0", input=texts)
```

- A) downgrade to `amazon.titan-embed-text-v1`, since v2 is not yet supported on Bedrock
- B) pass `provider="bedrock"` as a separate keyword argument
- C) prefix the model with `bedrock/`: `bedrock/amazon.titan-embed-text-v2:0`
- D) wrap `input` in an extra list before sending it

<details><summary>Show answer</summary>

**C)** Under LiteLLM, the embeddings model also needs the `bedrock/` prefix, exactly like the chat model.
</details>

**Q8.** The brain calls tools in this order: given `cancel` plus a six-character PNR, it calls `lookup_booking`, then `get_disruption_reason(segment)`, then `get_rebooking_options(pnr, tier)`, then answers. For `cancel JX48Q2, options?` the sequence is:

- A) `lookup_booking` then `get_rebooking_options`
- B) `lookup_booking` then `get_disruption_reason`
- C) `get_rebooking_options` then `lookup_booking` then `get_disruption_reason`
- D) `lookup_booking` then `get_disruption_reason` then `get_rebooking_options`

<details><summary>Show answer</summary>

**D)** All three fire in order, because the booking has a segment and a tier to feed the next calls.
</details>

**Q9.** Match each caller to the model string it needs. Bank: `bedrock/us.anthropic...` · `us.anthropic...` · `bedrock/amazon.titan-embed-text-v2:0` · `anthropic...` (one is a decoy).

1. LiteLLM chat call
2. Strands `BedrockModel`
3. LiteLLM embeddings call

<details><summary>Show answer</summary>

1 = **`bedrock/us.anthropic...`**, 2 = **`us.anthropic...`**, 3 = **`bedrock/amazon.titan-embed-text-v2:0`**. The bare `anthropic...` (no `us.`) is the decoy.
</details>

**Q10.** True or False: `bedrock:InvokeModelWithResponseStream` is the IAM action that allows streaming, while `bedrock:ConverseStream` is not an IAM action at all.

- A) True
- B) False

<details><summary>Show answer</summary>

**A) True.** The streaming permission is `InvokeModelWithResponseStream`. `ConverseStream` is an API operation, not something you can grant.
</details>

**Q11.** Match each line to its effect. Bank: **a)** picks the model through its cross-region profile  **b)** gives the model the tools it may call  **c)** pulls the assistant's text out of the response

```python
1  modelId="us.anthropic.claude-haiku-4-5-20251001-v1:0"
2  toolConfig=TOOL_CONFIG
3  text = resp["output"]["message"]["content"][0]["text"]
```

<details><summary>Show answer</summary>

1 = **a**, 2 = **b**, 3 = **c**.
</details>

**Q12.** Order the steps to make one working Bedrock call:
`read the text from the response` · `create the bedrock-runtime client` · `call converse with messages` · `set the model id to the us. profile`

- A) create the client, set the us. profile id, call converse, read the text
- B) set the us. profile id, create the client, call converse, read the text
- C) create the client, call converse, set the us. profile id, read the text
- D) call converse, create the client, set the us. profile id, read the text

<details><summary>Show answer</summary>

**A)** Client first, then the profile id, then the call, then read the output.
</details>

**Q13.** A pipeline has three fixed stages that always run in the same order, with no branching and no model choice. The right build is:

- A) a graph with branches
- B) a chain
- C) an agent loop
- D) a multi-agent supervisor

<details><summary>Show answer</summary>

**B)** Fixed, linear, no judgement is a chain. Reaching higher is cost you do not need.
</details>

**Q14.** True or False: the Strands `BedrockModel` takes the model id with the `bedrock/` prefix, the same as LiteLLM.

- A) True
- B) False

<details><summary>Show answer</summary>

**B) False.** Strands takes the bare `us.anthropic...` profile with no `bedrock/`. Only LiteLLM needs that prefix.
</details>

**Q15.** In the line `text = resp["output"]["message"]["content"][0]["text"]`, what is being read?

- A) the raw JSON payload of every tool result produced during the turn
- B) the stop reason that ended the loop
- C) the first text block of the assistant's message
- D) the token usage for the call

<details><summary>Show answer</summary>

**C)** It reaches into the assistant message and pulls its first content block's text.
</details>
