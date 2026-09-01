# Solution Walkthrough · Design on Paper

This guide gives the correct answer to every item, the reasoning behind it, and, for the multiple-choice questions, why each wrong option is tempting and where it fails. Each walkthrough is written to stand on its own, so you can read it without the exercise open in front of you.

A note on how to read it: the questions are not independent. Six ideas recur across the stations (the trace invariant, the autonomy gate, the partition-and-de-PII rule, the ambiguity theme, the retry-plus-idempotency pair, and the "throw a bigger model or window at it" anti-reflex). The final section lists those threads, because seeing them is most of the point.

---

# Station 1 · Two planes

The station drills one habit: when something goes wrong, name the plane the fault came from before you start fixing. The control plane is the part that decides (planner, prompts, routing, eval gates, allowlists). The execution plane is the part that does (tool calls, API hits, database writes, model invocations, retries, network). You classify a fault by where it *originates*, and you accept that the *fix* often lives in the opposite plane.

### 1.1 · Classify the plane

| # | Fault | Plane | Why |
|---|---|---|---|
| 1 | Planner chose `send_quote` for an opted-out account | Control | The wrongness is in the choosing. The tool would have run fine; the planner simply decided to take an action it should not have. |
| 2 | `send_quote` returned HTTP 500 | Execution | The decision to call the tool may have been perfectly correct. The fault arose in the doing, when the downstream service failed. |
| 3 | Planner skipped the approval gate for an 18% discount | Control | Routing through a gate is a deciding step. The planner failed to route, so the fault is in the control logic. |
| 4 | `crm_update` timed out after 30 seconds | Execution | A timeout is a tool-call and network fault, squarely in the doing. |
| 5 | Router sent an expansion case to the Renewal Agent | Control | Routing is deciding. The classifier picked the wrong destination. |
| 6 | A retry storm hammered the CRM API | Execution | Retries and network behaviour are execution-plane by definition. |

The one worth pausing on is fault 6. The runaway retries manifest in the execution plane, which is where the deck places retries, so the classification is Execution. The *fix*, a maximum-attempts cap or a circuit breaker, is a design decision you might think of as control-side configuration. That split is the whole lesson of the station: the plane a fault originates in and the plane its defence lives in are frequently different, which is exactly why you keep separate alarms, traces, and incident playbooks for each.

### 1.2 · Read the trace

**Answer: B, a control-plane failure. The planner issued a discount above the 15% autonomy boundary without firing the approval gate.**

The trace shows the planner deciding on an 18% discount, then calling `send_quote` with no `request_approval` step in between, and the call returning 200 OK. Nothing failed in the execution plane; the tool did exactly what it was told. The defect is that the planner decided to act beyond its authority, and that is a deciding failure.

Why the other options fail:

- **A** invents a downstream email bounce that the trace does not show. It is the reflex of assuming the tool broke, and it ignores the 200 OK sitting in the evidence.
- **C** invokes state drift (the CRM not updating), but the trace stops at the output and shows no such thing. It is plausible-sounding and unsupported.
- **D** treats the 200 OK as proof the design worked. This is the trap the whole station is built around: a success code tells you the *call* succeeded, not that the *decision* was authorised. The green status is precisely what hides a control-plane bug from anyone watching only execution signals.

### 1.3 · Control-plane defences

**Answer: A, C, D, and F.**

- **A**, a strict tool allowlist, constrains what the planner is permitted to decide to call.
- **C**, a trace-checked invariant, is an assertion on the decision graph, and eval gates are control-plane.
- **D**, an approval gate on discounts above 15%, is routing and gating logic.
- **F**, router unit tests, test the classification decision itself.

The two you leave out, **B** (backoff and idempotency) and **E** (an alarm on tool error rate), are not wrong to have; they simply guard the execution plane. This is the useful part of the question. A hallucinated action or a mis-routing bug will never trip an error-rate alarm, because nothing errored. You catch deciding bugs with deciding-side defences, and no amount of execution-plane monitoring substitutes for them.

### 1.4 · One test for the hallucinated action

**Answer: B. Assert that every user-visible "quote sent" statement has a matching successful `send_quote` event in the same trace.**

