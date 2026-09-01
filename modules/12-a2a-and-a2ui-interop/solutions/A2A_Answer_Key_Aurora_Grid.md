# Answer Key: Aurora Grid, an A2A Outage Desk

**Language:** Python 3.10+, Bash
**Topics:** A2A protocol, Agent Card, JSON-RPC 2.0, tasks and messages, agent discovery and registries, Strands / LangGraph / LangChain
**Level:** Intermediate

Every number quoted below came out of a live socket. The companion notebook `Aurora_Grid_A2A_Solution.ipynb` executes with zero errors and 27 of 27 self-checks passing against `a2a-sdk 0.3.26`, `strands-agents 1.42.0`, `langchain 1.3.11`, `langgraph 1.2.7`, `litellm 1.95.0`.

---

## Stage 0

### Q0.1 Trace the round trip

| # | Answer |
| --- | --- |
| 1 | **Arrow 1.** `GET /.well-known/agent-card.json` is a plain HTTP GET. Only the POSTs to the card's `url` carry JSON-RPC. Discovery sits outside the RPC layer deliberately, so a client can inspect an agent before committing to its protocol |
| 2 | Turn 1 returned a Task in state `input-required`. The agent asked a question and parked the work. `taskId` is the only thing that tells the server this new message answers that question rather than starting fresh |
| 3 | **200.** That is the trap. The server opens a brand new task, runs it to `completed`, and returns success. The original question is never answered and nothing logs a warning |

Measured, same text sent twice:

```
original task        : 5f974897-2177-474e-961a-048782d056a1
WITHOUT taskId       : d83e503c-9bfc-456e-b86d-413a2f3d7063  state=completed
WITH taskId+contextId: 5f974897-2177-474e-961a-048782d056a1  state=completed
```

### Q0.2 Spot the wrong arrow

**Arrow 1 is wrong.** The registry is not an A2A agent endpoint in this design, so `message/send` does not apply. It should read `GET /agents?tag=dispatch`.

The deeper point: A2A defines no registry method. Nothing in the spec turns "find me an agent" into a protocol call. Any arrow into a registry is your own API, drawn in your own ink.

### Q0.3 Message or Task

| # | Answer | Reason |
| --- | --- | --- |
| a | Message | Single lookup, answer fits in the response, no handle needed afterwards |
| b | Task | Work outlives the HTTP response. The caller needs an id to come back to |
| c | Message | Boolean lookup, no state to carry |
| d | Task | An approval gate guarantees a second turn. `input-required` is the state that expresses it |

**The rule:** open a Task when either side will need to come back. A Message assumes the conversation ends with this response.

---

## Stage 1 blanks

### Blank 1: the decorator

```python
@tool
def lookup_feeder(landmark: str) -> str:
    """Map a street or landmark to the feeder segment that supplies it."""
```

**What.** `@tool` from `strands` registers the function as a callable tool and as the source of an auto-derived A2A skill.

**Why.** The docstring becomes the skill description on the public card. Your docstring is a public interface, not a comment.

**Runtime behaviour with the decorator removed**, measured:

```
tool=<<function plain_function at 0x7f2dff55da80>> | unrecognized tool specification
skills on the card: [('decorated_tool', [])]
```

One line on **stderr**. No exception. `Agent` builds fine, the tool never fires, the card never lists the skill. Under `logging` config that filters stderr, this failure is completely invisible.

### Blank 2: the constructor

```python
locator_agent = Agent(
    name="Fault Locator",
    description="Maps an outage complaint to the feeder segment that supplies it.",
    model=strands_model("Maple Street is on feeder F-114."),
    tools=[lookup_feeder],
)
```

Option (b) uses `llm=` and `functions=`, which are LangChain habits carried across. Option (c) passes a bare model ID string where a model object is required.

### Blank 3: the reducer

```python
class DispatchState(TypedDict):
    request: str
    priority: str
    plan: str
    trace: Annotated[list[str], add]
```

**What.** `Annotated[list[str], add]` attaches `operator.add` as the reducer for this field.

**Why.** Without a reducer, a LangGraph node's return value **replaces** the field. `triage` writes `["triage"]`, `assign` overwrites it with `["assign"]`.

