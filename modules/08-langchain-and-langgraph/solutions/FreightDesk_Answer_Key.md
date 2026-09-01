# FreightDesk: Answer Key and Facilitator Notes

Companion to `FreightDesk_Lab.md`. Do not distribute with the lab file.

Every answer below is stated as: **the pick**, why it is right, what each wrong option costs. Where a claim was measured rather than read, the measured output is included.

---

## 1. Answer index

| TODO | Answer | The one line to say out loud |
|---|---|---|
| 1 | A | Pipes read left to right as data flow |
| 2 | B | A missing AWB is business data, not a fault |
| 3 | B | A timeout must stay an exception or retry cannot see it |
| 4 | A | Retries re-run calls, so writes need idempotency |
| 5 | B | Retry only what time fixes |
| 6 | B | Matching `tool_call_id`, exception type not message |
| 7 | B | Return without calling `handler` and the tool never runs |
| 8 | B | `checkpointer=` |
| 9 | A | `thread_id` is the memory key |
| 10 | B | Gate side effects, allow reads |
| 11 | B | `"__interrupt__" in result` |
| 12 | A | `{"decisions": [{"type": "approve"}]}` |
| 13 | B | `apply_to_tool_results=True` |
| 14 | B | Phone is not a built-in type |
| 15 | B | `trigger` and `keep`, as tuples |
| 16 | C | When a control fails, the capability it controls fails with it |

| Checkpoint | Answer |
|---|---|
| R1 | Q, S, R, P, T, and the list order is wrong |
| R2 | B |
| R3 | `M --> T`, fix is "before" |
| R4 | P2, `apply_to_tool_results=True` |
| R5 | 1B, 2C, 3D, 4E, 5A, 6F. Distractors G and H |

---

## 2. Segment 0

### TODO-1: **A**, `TRIAGE_PROMPT | llm | JsonOutputParser()`

Pipes read left to right as data flow. Text into a prompt template, formatted prompt into a model, model output into a parser.

| Wrong | Cost |
|---|---|
| B | Feeds a prompt template into a model. Backwards |
| C, D | Parser placed before there is anything to parse |

**The point of the segment, not the question.** This chain has no tools and cannot loop. That is why it belongs in front of the agent. If a learner asks why not just let the agent classify, the answer is cost, latency and testability: you can unit test this chain against 200 historical emails tonight.

---

## 3. Segment 1

### TODO-2: **B**, return `NOT_FOUND: ...`

A missing AWB is a business outcome. Returned as text it becomes a `ToolMessage` the model reads and acts on, so it asks for a corrected number and the case continues.

| Wrong | Cost |
|---|---|
| A, D | End the turn. Measured: a tool raising `KeyError` inside `create_agent` propagates out of `invoke` and the run stops |
| C | `None` becomes an empty tool result and the model fills the gap by inventing |

Measured, `middleware=[]`:

```text
CLAIM: run HALTED with KeyError -> 'internal_field_missing'
```

### TODO-3: **B**, `raise CarrierTimeout(...)`

A timeout is an absence of information, and the same call usually works two seconds later. Raising a typed exception is what makes it visible to the retry layer.

| Wrong | Cost |
|---|---|
| A | The tempting one. Looks defensive, silently disables retry: the middleware sees a successful call returning a string. The model then has to reason about infrastructure it cannot fix |
| C | Fabricates a status for cold chain cargo |
| D | Makes the call slow and changes nothing |

### TODO-4: **A**, return `ALREADY_REBOOKED: ...`

Segment 2 adds retries, and retries re-run calls. A human on a slow connection can also approve twice. Both become duplicate bookings without this check.

| Wrong | Cost |
|---|---|
| B | Turns a benign repeat into a crash |
| C | Silently overwrites, so the second call reports success for a change that did not happen |
| D | Deletes your only record of the write |

**Facilitator note.** This is the first TODO where the right answer depends on a segment they have not read yet. The hint in the lab is deliberate. If nobody catches it, do not give it away, let Segment 2 create the double booking and come back.

---

## 4. Segment 2

### TODO-5: **B**, `(CarrierTimeout, CarrierUnavailable)`

Retry what time fixes.