The hallucinated action is the planner claiming work it never performed. The only assertion that catches it ties the *claim* to the *evidence*: if the user was told "quote sent" but no successful `send_quote` event exists in that trace, the test fails and the claim is exposed.

Why the other options fail:

- **A**, a latency assertion, measures speed and says nothing about whether the action happened.
- **C**, a temperature ceiling, is a knob that might lower how often the model hallucinates in general, but it proves nothing about any specific session and is not a test.
- **D**, checking the CRM record exists before the session, validates an unrelated precondition.

The reusable shape here is worth memorising: *every customer-visible claim of type X must have a corresponding successful event of type X in the same trace.* You will see it again in the synthesis pre-mortem (7.5).

---

# Station 2 · Design discipline

Three artefacts, three owners, three review lenses. The station drills the idea that ownership tracks abstraction, and that a soft PRD is the most expensive kind of technical debt because everything downstream inherits it.

### 2.1 · Owner and reviewer

| Artefact | Owner | Reviewer is checking |
|---|---|---|
| PRD | B, Product Manager | X, is this the right problem, with measurable success and clear autonomy limits |
| HLD | A, Architect | W, does the component topology connect and hold together |
| LLD | C, Engineer | Y, are schemas, state shape, and retry or timeout policy precise enough to test |

The ownership ladder follows the abstraction ladder. The Product Manager owns the problem framing (who, what, success, limits). The Architect owns how the system is shaped (the components and how they connect). The Engineer owns the precise contracts (schemas, state, timeouts) that make the thing testable. The reviewer questions climb the same ladder: feasibility of the topology at HLD, testability of the detail at LLD, and problem-fit at PRD.

Option **Z**, "is the marketing copy on-brand," is a distractor that maps to none of the three. It is in the bank to test whether you will force-fit a plausible item that does not belong. Brand review is real work; it is simply not what any of these three artefacts exists to catch.

### 2.2 · Build the PRD from the pool

**Answer: 1-A, 2-B, 3-C, 4-D, 5-E, 6-F, 7-G, 8-H. Items I, J, K, and L stay unused.**

| PRD question | Answer | What makes it correct |
|---|---|---|
| Who is the user | A | Names both persona and surface (internal CSM, renewals console), specific enough to change the design. |
| Goal, one sentence | B | A single sentence that includes the clean-escalation path, not just the happy path. |
| Success KPI | C | Countable and time-bound: percent auto-completed, cycle time, CSAT. |
| Autonomy boundary | D | The three-tier free / approval / prohibited split with the actual thresholds. This is the load-bearing line the topology later has to enforce. |
| Failure looks like | E | Names concrete unacceptable outcomes, so you can design against each. |
| Rollback path | F | Every side-effecting action records its inverse; a failed run reverses completed steps. |
| PII surface | G | Catalogues the touchpoints and the handling (masked in logs, excluded from any retrieved cache). |
| Cost ceiling | H | A per-run base plus a hard stop with human approval above it. |

The four distractors are not random noise. Each is a real way a PRD goes soft, and learning to reject them on sight is the skill:

- **I**, "deliver a better renewals experience," is a vague aspiration standing in for a goal. It gives the agent no target to optimise.
- **J**, "always use the latest model," is solutioning (a model choice) leaking into requirements, where it does not belong.
- **K**, "send as many renewal emails as possible," is a throughput vanity metric that optimises the wrong thing.
- **L**, "store the full contract PDF in long-term memory," is a convenience that directly violates the "no PII in retrieved or cached context" rule. It returns as the planted memory leak in 7.2, so flagging it here pays off later.

### 2.3 · The only defensible KPI

**Answer: B. Percent of renewals auto-completed without escalation, tracked weekly.**

A KPI has to be countable and it has to have a cadence. Option B gives you both. The others describe sentiments or vague directions with no unit and no denominator: "feel more valued," "responds quickly," and "fewer complaints" cannot be measured, and the last is a lagging proxy with no baseline. If you cannot state the numerator, the denominator, and the cadence, you do not yet have a KPI.

---

# Station 3 · Mermaid as lingua franca

The station drills reading a design as a graph and testing whether the graph actually says what the designer thinks it says.

### 3.1 · Pick the correct agentic loop

**Answer: B.**