**Runtime behaviour**, both graphs built and run side by side in the notebook:

```
with    Annotated[list, add] -> ['a', 'b']
without Annotated[list, add] -> ['b']
```

Nothing raises either way. This is the highest frequency LangGraph state bug, and it gets worse as the graph grows, because the loss is proportional to how many nodes write the field.

**Rule to carry out of here:** every LangGraph state field written by more than one node needs a reducer.

### Blank 4: the edges

```python
_builder.add_edge(START, "triage")     # (b)
_builder.add_edge("triage", "assign")  # (c)
_builder.add_edge("assign", END)       # (a)
```

**Runtime behaviour with the START edge missing:**

```
ValueError: Graph must have an entrypoint: add at least one edge from START to another node
```

This one raises, at `compile()` time, which makes it the friendliest bug in the exercise. Distractor (e) `add_edge(END, START)` compiles into an unreachable cycle instead.

### Blank 5: the LCEL pipe

```python
    | langchain_model("Aurora Grid: fault found on feeder F-114. "   # (b)
                      "Crew ALPHA-2 en route, power back by 15:05.")
    | StrOutputParser()                                              # (a)
```

Order is not cosmetic. LCEL pipes left to right: a prompt value goes in, a message object comes out of the model, a string comes out of the parser. `JsonOutputParser` on a plain text prompt raises at invoke time, not at build time, so it survives import and dies in the first request.

---

## Stage 2 blanks

### Blank 6: the streaming flag

```python
enable_a2a_compliant_streaming=True,
```

**What.** Switches the Strands A2A adapter from legacy status-update streaming to spec-compliant artifact-update streaming.

**Why it matters.** Measured on the Fault Locator, two servers on separate ports, identical request:

| Setting | `len(task.history)` | Artifact parts |
| --- | --- | --- |
| `False` (the default) | **12** | 1 |
| `True` | **1** | 12 |

With `False`, every stream fragment becomes its own agent message in `task.history`. The reply `"Maple Street is on feeder F-114."` produced twelve history entries for a single turn.

`a2a-sdk` itself emits the warning: the default Strands response stream does not conform to what the A2A spec expects, and the next major version flips the default.

**Why this is worse than cosmetic.** `task.history` is the conversation record. Any downstream agent that replays it sees twelve turns that never happened. Multi-agent handoff, audit, and few-shot replay all read from here.

**Production note.** Assert on `len(task.history)` in CI, not just on the final text. Only the length catches this.

### Blank 7: the tags

```python
tags=["outage", "locate"],
```

**Runtime behaviour**, auto-derived versus declared, both built in the notebook:

```
BROKEN (auto-derived)    skills=[('lookup_feeder', [])]
                         tag=locate matches -> NOTHING
FIXED (declared)         skills=[('locate_fault', ['outage', 'locate'])]
                         tag=locate matches -> ['locate_fault']
```

Strands can derive a skill `id` from the function name and a `description` from the docstring. It cannot invent tags, so auto-derived skills always carry `tags=[]`.

The agent is healthy, published, reachable, and invisible to every capability query. Option (c) `tags="outage,locate"` fails Pydantic validation at startup, which is the one merciful distractor here.

### Blank 8: the submit guard

```python
if not context.current_task:
    await updater.submit()
```

**What.** `context.current_task` is `None` on first contact and populated on every follow-up turn.

**Why.** Calling `submit()` unconditionally re-registers a task the store already tracks. Option (c) inverts the test, so the first turn never submits at all and the task is never created.

### Blank 9: the question that is not a failure

```python
await updater.requires_input(
    updater.new_agent_message(
        [{"kind": "text",
          "text": "Which feeder segment? Reply with the feeder ID, e.g. F-114."}]))
```

| Choice | State the caller sees | What the caller does next |
| --- | --- | --- |
| `requires_input` | `input-required` | Answers, on the same task |
| `failed` | `failed` (terminal) | Retries from scratch, question lost |
| `reject` | `rejected` (terminal) | Gives up, question lost |
| `raise` | `-32603 Internal error` | Pages someone |