| Wrong | Cost |
|---|---|
| A | Retries your own `KeyError` three times with backoff, then fails anyway |
| C | Retries error classes this tool never raises. Does nothing |
| D | `None` means the default, which is all exceptions. A with extra steps |

Exceptions outside `retry_on` propagate immediately and never reach `on_failure`. That is intended: `on_failure` is about exhausted retries, not unhandled types.

Verified signature:

```text
ToolRetryMiddleware(*, max_retries=2, tools=None, retry_on=(Exception,),
                    on_failure='continue', backoff_factor=2.0, initial_delay=1.0,
                    max_delay=60.0, jitter=True)
```

Note the default `retry_on` is every exception. Leaving it unset is option A by omission, which is how this lands in real code.

---

## 5. Segment 3

### TODO-6: **B**, `ToolMessage` with matching `tool_call_id` and `status="error"`

Three things right at once:

| Element | Why |
|---|---|
| `tool_call_id=request.tool_call["id"]` | Must match the call the model made, or history carries an unanswered tool call and the next model call fails on a different error than the one you were fixing |
| `status="error"` | Marks a failure rather than a result |
| `type(exc).__name__`, not `str(exc)` | Raw exception text carries hostnames, connection strings and paths you do not want in a prompt or a trace |

| Wrong | Cost |
|---|---|
| A | Returns a bare string where a message object belongs |
| C | Hardcoded id matches nothing |
| D | Re-raises, which is the thing being prevented |

Measured with the safety net in place:

```text
TOOL_FAILED: boom raised KeyError. | status = error
```

### TODO-7: **B**, return a `ToolMessage` without calling `handler`

That is the short-circuit. Return from a wrap layer and the tool never runs.

| Wrong | Cost |
|---|---|
| A | Calls the tool anyway, which is what you were blocking |
| C | `None` where a message is required |
| D | Raises, which your own safety net then catches and describes badly |

**The transferable line:** a prompt asks the model not to do something, a guard makes it impossible. Guards are cheaper and do not degrade with context length.

---

## 6. Segment 4

### TODO-8: **B**, `checkpointer=checkpointer`

Recall. Worth knowing for the failure it produces: leave it out and the HITL middleware has nowhere to write paused state, so approvals stop working and the error points somewhere else.

Verified: `create_agent(model, tools, system_prompt, middleware, response_format, state_schema, context_schema, checkpointer, store, interrupt_before, interrupt_after, debug, name, cache, transformers)`.

### TODO-9: **A**, `"thread_id": CASE_AWB`

`thread_id` is the memory key. Using the AWB makes the technical memory boundary the same as the business boundary.

Every other key name is **silently ignored**. You get a working agent with no memory and no error message, which is the worst combination available.

**Facilitator note.** Test input 6 in the lab exists for this. Learners who picked B, C or D will pass every test except 5, and will not know why until they run 5 and 6 back to back.

---

## 7. Segment 5

### TODO-10: **B**

Gate side effects, allow reads.

| Wrong | Cost |
|---|---|
| A | Gates everything. A desk agent approving `find_shipment` forty times a morning stops reading arguments. By the time a real rebooking appears the approval is muscle memory. Worse than no gate, because it produces an approval record nobody read |
| C | Leaves `notify_customer` open. Agent messages a customer unreviewed |
| D | Configures only auto-approvals and gates nothing |

**The decision rule behind the split**, and the part worth teaching: allow `edit` where the argument space is small and enumerable, like a flight number picked from a list the agent just retrieved. Withhold `edit` where the argument is free text, like a customer message, because free-text editing inside an approval popup routes around every content control upstream. Reject and redraft instead.

### TODO-11: **B**, `"__interrupt__" in result`

Measured return from a paused `invoke`:

```text
keys = ['messages', '__interrupt__']
interrupt value keys = ['action_requests', 'review_configs']
action_requests = [{'name': 'rebook', 'args': {...}, 'description': 'Tool execution requires approval\n\nTool: rebook\nArgs: {...}'}]
review_configs  = [{'action_name': 'rebook', 'allowed_decisions': ['approve', 'reject']}]
```

Two things to flag from that dump. The action request key is **`args`**, not `arguments`, which some docs examples show. And `description` is prebuilt from your `description_prefix` plus the tool name and args, so you do not have to assemble it.

| Wrong | Cost |
|---|---|
| A, D | Attributes the default invoke result does not carry |
| C | True whether the run paused or not |