An agent is defined by its feedback edge: after acting and observing, control returns to the planner so it can decide the next step. Only B has the observe-back-to-planner edge and a proper terminal path (reply, then eval gate, then surface). The others each break a different property that an agent needs:

- **A** is a straight pipeline with no loop at all. It is a one-shot tool call, not an agent.
- **C** loops observe back to the tool, so the tool fires again without the planner ever re-deciding. That is an infinite execution loop with no re-planning and no exit.
- **D** runs planner, tool, observe, surface exactly once, but the observation never returns to the planner, so the decider cannot act on what it just learned.

This is the same distinction as the four-quadrant rubric from Half 1. The loop is what makes a system "multi-step and non-deterministic." A lacks iteration, C lacks re-planning, and D lacks feedback to the decider.

### 3.2 · Spot the wrong arrow

**Answer: B. The edge `AC -->|discount 18%| SQ` sends an above-policy discount straight to `send_quote` without passing the approval gate.**

Policy requires anything above 15% to pass manager approval first. The diagram does contain an approval node, but it dangles off the Recommendation Agent and never sits between the decision and the action, so it approves nothing. The wrong arrow is the one that reaches a side-effecting action while carrying an above-threshold value, with no gate in the path.

The other edges (Triage to Health, Terms Lookup to Recommendation, Recommendation to Action) are ordinary control-flow edges with no policy attached, so none of them is the fault.

The takeaway travels directly to 7.4: an approval node that is not on the path between the decision and the side effect is decoration, not enforcement.

### 3.3 · Trace the flow

**Answer: User goal, then Planner, then Tool needed = No, then Reply, then Eval gate, then Surface.**

With all data already cached, the planner reaches the decision node and takes the "No" branch, because no tool is needed. The turn then produces a reply, passes the eval gate, and reaches the surface. The tool-and-observe branch is skipped entirely. The detail worth noticing is that even the no-tool path still passes the eval gate before anything surfaces; output validation is not optional just because no tool ran.

### 3.4 · Why Mermaid

| # | Statement | Answer | Why |
|---|---|---|---|
| 1 | A Mermaid diagram can be diffed in a pull request | True | A Mermaid file is text, so a pull request shows the exact change line by line. |
| 2 | A PNG updates automatically when the code changes | False | A PNG is a binary snapshot. It goes stale silently the moment the design moves, which is the reason the program bans PNG-in-wiki for living diagrams. |
| 3 | GitHub and GitLab render Mermaid natively | True | Both render Mermaid in the browser without any export step. |
| 4 | Mermaid replaces the need for an HLD | False | Mermaid is the notation the HLD uses, not the HLD itself. The HLD also carries component responsibilities, the tool list, the memory model, and the gates, none of which a single flowchart captures. |

---

# Station 4 · Prompts as policy

The station drills the precedence order and the five specific ways prompts break, and it insists that the failures are structural, not model-quality problems you can buy your way out of.

### 4.1 · Rank prompt strength

**Answer: System, then Tool, then User.**

The system prompt encodes policy and persona and changes rarely, so it sits highest. The tool prompt tells the planner when and how to use a specific tool and changes when that tool changes. The user prompt is the request for this turn and changes every turn, so it is weakest. A clean way to remember it: authority is inversely related to how often the layer changes.

### 4.2 · Match failure mode to defence

**Answer: Ambiguity to C, Conflicting instructions to B, Missing schema to A, Context overflow to D, Injection to E. Items F and G stay unused.**

| Failure mode | Defence | Why this defence targets the cause |
|---|---|---|
| Ambiguity | C | Ambiguity is a missing-input problem, so the fix is to require the under-specified fields before acting, not to hope the model guesses better. |
| Conflicting instructions | B | The failure is an unresolved precedence, so you resolve conflicts in the system prompt and let the higher layer win. |
| Missing schema | A | The failure is an unstructured output, so you enforce a typed contract and reject on parse failure. |
| Context overflow | D | The failure is exceeding the window, so you budget the context and truncate or summarise to fit with headroom. |
| Injection through retrieved content | E | The failure is hostile text entering trusted context, so you treat retrieved content as data and quarantine instruction-like patterns. |

Options **F** (raise the temperature) and **G** (switch to a bigger model) stay unused because neither touches the structural cause of any of the five. They are the "throw a model at it" reflexes, and a senior audience should reject both on sight.