A missing fact is a question, not a failure. Getting this wrong turns every clarification into a full restart, and on a paid model that is a real bill.

### Blank 10: artifact then complete

```python
await updater.add_artifact(
    [{"kind": "text", "text": result["plan"]}], name="dispatch_plan")   # (b)
await updater.complete()                                               # (a)
```

Order matters. `complete()` closes the task, so an artifact added afterwards lands on a queue nobody reads. Completing with no artifact at all returns a successful task with an empty `artifacts` list, which the coordinator prints as `''` with no error to explain it.

### Blank 11: the url

```python
url=f"{BASE[role]}/",
```

Option (b) `url="/"` fails validation. Option (c) hardcodes `localhost`, which behaves identically to `127.0.0.1` and is wrong for the same reason. See Bug 4.

---

## Stage 3 blanks

### Blank 12: the card fetch

```python
card = await A2ACardResolver(httpx_client=hx, base_url=base).get_agent_card()
```

`A2ACardResolver` defaults to `agent_card_path="/.well-known/agent-card.json"` and issues a GET. Option (b) invents a JSON-RPC method that does not exist. There is no `agent/getCard`.

Verified constants from the SDK:

```
card path      : /.well-known/agent-card.json
retired path   : /.well-known/agent.json
extended card  : /agent/authenticatedExtendedCard  (method: agent/getAuthenticatedExtendedCard)
default rpc url: /
```

### Blank 13: the tag filter

```python
if tag in skill.get("tags", [])
```

Option (b) matches the tag against the agent's **name**, which reviews fine and matches nothing.

Option (d) matches against `skill["id"]`, which is the nastier one: `tag="locate"` accidentally matches `id="locate_fault"`, so the first test passes and every other tag fails. Partially working filters are worse than broken ones, because they buy you a false sense of coverage.

### Blank 14: the three routes

```python
Route("/.well-known/agent-card.json", registry_card),   # (b)
Route("/refresh", refresh),                             # (c)
Route("/agents", agents),                               # (a)
```

Option (d) `Route("/message/send", ...)` is the conceptual trap: A2A methods are JSON-RPC method names inside a POST body, never HTTP paths. There is exactly one POST endpoint, at the card's `url`.

**Why the registry publishes its own card.** A client that knows one URL can KNOCK on the registry, read `skills[0].description`, and learn how to ASK. Without it you are back to hardcoding two URLs instead of one.

**Live output:**

```
registered : ['Crew Dispatcher', 'Customer Notifier', 'Fault Locator']
unreachable: []

  tag=locate     -> ['Fault Locator']
  tag=dispatch   -> ['Crew Dispatcher']
  tag=comms      -> ['Customer Notifier']
  tag=billing    -> NOTHING REGISTERED
```

---

## Stage 4 blanks

### Blank 15: ASK, not KNOCK

```python
resp = await hx.get(f"{BASE['registry']}/agents", params={"tag": tag})
```

Option (b) KNOCKs on the registry's own card, which describes the registry rather than listing agents.

### Blank 16: the separator

```python
separator = ""
return separator.join(chunks)
```

**Runtime behaviour**, twelve parts on the wire from one streamed reply:

```
BROKEN  " ".join -> 'Map le  Str eet  is  on  fe ede r F -11 4. '
FIXED    "".join -> 'Maple Street is on feeder F-114.'
```

Parts within an artifact are **appended**, never separated. A streaming agent emits one part per chunk and the boundaries are arbitrary tokenizer artefacts. A separator is a decision the sender never authorised.

This bug is invisible on a non-streaming agent, which is exactly how it ships.

### Blank 17: the two attributes

```python
msg.task_id = task.id          # (a)
msg.context_id = task.context_id  # (b)
```

**Measured nuance.** `task_id` alone is sufficient. The server backfills `contextId` from the stored task:

```
same task id     : True
contextId kept   : True
state            : completed
```

**Send both anyway.** `contextId` groups related tasks into one conversation, and the moment you fan out to a second agent, the server on that side has no stored task to backfill from.

Distractor (c) `msg.message_id = task.id` is the shape of Q12: it assigns a real value to the wrong field, so nothing validates and nothing resumes.

### Blank 18: the transport