Newer builds also accept `version="v2"` on invoke and return an object with an `.interrupts` attribute. Both work. `print(result.keys())` once and use what your build gives you.

### TODO-12: **A**, `{"decisions": [{"type": "approve"}]}`

A list of decisions, one per pending action, in the same order as the actions in the interrupt. Types: `approve`, `edit`, `reject`, `respond`.

| Wrong | Cost |
|---|---|
| B | The older shape from early builds. The single most common copy-paste failure on this topic |
| C, D | Invented |

Measured after approve: `['REBOOKED 160-45872910 -> MA-219']`.

**Say this once, it prevents a real incident:** `respond` returns the human's text as a **successful** tool result. Denying a rebooking with `respond` tells the model the rebooking worked.

---

## 8. Segment 6

### TODO-13: **B**, `apply_to_tool_results=True`

The default checks user input only. In this design the shipper email never appears in user input. It comes out of `find_shipment`.

Same middleware, same tool, one argument different:

```text
apply_to_tool_results=False -> shipper contact ops@kavery-exports.example / +91 98450 11223
apply_to_tool_results=True  -> shipper contact [REDACTED_EMAIL] / +91 98450 11223
```

Input-only redaction here protects nothing and produces a clean compliance answer that is false. The phone survives in both lines because that layer is TODO-14.

### TODO-14: **B**, a custom type with an explicit `detector`

Built-in types: `email`, `credit_card`, `ip`, `mac_address`, `url`. Phone is not among them.

A and C raise at construction:

```text
ValueError: Unknown PII type: phone. Must be one of
['email', 'credit_card', 'ip', 'mac_address', 'url'] or provide a custom detector.
```

Loud failure, which is the good case. The library can only protect you from a type it has never heard of. It cannot check your regex, and that is where the damage happens.

**Run this bit live if you run nothing else.** An earlier draft of this lab used `\+?\d[\d\s().-]{7,}\d`, which looks perfectly reasonable. Measured end to end, the agent produced:

```text
AWB ****2910: BLR to AMS, 12 pcs / 480 kg, booked MA-217 dep ****8-06
```

The detector ate the air waybill and the departure date. Every downstream call now carries masked identifiers, so the agent is reasoning about a shipment it can no longer name. Requiring a leading `+` fixes it for this data and costs you local-format numbers like `9845011223`.

Detector scores on the six probe strings:

| String | `\+?\d[\d\s().-]{7,}\d` | `\+\d{1,3}[\s.-]?\d{4,5}[\s.-]?\d{4,6}` |
|---|---|---|
| `+91 98450 11223` | match | match |
| `160-45872910` | **match, false positive** | no match |
| `2026-08-06` | **match, false positive** | no match |
| `MA-217` | no match | no match |
| `480 kg` | no match | no match |
| `9845011223` | match | **no match, false negative** |

Neither column is clean. That tradeoff is the design decision, and there is no setting that removes it. Bonus 6 is where they meet it properly.

---

## 9. Segment 7

### TODO-15: **B**, `trigger=("messages", 12)`

Current parameters are `trigger` and `keep`, both `(unit, value)` tuples where the unit is `fraction`, `tokens` or `messages`.

| Wrong | Cost |
|---|---|
| A | The deprecated name. Absorbed by `**deprecated_kwargs`, so it may still run, which is exactly why old tutorials keep it alive |
| C, D | Not valid |

Verified signature and defaults:

```text
SummarizationMiddleware(model, *, trigger=None, keep=('messages', 20),
                        token_counter=count_tokens_approximately,
                        summary_prompt=<long default>, trim_tokens_to_summarize=4000,
                        **deprecated_kwargs)
```

**The default `trigger` is `None`, and `None` means summarization never fires.** A `SummarizationMiddleware` instantiated with no trigger is a no-op that looks like a control. That is the fact to make them say back to you.

---

## 10. Segment 8

### TODO-16: **C**, `degraded_agent.invoke(payload)`

The approval gate pauses by writing state to the checkpointer. Persistence down means it cannot pause, which means it cannot gate. Any fallback that keeps write tools reachable has removed your only control while looking like resilience.