### 4.3 · Classify the snippet

**Answer: 1-M1, 2-M2, 3-M4, 4-M3, 5-M5.**

| # | Snippet | Mode | The tell |
|---|---|---|---|
| 1 | "find me cheap options" | M1 Ambiguity | No currency, class, or date; the model must fill the gap with a guess. |
| 2 | System says concise, user says detailed | M2 Conflicting instructions | Both instructions are perfectly clear; they simply conflict, and with no resolution rule the model picks arbitrarily. This is not ambiguity. |
| 3 | Prompt plus 40 chunks plus history exceeds the window | M4 Context overflow | The total input is larger than the window, so the model silently drops something. |
| 4 | Code expects JSON, model returns prose | M3 Missing schema | No structured-output contract, so the parser fails or half-succeeds. |
| 5 | Retrieved doc carries a SYSTEM override | M5 Injection | The hostile instruction rode in through retrieved content into trusted context. |

Two distinctions carry the weight. Snippet 2 is a hierarchy problem, not ambiguity, because clarity is not the issue. Snippet 5 is injection specifically because the instruction arrived through *retrieved* content, which is the dangerous vector, and is quite different from a user simply typing "ignore your rules," which the precedence hierarchy already handles.

### 4.4 · Hierarchy in practice

**Answer: C. Refuse the autonomous 20% and route to the approval gate, because the system rule outranks the user turn.**

The system prompt caps discounts at 15% without approval. The CSM asking to push 20% is a user-turn instruction, the weakest layer. The correctly designed agent declines to apply 20% on its own and routes to the approval gate instead.

Why the other options fail:

- **A** claims the user has final say over the system prompt, which inverts the hierarchy. The human-in-the-loop authority is exercised *through* the approval gate, not by overriding policy inline.
- **B** applies the 20% and logs a warning, but the prohibited action still happened. A log is forensics, not a control.
- **D** hands a hard policy boundary to case-by-case model judgment, which is precisely what the boundary exists to prevent.

The point that carries forward: human-in-the-loop is a gate in the path, not a suggestion the user can wave away.

### 4.5 · What actually enforces the hierarchy

**Answer: B. Training and design convention; the model is steered to follow it but can still be pushed off it, which is why later checks exist.**

The hierarchy tells you the intended precedence. It is not a hard runtime constraint (A), there is no compiler rejecting conflicting prompts at build time (C), and it is not the identity provider's role permissions, which govern human access rather than prompt authority (D). This is the honest limit of the whole "prompts as policy" idea: treating the hierarchy as if it were a hard guarantee is how teams get surprised by injection. The hierarchy states the intent; the checkpoints enforce it when the model wobbles.

### Run these · prompt-then-predict

All three predictions are **B**. What matters is not the prediction but what you watch for when you run it.

- **Run 4A (hierarchy override).** A well-aligned model declines the autonomous 25% discount and states that approval is required. Watch whether your model holds the line or caves to "skip the approval nonsense." Some models hold and some can be nudged off, and that variance is the lesson: it is the reason you never rely on the prompt alone.
- **Run 4B (ambiguity).** The model should surface the missing inputs (term, tier, discount limit) rather than invent a confident quote. If it invents numbers, you have just watched ambiguity produce a plausible but fabricated artefact in real time.
- **Run 4C (injection).** The model should summarise only the entitlements and ignore the embedded SYSTEM OVERRIDE. Watch whether it leaks the contract value or the owner's email. This is the exact injection pattern from the live-session trace, reproduced on demand. Note why option C (escalate and stop) is not the precise answer: the question is about *handling*, and the correct immediate behaviour is to treat the block as data and answer the real request. Escalation may follow operationally, but not obeying the injected instruction is the behaviour being tested.

---

# Station 5 · Memory and retrieval

The station drills two taxonomies and, more importantly, the boundaries between their categories, because confusing the categories is how context poisoning and cross-tenant leaks start.

### 5.1 · Fill the memory table