```python
supported_transports=[TransportProtocol.jsonrpc],
```

The card already declared `preferredTransport: JSONRPC`. Requesting `grpc` against a server that only speaks JSON-RPC fails at client creation. Option (c) passes a raw string where the enum is required, and the enum value is `"JSONRPC"`, not `"JSON-RPC"`.

Verified: `TransportProtocol` values are `['JSONRPC', 'GRPC', 'HTTP+JSON']`.

### The full run

```
[ASK] tag=locate     -> Fault Locator @ http://127.0.0.1:9101/
  locator says: 'Maple Street is on feeder F-114.'

[ASK] tag=dispatch   -> Crew Dispatcher @ http://127.0.0.1:9102/
  state=input-required  task=6969aadb-caa4-4c21-b5da-f841daff89bf
  agent asks: 'Which feeder segment? Reply with the feeder ID, e.g. F-114.'
  state=completed  SAME task
  plan: 'Crew ALPHA-2, P1, ETA 45 min'

[ASK] tag=comms      -> Customer Notifier @ http://127.0.0.1:9103/
  sms: 'Aurora Grid: fault found on feeder F-114. Crew ALPHA-2 en route, power back by 15:05.'
```

---

## Stage 5 trace answers

### 1. Why only one of steps 4 and 5 completes the original ticket

Step 4 omits `taskId`, so the server has no reference and opens a new task. Step 5 carries `taskId` and `contextId`, so `context.current_task` is populated, the `submit()` guard skips, and the executor resumes. Both return HTTP 200 with `state: completed`.

### 2. The three history entries

```
state          : completed
history length : 3
  1. user   Send a crew, it is dark near the clinic
  2. agent  Which feeder segment? Reply with the feeder ID, e.g. F-114.
  3. user   Feeder F-114, clinic block
artifacts      : [('dispatch_plan', ['Crew ALPHA-2, P1, ETA 45 min'])]
```

The final answer is **not** in `history`. It is in `artifacts`. `history` is the conversation; `artifacts` are the deliverables. A client that reads only `history` on a completed task gets the question and never the answer.

### 3. Which states you can cancel from

Cancellation is legal only from non-terminal states: `submitted`, `working`, `input-required`, `auth-required`. The four terminal states refuse it.

```
cancel a terminal task        -32002  Task cannot be canceled - current state: TaskState.completed
```

The SDK appends the offending state to the message, which is the one error in the set that tells you why on its own.

---

## Stage 6 bug fixes

### Bug 1: orphaned task

```python
reply = create_text_message_object(Role.user, "Feeder F-114")
reply.task_id = t1.id                # FIX
reply.context_id = t1.context_id     # FIX
```

### Bug 2: shredded artifact

```python
text = "".join(...)   # one character: the space comes out
```

### Bug 3: untagged skill

The missing keyword argument is `skills=`.

```python
server = A2AServer(
    agent=locator_agent, host="127.0.0.1", port=9199, version="1.0.0",
    skills=[AgentSkill(id="locate_fault", name="Locate fault",
                       description="Map an outage complaint to a feeder segment.",
                       tags=["outage", "locate"])],
)
```

### Bug 4: unreachable url

No code change. The written answer:

| | |
| --- | --- |
| **Who breaks** | Every caller not on this host. A sibling container, a pod on another node, a partner in another data centre. The local coordinator keeps working, which is why this reaches production |
| **What it should come from** | The externally advertised base URL, injected as configuration, not composed from the bind address |
| **The mechanism** | Strands exposes `http_url=` for exactly this, plus `serve_at_root=True` for load balancers that strip path prefixes |
| **The rule** | The bind address is where the socket listens. `card.url` is where the world dials. Different facts, different variables |

Measured:

```
host            default='127.0.0.1'
port            default=9000
http_url        default=None
serve_at_root   default=False

bind-derived url : http://127.0.0.1:9197/
config-driven url: https://agents.aurora-grid.example/locator/
```

Note `port` defaults to **9000**, which is Bug 5.

---

## Checkpoint answers