| Wrong | Cost |
|---|---|
| A | Retries the same failing path |
| **B** | **The trap.** Same tools, same prompt, users barely notice. And `rebook_shipment` now executes unreviewed on every call. This is a real production pattern, usually written during an incident by someone trying to restore service |
| D | Throws away the turn and tells the user nothing useful |

**The line to land the whole lab on:** when a control fails, the capability it controls fails with it. Anything else is a control you do not have.

**Facilitator note.** Give this segment room. For a room of solution and test architects it lands harder than any middleware syntax, and B is the answer most of them will defend before they see it. Ask whoever picked B to describe the incident review three weeks later.

---

## 11. Reasoning checkpoints

### R1: **Q, S, R, P, T**, and the list is wrong

Summarization and PII input checking both act in the before-model phase, so they run in list order: compaction (Q), then email redaction (S). The model call produces the tool call (R). The gate runs in the after-model phase and reads the proposed call (P). Only after a decision does the tool execute (T), inside the wrap layers.

**The second question is the real one.** With `[compaction, pii_email, ...]`, the summarizer model reads unredacted history. Swap them. The lab's own list is a privacy bug, and they were asked to trace it before they were told.

Ordering rules, confirmed:

| Hook type | Order |
|---|---|
| `before_*` | First to last down the list |
| `after_*` | Last to first |
| `wrap_*` | Nested, first entry outermost |

### R2: **B**

Retry catches the first two `CarrierTimeout` exceptions itself and re-invokes the handler. Only the third attempt produces a result, so the model sees exactly one successful `ToolMessage` and never learns the carrier API was slow.

| Wrong | What it actually describes |
|---|---|
| A | What `on_failure="continue"` does after retries are **exhausted**, which is not this case |
| C | What `on_failure="error"` does after exhaustion |
| D | What happens if the safety net sits inside the retry layer: exceptions get converted before retry sees them, so nothing retries |

D is worth sitting with. It is a real bug produced purely by middleware order, and it is silent.

### R3: the arrow `M --> T`

Execution happens before approval, so the gate is asked to approve something already done. One-word fix: **before**. The chain must be `M --> H --> T`.

A gate placed after the side effect is not a control, it is a notification.

### R4: **P2**, and the argument is `apply_to_tool_results=True`

P1 guards the door the data does not come through. `apply_to_output` matters too, for what the model writes back into logs, but the argument doing the specific work here is `apply_to_tool_results`.

### R5

| Symptom | Missing control |
|---|---|
| 1 Double rebooking | **B** idempotency check in the write tool |
| 2 Context length error at turn 38 | **C** summarization with a real `trigger` |
| 3 Booking changed with no approval record | **D** fail-closed degradation |
| 4 Traceback shown to a desk agent | **E** `wrap_tool_call` safety net |
| 5 Phone number in a trace | **A** PII with `apply_to_tool_results=True` |
| 6 Run stops on a missing AWB | **F** expected outcomes returned as data |

Distractors: **G** and **H**. A tool call limit caps loops and prevents none of these. Structured output on the triage chain is upstream of all six.

**Symptom 3 is the one people get wrong**, and the miss is instructive. They answer "no HITL gate". The gate existed. The degraded path went around it. That is the whole of Segment 8 restated as a support ticket.

---

## 12. The chain, filled in

| Segment | Failure it prevents | Failure it creates |
|---|---|---|
| 0 LCEL router | Paying agent prices for trivial questions | Real cases still reach an agent with no tools |
| 1 Error split | A typo ending a case with a traceback | Transient carrier failures now surface as raised exceptions with nothing catching them |
| 2 Retry | A two second outage losing the case | Only predicted failure types are covered |
| 3 Safety net | An unpredicted bug ending the turn | Nothing crashes, so the agent completes the case including the write |
| 4 Checkpointer | Losing the case between turns | It now remembers, and still writes unreviewed |
| 5 Approval gate | Freight moved on model judgment | Approval screens and traces now carry shipper identifiers |
| 6 PII | Identifiers leaking at three doors | Long threads still grow without limit |
| 7 Compaction | Context length failure mid-case | A working system with a single point of failure nobody has tested |
| 8 Fail closed | A controls outage disguised as a memory outage | Nothing |

If a learner can produce the right column unaided, they understand the system. The left column alone means they learned the tools.

---

## 13. Verified API facts