| Layer | Lifetime | Holds | Nimbus example |
|---|---|---|---|
| Short-term | Minutes | a, current run state | 1, this renewal's draft quote and current step |
| Episodic | Hours to days | b, specific task history | 2, last attempt failed because the CRM write timed out |
| Long-term | Months+ | c, user-stable facts | 3, this account prefers annual billing |
| Behavioural | Months+ | d, patterns from usage | 4, this CSM's accounts renew near quarter-end |
| Operational | Continuous | e, system-level state | 5, `send_quote` p95 latency and cost per run |

The discriminator is lifetime plus the question each layer answers. Short-term is "what is happening in this run right now." Episodic is "what happened in prior specific runs," meaning events with a timestamp. Long-term is "stable facts about this account," with no expiry expected. Behavioural is "patterns inferred across many interactions," also long-lived but derived rather than stated. Operational is "system health," continuous and not about any single account.

The deliberate trap is that long-term and behavioural share the "months+" lifetime. They are separated by *source*, a stable stated fact versus an inferred pattern, not by how long they live. That distinction matters in practice, because behavioural facts should usually be re-derived and re-validated rather than frozen once and trusted forever.

### 5.2 · Which layer

| # | Item | Layer | Why |
|---|---|---|---|
| 1 | Mid-way through this run's 3-step expansion | L1 Short-term | State of the run happening now. |
| 2 | Contact prefers email, never calls | L3 Long-term | A stable preference with no expiry. |
| 3 | Two runs ago the gate rejected a 30% discount | L2 Episodic | A specific past event with a timestamp. |
| 4 | CRM error rate over the last hour | L5 Operational | System health, continuous, not about one account. |
| 5 | This segment expands after onboarding milestone 3 | L4 Behavioural | A pattern inferred across many accounts. |

The pairs to keep crisp are 1 versus 3 (this-run state versus a prior-run event) and 4 versus 5 (a segment pattern versus a system metric).

### 5.3 · What must never be stored

**Answer: A, C, D, and F.**

- **A**, raw card numbers and OTPs, are secrets and never belong in memory.
- **C**, cross-tenant data in one store, is a data-isolation breach; memory must be partitioned per tenant.
- **D**, an unconfirmed model assertion, poisons future retrieval; only tool-confirmed facts earn a place.
- **F**, transient retry noise, is clutter, not signal, and degrades future context.

The two you keep, **B** (seat count) and **E** (billing cycle), are legitimate stable facts that belong in long-term memory. The through-line is simple: store confirmed, partitioned, durable signal; never store secrets, cross-tenant data, hallucinations, or noise. Item C returns as the planted leak in 7.2, and item D is the storage-side of the hallucination pattern from 1.4.

### 5.4 · Match RAG concern to the failure it prevents

**Answer: Chunking to D, Embedding to G, Metadata to E, Ranking to C, Freshness to B, Access control to A, Cost to F. Item H stays unused.**

| RAG concern | Failure it prevents |
|---|---|
| Chunking | D, a clause split across two chunks so neither is retrievable as a complete answer. |
| Embedding | G, after swapping the embedding model, old and new vectors are no longer comparable. |
| Metadata | E, you cannot filter by source, date, tenant, or access level at query time. |
| Ranking | C, retrieval returns loosely related passages and the top hit is rarely the right one. |
| Freshness | B, an answer cites a contract clause that was amended last week. |
| Access control | A, wrong-tenant documents surface to the wrong customer. |
| Cost | F, query latency and re-indexing spend balloon under load with no budget. |

Each concern maps to a failure that only that concern prevents. The one to underline is access control, because it produces a *security* failure rather than a quality one, and it is the concern demos skip most often. It pairs with 5.6.

### 5.5 · The hardest RAG problem

**Answer: B. Deciding what to retrieve when the user's question is ambiguous.**

Chunk size, vendor choice, and index compression are engineering knobs with known answers. Knowing what to retrieve when the question underspecifies what is relevant is the open problem, because no lookup tells you the user's intent, and retrieval quality collapses precisely when the query is vague. This is the same ambiguity theme from 4.2 and 4.3, now on the retrieval side.

### 5.6 · Where tenant security belongs

**Answer: B. In the retriever itself, filtering documents before they reach the context, in addition to the API.**

Tenant security has to live where the data is selected. A gateway alone (A) does not stop the retriever from pulling another tenant's document into context. A system-prompt instruction (C) is a request, not a control, and the model can be pushed off it, as 4.5 established. UI hiding (D) is cosmetic, because the data has already left the boundary. Enforce access where documents are chosen, not where they are displayed.

