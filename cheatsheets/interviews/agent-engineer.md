# Interview Guide · Agent Engineer

Both sides of the table. If you are **interviewing**, the questions are diagnostic. If you are **being
interviewed**, they are what to be ready for — and what a good answer sounds like.

---

## The five questions that separate people

### 1. "Walk me through what happens between the user's question and the answer."

**Weak:** "The agent thinks about it and calls tools."
**Strong:** describes the loop — model call, `stopReason`, tool dispatch, appending **both** the assistant
`toolUse` turn and the `toolResult` turn, next call, termination condition.

**The follow-up that reveals everything:** *"What happens if you forget to append the assistant message?"*
Anyone who has actually built the loop answers immediately: the model repeats the tool call, because from
its perspective it never asked.

### 2. "Your agent gives a wrong answer in production. Walk me through the first ten minutes."

**Weak:** "I'd look at the prompt."
**Strong:** stops the bleeding first, then gathers evidence — which model answered, turns per task,
citations present, empty tool results, abstention rate. Only then forms a hypothesis.

Reading the prompt first is the tell that someone has debugged agents in a notebook but not in production.

### 3. "How do you know it works?"

**Weak:** "We tested it. It works well."
**Strong:** names an [evidence rung](../frameworks/evidence-ladder.md). Describes a golden set with real
inputs, cases that currently fail, an abstention slice and an adversarial slice. Mentions a gate that
**fails the build**.

**Follow-up:** *"How was the golden set built?"* If it was built by labelling the agent's own output, it is
a mirror, not evidence.

### 4. "When would you not use an agent?"

**Weak:** "For simple tasks."
**Strong:** the control-flow test. If you can enumerate the steps in advance, it is a workflow. Bonus for
the routing pattern — send the known 80% to a cheap workflow and reserve the agent for the rest.

Candidates who cannot articulate when *not* to use an agent will build R4 systems for R2 problems.

### 5. "What does your agent do when it doesn't know?"

**Weak:** "It gives its best answer."
**Strong:** abstention is a designed, measured behaviour with a target rate, a structured output, and a
route to a human. Knows that confident-wrong is the failure that ends projects.

## Technical depth checks

| Area | Question | Listen for |
| --- | --- | --- |
| Tool design | "Model keeps picking the wrong tool. Why?" | The description is the bug; the model only sees the schema |
| Cost | "Cost doubled, traffic flat. Where do you look?" | Turns per task first — it multiplies four taxes |
| Context | "How do you decide top-k?" | Measure the accuracy curve; it peaks and falls |
| Memory | "Buffer, summary or vector?" | Trade-offs, and what each silently drops |
| Multi-agent | "When is a swarm wrong?" | No stop rule = unbounded; adding agents multiplies a bad prompt |
| Safety | "Agent must not issue refunds. How?" | Do not give it the tool. Not a prompt instruction |
| Reversibility | "How do you roll back a prompt change?" | Prompts versioned in the manifest, or they cannot |

## The practical exercise

Better than a whiteboard. Give a broken agent and 45 minutes.

**Setup:** a working loop with **one** seeded defect — the assistant `toolUse` turn is not appended.
**Watch for:** do they print the message array, or do they start rewriting the prompt?
**Great answer:** finds it in under 15 minutes, then asks "what test would have caught this?"

Alternative: give a tool whose description overlaps a neighbour's and watch them diagnose tool selection.

## Red flags

| Signal | Why it matters |
| --- | --- |
| Cannot describe the loop without a framework | Cannot debug it either |
| Never mentions cost | Will build something nobody can afford to run |
| "We just add it to the prompt" for every problem | Prompt-as-hammer; no engineering model |
| No concept of abstention | Will ship confident-wrong |
| Evaluation described as "we tried it" | E1 evidence for a production claim |
| Talks only about model choice | Model choice is rarely the bottleneck |

## Green flags

- Describes a failure they caused, and what they changed afterwards
- Distinguishes retrieval failure from generation failure by instinct
- Mentions who is on-call for the agent
- Has an opinion on framework choice **with a reason**, not an allegiance
- Asks what the abstention rate should be before asking what the accuracy target is

---

## If you are the candidate

**Prepare three stories:**
1. An agent you shipped, with the cost per task and how you measured it
2. A production failure, how you found it, and the guard you added
3. A time you argued for *not* building an agent

**Bring numbers.** "Roughly 60%" is weaker than "58% autonomous resolution on a 130-case golden set, 22% of
which are abstention cases."

**Study these:** [Autonomy Ladder](../frameworks/autonomy-ladder.md) ·
[Failure Signature Catalog](../frameworks/failure-signature-catalog.md) ·
[Evidence Ladder](../frameworks/evidence-ladder.md) ·
[Bedrock Converse](../quick-reference/bedrock-converse.md)

**Build first:** [Module 05](../../modules/05-agent-loop-no-framework-to-strands/) —
if you can write the loop by hand, question 1 is free.