Measured against langchain 1.3.14 and langgraph 1.2.10 by running the code, not by reading docs. Re-check on your cohort's build.

| Fact | Detail |
|---|---|
| Tool exceptions in `create_agent` | Not caught by default. A tool raising `KeyError` propagates out of `invoke` and ends the run. The default handler returns the message for `ToolInvocationError` and re-raises everything else. Error handling is a middleware concern |
| Interrupt surfacing | Default `invoke` returns keys `['messages', '__interrupt__']`. The value has `action_requests` and `review_configs`. Action requests carry `name`, `args`, `description`. **`args`, not `arguments`** |
| Review configs | Carry `action_name` and `allowed_decisions` |
| HITL resume | `Command(resume={"decisions": [{"type": "approve"}]})`. Types `approve`, `edit`, `reject`, `respond`. Older builds used a bare list with `accept` |
| `HumanInTheLoopMiddleware` signature | `(interrupt_on, *, description_prefix='Tool execution requires approval')` |
| `SummarizationMiddleware` | `trigger` and `keep` as tuples. Defaults `trigger=None`, `keep=('messages', 20)`. `max_tokens_before_summary` and `messages_to_keep` are absorbed by `**deprecated_kwargs` |
| `PIIMiddleware` signature | `(pii_type, *, strategy='redact', detector=None, apply_to_input=True, apply_to_output=False, apply_to_tool_results=False)` |
| `PIIMiddleware` built-in types | `email`, `credit_card`, `ip`, `mac_address`, `url`. Anything else raises `ValueError` at construction unless you pass `detector=` |
| `ToolRetryMiddleware` defaults | `max_retries=2`, `retry_on=(Exception,)`, `on_failure='continue'`, `backoff_factor=2.0`, `initial_delay=1.0`, `max_delay=60.0`, `jitter=True` |
| `ToolCallLimitMiddleware` signature | `(*, tool_name=None, thread_limit=None, run_limit=None, exit_behavior='continue')` |
| `ToolErrorMiddleware` | Recent builds only. If preflight says MISSING, the Segment 3 safety net does the same job |
| Conditional interrupts (`when`) | Recent builds only. Check before assigning Bonus 1 |
| Wrap-hook nesting | Measured: `middleware=[outer, inner]` traces as `A-enter, B-enter, B-exit, A-exit`. First in the list is outermost. Two docs pages disagree on this, which is why Bonus 7 exists |
| `yield` in `wrap_tool_call` | Makes the function a generator and raises `NotImplementedError`. Use `return` |
| `ToolCallRequest` fields | `tool_call`, `tool`, `state`, `runtime` |
| Bedrock model id | The `us.` cross-region inference profile prefix is required. A bare model id raises `ValidationException` |
| Bedrock sampling | Claude 4.x treats `temperature` and `top_p` as mutually exclusive. Set one |
| Model init alternatives | `ChatBedrockConverse(model=..., region_name=...)` or `init_chat_model(MODEL_ID, model_provider="bedrock_converse")` |

---

## 14. What changes in production

| In this lab | In production |
|---|---|
| `InMemorySaver` | Postgres or MongoDB checkpointer, plus a tested degraded path |
| Dict `SHIPMENTS` | Real booking system behind a client with timeouts and a circuit breaker |
| Hardcoded region and model id | Configuration, not literals |
| Approval printed to stdout | A queue with an identity attached to every decision, retained for audit |
| Retry counter in a module dict | Server-side idempotency keys on every write |
| No evals | A fixed case set that runs on every prompt or model change, including the cold chain case |

---

## 15. Running the lab

| Timing | Notes |
|---|---|
| Segments 0 to 3 | The mechanical half. Learners move fast. Do not slow them down |
| Segment 4 | Where test inputs 5 and 6 expose a wrong TODO-9 that passed everything else |
| Segment 5 | First conceptual jump. The after-model timing is the thing to make them state back |
| Segment 6 | Run the detector probe live. The false-positive result changes the room |
| Segment 7 | Short. The `trigger=None` fact is the whole segment |
| Segment 8 | Protect the time. Option B is the answer most architects defend before they see it |

**If time runs short**, cut Segment 0 and Segment 7 and keep 1, 3, 5, 6, 8. That still delivers the chain: errors, crashes, control, data, and the failure of control.