---

# Station 6 · Tools, registries, cost

The station drills the runtime contract every tool needs, the governance a registry adds, and the arithmetic that makes agent sessions cost roughly an order of magnitude more than a single chatbot turn.

### 6.1 · Match requirement to what breaks without it

**Answer: Schema to C, Idempotency key to A, Timeout to B, Retry policy to D, Permission scope to E. Item F stays unused.**

| Tool requirement | What breaks without it |
|---|---|
| Schema | C, malformed inputs and outputs flow through untyped and the parser fails or half-succeeds. |
| Idempotency key | A, a retried or duplicated call double-charges, double-sends, or double-books. |
| Timeout | B, a slow dependency hangs the whole run with no bound. |
| Retry policy | D, transient failures either give up instantly or hammer the dependency with no backoff. |
| Permission scope | E, an agent invokes an action it should never have been able to touch. |

Option **F**, "the tool has no owner in the catalog," stays unused because ownership is a *registry* concern, not one of the five runtime-contract fields. It is tempting because "owner" feels like tool metadata, and that temptation is the hook into the next topic. The five-part contract is about runtime safety; owner, SLA, and deprecation are governance and belong in the registry.

### 6.2 · Idempotency scenario

**Answer: B. Two identical renewal quotes.**

With no idempotency key, a dropped response followed by a retry produces two real quotes, because the second call is indistinguishable from a fresh one.

Why the other options fail:

- **A** assumes the first call failed, but the first call may well have succeeded on the server even though the client never saw the response. That is the whole reason duplicates happen.
- **C** assumes the API deduplicates by default. It does not; you have to supply a key so the server can recognise the retry as the same logical operation. This is the dangerous assumption the question is designed to surface.
- **D** assumes retries are blocked, but nothing blocks them here, and in the synthesis the tool is configured to retry three times, which is exactly what makes the missing key dangerous.

Retries and idempotency are a pair. Retry without an idempotency key is a duplication engine. This drives 7.1 directly.

### 6.3 · Which requirement

**Answer: B. Timeout.**

"A slow tool that never errors is worse than one that fails fast" is an argument about bounding time. A timeout converts an unbounded hang into a fast, handleable failure. Schema, scope, and retry each address a different property; only the timeout addresses the hang.

### 6.4 · With or without registries

**Answer: 1-N, 2-W, 3-N, 4-W, 5-N, 6-W.**

| # | Statement | Without or With | Why |
|---|---|---|---|
| 1 | Three teams each build their own `send_email` | Without | Duplication is the signature of no registry. |
| 2 | Audit is a query, not an investigation | With | A registry makes capabilities queryable. |
| 3 | No single owner, no SLA, no deprecation path | Without | Invisibility of ownership is the signature of no registry. |
| 4 | One canonical tool, one schema, one owner | With | Canonicalisation is what a registry provides. |
| 5 | Nobody knows which agents run where | Without | No discoverability. |
| 6 | Reusable across teams, versioned, observable | With | Reuse and versioning are registry outcomes. |

A registry converts tribal, duplicated, unauditable capability into a single discoverable contract. The tell for "without" is duplication and invisibility; the tell for "with" is canonical and queryable.

### 6.5 · Which registry

**Answer: 1-T, 2-A, 3-A, 4-T.**

| # | Entry | Registry | Why |
|---|---|---|---|
| 1 | `send_quote` schema and owning team | Tool | It describes a tool and its contract. |
| 2 | Recommendation Agent capabilities and cost per run | Agent | It describes an agent and what it costs. |
| 3 | Which agents are deployed in the workspace | Agent | It is an inventory of agents. |
| 4 | SLA and deprecation date for `kb_search` | Tool | It is lifecycle metadata for a tool. |

The tool registry answers "what tools exist and what are their contracts." The agent registry answers "what agents exist, what can they do, and what do they cost." The only thing you decide is whether the entry describes a tool or an agent.

### 6.6 · Compute the cost

**Answer: B, 336,000 tokens.**

The formula is multiplicative:

$$\text{tokens per session} = \text{base prompt} \times \text{turns} \times (1 + \text{retrieval}) \times (1 + \text{sub-agents}) \times (1 + \text{retries}) \times (1 + \text{eval})$$

Worked step by step:

| Step | Operation | Running total |
|---|---|---|
| Base prompt | 1,200 | 1,200 |
| Turns | × 4 | 4,800 |
| Retrieval over 6 chunks | × (1 + 6) = × 7 | 33,600 |
| 3 sub-agents | × (1 + 3) = × 4 | 134,400 |
| 25% retry rate | × (1 + 0.25) = × 1.25 | 168,000 |
| Eval-as-judge | × (1 + 1) = × 2 | 336,000 |

Each wrong option comes from a specific, diagnosable error:

- **A, 216,000**, used 6 and 3 directly instead of (1 + 6) and (1 + 3). It forgot the "+1" in each factor.
- **C, 168,000**, forgot the eval multiplier and stopped one step early, treating eval-as-judge as × 1.
- **D, 268,800**, forgot the retry multiplier, treating the 25% retry rate as × 1.

The "+1" exists in each factor because retrieval, sub-agents, retries, and evaluation *add* token passes on top of the base flow; the base flow still runs, so the factor is (1 + x), not x. Dropping the "+1" is the most common error and it always under-counts.

### 6.7 · The biggest lever

**Answer: B. Drop eval-as-judge.**

Because the formula is multiplicative, the biggest lever is always the largest whole multiplier, not the biggest-looking absolute number.

| Change | Factor | Reduction |
|---|---|---|
| B, drop eval-as-judge (× 2 to × 1) | 0.50 | about 50% |
| A, trim base 1,200 to 1,000 | 0.833 | about 17% |
| D, remove one of six chunks (× 7 to × 6) | 0.857 | about 14% |
| C, retry 25% to 10% (× 1.25 to × 1.10) | 0.88 | about 12% |

This is the most useful cost intuition in the station. Eval-as-judge is a silent doubling, so questioning whether you need model-graded evaluation on every run is worth far more than shaving prompt tokens. It reframes cost work from "make the prompt shorter," which is marginal, to "challenge the times-N stages," which is structural.

---

# Station 7 · Synthesis · Audit the Nimbus design

The station is where everything converges. The design looks production-ready at a glance, and it is not, because the one thing that is correct (the gate) is the thing you notice first, and the misses are hidden in the contracts, the memory plan, and the metric.

### 7.1 · The unsafe tool

**Answer: B. `send_quote`, because it retries three times with no idempotency key, risking duplicate quotes to the customer.**

This is the retry-plus-idempotency pair from 6.2 made concrete. A retried send with no key produces a second real quote. The other options are distractors: a 5-second timeout on a read (A) is reasonable, a 30-second timeout on a write (C) is generous but not itself unsafe, and "reads should never be retried" (D) is false, because idempotent reads are safe to retry.

### 7.2 · The memory leak

**Answer: C. A retrieved-context cache holding contract text, keyed by account and shared workspace-wide.**

This single entry breaks two stated rules at once. Contract value is PII that must be excluded from any retrieved-context cache (PRD slot 7, and pool item G in 2.2), and memory must be partitioned per tenant (5.3, item C). A cache shared across the whole workspace is a cross-tenant leak waiting to happen. The other three memory entries are correct: short-term state with a TTL, a legitimate long-term preference, and operational metrics. This is the L distractor from 2.2 made real; the exercise plants the exact convenience the PRD stage taught you to reject.

### 7.3 · The weak PRD line

**Answer: B. Success KPI, "improve renewal experience."**

The line has no unit, no denominator, and no cadence, so it fails the measurable bar, exactly as in 2.3. The other three stated lines are well-formed: a concrete autonomy threshold, an inverse-recording rollback, and a hard cost ceiling.

### 7.4 · Does the topology enforce the approval boundary

**Answer: B. Yes. Every path to a side-effecting action passes through the gate, and only above-threshold cases route to approval.**

This is the item you must *not* flag as broken. Trace the paths: both `send_quote` and `crm_update` sit downstream of the Action Agent, which is reached only via the gate's "No" branch or via approval after a "Yes." Every path to a side effect passes through the gate.

Why the other options fail:

- **A** claims `send_quote` can be reached without the gate, which is true of the broken diagram in 3.2 but not of this one.
- **C** wants approval before the Recommendation Agent, which would gate before the discount is even known. The gate belongs after the recommendation and before the action, which is exactly where it sits.

The contrast with 3.2 is deliberate. Same case, two topologies: one puts the gate in the path, the other leaves it dangling. Recognising the correct one is as important as spotting the broken one, because it stops reflexive fault-finding, which is a real failure mode in design review.

### 7.5 · Failure pre-mortem

**Answer: Looping to A, Silent failure to B, Hallucinated step to C, Context poisoning to D, State drift to E, Unsafe autonomy to F. Item G stays unused.**

| Failure pattern | Defence | Note |
|---|---|---|
| Looping | A, iteration cap on the lookup and health agents, then escalate | Bounds a runaway loop. |
| Silent failure | B, verify the CRM write landed, alarm on mismatch | Catches a 200 that did not actually propagate. |
| Hallucinated step | C, trace invariant that "quote sent" requires a matching `send_quote` event | The invariant from 1.4, applied here. |
| Context poisoning | D, partition the cache per tenant, keep contract value out, TTL session memory | The fix for the leak in 7.2. |
| State drift | E, explicit state schema, resume-from-checkpoint | Keeps a multi-step run coherent. |
| Unsafe autonomy | F, approval gate fires on cumulative discount or value crossing the threshold | The enforcement validated in 7.4. |

Option **G**, "increase the model's context window," stays unused because a bigger window addresses none of the six patterns. It is the "throw capacity at it" reflex, the sibling of the unused options in 4.2. Notice how many defences here are call-backs: C is the trace invariant, D is the leak fix, and F is the gate. The pre-mortem is where the separate threads of the exercise tie together.

### 7.6 · Production-ready checklist

**Answer: 1 False, 2 False, 3 True, 4 False, 5 False.**

| # | Check | Answer | Why |
|---|---|---|---|
| 1 | Every side-effecting tool has an idempotency key | False | `send_quote` has none (7.1). |
| 2 | The retrieved-context cache is tenant-partitioned and PII-free | False | It is neither (7.2). |
| 3 | The autonomy boundary is enforced in the topology | True | The gate is correct (7.4). |
| 4 | The success KPI is measurable | False | It is a sentiment, not a metric (7.3). |
| 5 | Each of the six failure patterns has a named defence | False | They are defended only once you complete 7.5; the design as given does not yet wire them in. |

Three concrete fixes fall out of this: add an idempotency key to `send_quote`, partition and de-PII the retrieved cache, and replace the KPI with a measurable one, then wire in the pre-mortem defences. Row 3 is the single True, and it is instructive: because the gate is right, the design *feels* finished, while the real gaps hide in the tool contracts, the memory plan, and the metric.

---

# Threads that recur across the exercise

The stations were built to share connective tissue. Tracing these threads is how the individual answers become a mental model rather than thirty-six separate facts.

- **The trace invariant.** "Every user-visible claim of type X needs a matching successful event of type X in the same trace" appears in 1.4 and again as the hallucinated-step defence in 7.5. It is the single most reusable test in the whole day.
- **The autonomy gate.** Defined in the PRD (2.2, item D), drawn wrong in 3.2, and drawn right in 7.4. The lesson is that a boundary stated in words is worthless until it sits on the path between the decision and the side effect.
- **Partition and de-PII.** The rule shows up as a rejected PRD convenience (2.2, item L), as a memory prohibition (5.3, item C), and as the planted leak in 7.2. Convenience that violates a stated constraint is the most common way a good PRD gets quietly undone downstream.
- **The ambiguity theme.** The same root cause appears as a prompt failure mode (4.2 and 4.3) and as the hardest RAG problem (5.5). Underspecified input is not a model-quality problem; it is a design problem you solve by demanding the inputs.
- **Retry plus idempotency.** Introduced in 6.2 and cashed in at 7.1. Retry without an idempotency key is a duplication engine, and the two are never designed separately.
- **The "throw a bigger model or window at it" anti-reflex.** The unused distractors in 4.2 (bigger model, higher temperature) and 7.5 (bigger context window) are all the same reflex. For a room full of architects, recognising and refusing that reflex is a large part of what separates a demo from a system.