| Q | Answer | Reasoning |
| --- | --- | --- |
| **Q1** | **b** | Plain HTTP GET on `/.well-known/agent-card.json` (RFC 8615). The retired `/.well-known/agent.json` still returns 200 with a server side deprecation log. There is no `agent/getCard` method |
| **Q2** | **a, c, e, g** | Required: `name`, `description`, `url`, `version`, `capabilities`, `defaultInputModes`, `defaultOutputModes`, `skills`. `provider`, `securitySchemes`, `iconUrl` are optional |
| **Q3** | **b** `['b']` | No reducer, so each node replaces the field. Same defect as Blank 3, proved live in the notebook |
| **Q4** | a=F, b=F, c=T, d=T, e=F | See breakdown below |
| **Q5** | 1-B, 2-A, 3-D, 4-C | E and F are distractors. Neither defect produces a schema error |
| **Q6** | **c, a, d, b** | `submit()`, `start_work()`, `get_user_input()`, `requires_input()` |
| **Q7** | `submit()` | On turn 2, `context.current_task` is populated. The task already exists in the store, so re-submitting registers work that is already tracked. The guard `if not context.current_task` is the whole fix |
| **Q8** | **7** | 3 registry GETs plus 4 `message/send` POSTs. Add 1 for the `/refresh` call in the real script, which itself fires 3 KNOCKs, for 11 total on a cold start |
| **Q9** | **b** | `input-required --> working` on the reply. The other three all originate from terminal states |
| **Q10** | P3, DELTA-7, ETA 180 min | `PRIORITY_KEYWORDS` is `clinic, hospital, water, school`. "Mill Road" hits none, so triage returns P3 |
| **Q11** | Two defects, see below | |
| **Q12** | `reply.message_id = task.id` | Fix: `reply.task_id = task.id`. Add `reply.context_id = task.context_id` as well. `messageId` identifies this single message and has no bearing on task continuity |
| **Q13** | `if tag in card["description"]` | Fix: `if tag in skill.get("tags", [])`. Matching a routing tag against free text is a coincidence generator |
| **Q14** | See below | |
| **Q15** | See below | |
| **Q16** | See below | |

### Q4 breakdown

| # | Statement | Answer | Why |
| --- | --- | --- | --- |
| a | `input-required` is terminal | **False** | It is a wait. The task resumes to `working` when the caller replies with the `taskId` |
| b | A2A standardises a registry query API | **False** | The spec names registries as a discovery strategy and explicitly declines to define an API for them |
| c | One `contextId` can span several `taskId` values | **True** | `contextId` is the conversation, `taskId` is one unit of work inside it |
| d | An agent may reply with a bare `Message` | **True** | For trivial work with nothing to track, a Message is the correct response |
| e | `-32601` means the method was understood and declined | **False** | `-32601` is Method not found, an envelope error. Understanding a method and declining it is `-32004 UnsupportedOperationError` |

### Q11: code review, two defects

| # | Defect | Fix |
| --- | --- | --- |
| 1 | `await updater.submit()` is unguarded | Wrap in `if not context.current_task:` |
| 2 | A missing feeder ID is reported as `failed` | Use `requires_input(...)`. `failed` is terminal, so the caller cannot answer the question |
| 3 (bonus) | `complete()` with no `add_artifact` | The task succeeds carrying nothing. The coordinator prints an empty string and no error explains why |

Any learner who finds all three has understood the stage.

### Q14: the acquired utility

| # | Answer |
| --- | --- |
| a | **Nothing in the coordinator's code.** The seed list in the registry gains one entry, which is a config change. Had the coordinator DIALed the dispatcher directly, this would be a code change, which is the argument for the registry in one sentence |
| b | `url`. It must be the externally reachable address, and behind a path-stripping load balancer it must reflect what callers actually dial, not what the container binds. On the Strands side that is `http_url=` plus `serve_at_root=True` |
| c | **No.** A2A is a wire contract, not a runtime contract. You POST JSON-RPC to a URL you read off a card. The language, framework, model, and deploy schedule on the other side are invisible and irrelevant |

### Q15: the melting notifier

| # | Answer |
| --- | --- |
| a | The push notification group: `tasks/pushNotificationConfig/set`, `/get`, `/list`, `/delete`. The agent calls your webhook on state change instead of you asking 40 times a minute |
| b | `capabilities.pushNotifications` must be `true` on the card |
| c | `-32003 Push Notification is not supported` |

Second order point worth raising in discussion: a webhook makes your coordinator an HTTP **server** as well as a client, which pulls authentication, replay protection, and idempotency into scope. Polling is inefficient and simple. Push is efficient and a system.

### Q16: the smallest matching card

```python
AgentCard(
    name="Restoration Verifier",
    description="Confirms supply is restored on a feeder segment.",
    url="http://127.0.0.1:9104/",
    version="1.0.0",
    capabilities=AgentCapabilities(streaming=False),
    default_input_modes=["text"],
    default_output_modes=["text"],
    skills=[AgentSkill(id="verify_restore", name="Verify restoration",
                       description="Confirm supply is back on a feeder segment.",
                       tags=["outage", "restore"])],
)
```

Validated against `a2a-sdk 0.3.26`. Nine lines of arguments, all eight required fields present, `tags` carrying the value the registry filters on.

Drop `tags` and the card is still valid and still unreachable by query, which is Blank 7 stated one last time.

---

## Reference tables

### JSON-RPC error codes, live triggers

| Code | Band | Name | Reproduced by |
| --- | --- | --- | --- |
| -32700 | envelope | `JSONParseError` | Truncated body. The SDK substitutes the real parse position: `Expecting value: line 1 column 36 (char 35)` |
| -32600 | envelope | `InvalidRequestError` | Missing `jsonrpc` key |
| -32601 | envelope | `MethodNotFoundError` | `"method": "message/sned"` |
| -32602 | envelope | `InvalidParamsError` | `message` with no `parts` |
| -32603 | envelope | `InternalError` | Unhandled exception in the executor |
| -32001 | the ask | `TaskNotFoundError` | `tasks/get` on an id never issued |
| -32002 | the ask | `TaskNotCancelableError` | `tasks/cancel` on a terminal task |
| -32003 | the ask | `PushNotificationNotSupportedError` | Card says `pushNotifications: false` |
| -32004 | the ask | `UnsupportedOperationError` | A method the agent declines |
| -32005 | the ask | `ContentTypeNotSupportedError` | A file sent to a text only agent |
| -32006 | the ask | `InvalidAgentResponseError` | A downstream agent broke the contract |
| -32007 | the ask | `AuthenticatedExtendedCardNotConfiguredError` | `supportsAuthenticatedExtendedCard` absent |

### Task states

| State | Kind |
| --- | --- |
| `submitted` | active |
| `working` | active |
| `input-required` | waiting |
| `auth-required` | waiting |
| `completed` | terminal |
| `canceled` | terminal |
| `failed` | terminal |
| `rejected` | terminal |
| `unknown` | active |

---

## Grading

| Band | Signal |
| --- | --- |
| **Full** | All 18 blanks, all 4 bugs, Q11 finds both defects, Q14c answered without hedging |
| **Solid** | Blanks and bugs done, scenario questions partially reasoned |
| **Gap: protocol vs framework** | Learner edits agent logic to fix a protocol problem, or reaches for a framework feature where a card field was the answer |
| **Gap: task lifecycle** | Learner treats `input-required` as an error, or cannot say why turn 2 needs `taskId` |
| **Gap: discovery** | Learner expects A2A to define the registry, or cannot name what the registry is for beyond "a list of URLs" |
| **Gap: silent failure literacy** | Learner looks for a stack trace on Bugs 1, 2, and 3. There is none. This is the habit the stage exists to break |

---

## Reusable teaching lines

- The framework is the chef, A2A is the menu and order slip, JSON-RPC is the waiter
- MCP is what is in your hands, A2A is who is in the room
- A card is a passport, not a manual
- A message is a shout, a task is a ticket
- KNOCK a domain, ASK a registry, DIAL a config
- Four ways out, two ways to wait
- Minus 326xx is the envelope, minus 320xx is the ask
- History is the conversation, artifacts are the deliverables
- The bind address is where the socket listens, `card.url` is where the world dials
- Your registry is your governance surface, because there is nowhere else for it to live
