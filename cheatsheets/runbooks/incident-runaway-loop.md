# Runbook · The agent is looping

**Severity:** high — this is the failure mode that spends money fastest.
**First action:** stop it. Diagnose second.

---

## 0. Stop it now

| Situation | Action |
| --- | --- |
| Loop is running right now | Kill the runtime task / disable the route |
| Recurring on a specific input | Block that route; add the input to a quarantine list |
| Swarm with no stop rule | Disable the swarm path entirely until it has one |
| Cost still climbing | Set a service quota or disable the agent's model permission temporarily |

> There is no diagnostic worth doing while a loop is burning budget. Stop first.

## 1. Which loop?

| Pattern | Signature | Root cause |
| --- | --- | --- |
| **Tool ping-pong** | Same tool, same arguments, repeatedly | Assistant `toolUse` turn missing from history |
| **Non-convergence** | Different tools, never satisfied, hits max iterations | The tool does not answer the question the model is asking |
| **Swarm sprawl** | Agent count or turns growing | No termination condition |
| **Critique oscillation** | Producer and critic alternate forever | No round cap; critic never accepts |
| **Retry storm** | Same call, increasing intervals | Downstream failing; no circuit breaker |

## 2. Tool ping-pong — the most common

The model asks for a tool, you run it, and the model asks again identically. It has not seen the result.

**Check:** print the message array before the second call. You must have **both**:

1. the **assistant** message containing the `toolUse` block, appended verbatim
2. a **user** message containing the `toolResult` with the matching `toolUseId`

```python
messages.append(resp["output"]["message"])           # ← the step people skip
messages.append({"role": "user", "content": [
    {"toolResult": {"toolUseId": tu["toolUseId"],
                    "content": [{"json": out}], "status": "success"}}]})
```

See the [Converse cheat sheet](../quick-reference/bedrock-converse.md#tool-use--the-round-trip-everyone-gets-wrong).

## 3. Non-convergence

The model keeps trying because nothing it receives resolves its question.

1. Print the model's rationale each turn. What is it still trying to find out?
2. Is any available tool capable of answering that?
   - **No** → the agent cannot succeed. It should abstain, not loop. Add the abstention instruction.
   - **Yes, but returning empty** → tool silence. Return an explicit status, not `[]`.
3. Is the task genuinely underspecified? Then the correct behaviour is to ask the user, not to keep trying.

> A loop is often an **abstention that never happened**. The model does not know it is allowed to stop.
> See [Abstention Budget](../frameworks/abstention-budget.md).

## 4. Swarms and critique loops

Both are unbounded by construction unless you bound them.

```python
MAX_ROUNDS = 3
MAX_TOKENS_PER_TASK = 50_000

for round in range(MAX_ROUNDS):
    ...
    if tokens_used > MAX_TOKENS_PER_TASK:
        raise BudgetExceeded(task_id)   # raise; do not warn
else:
    escalate_to_human(task_id, reason="max_rounds")
```

**Measure whether round 2 ever changes an outcome.** On most workloads it does not, and the cap can be 1.

## 5. The permanent guards

Every one of these belongs in **code**, not in the prompt:

- [ ] Hard iteration cap that **raises**, with an escalation path
- [ ] Per-task token budget that raises when exceeded
- [ ] Stop rule on every swarm and critique loop
- [ ] Retry cap with exponential backoff and a circuit breaker
- [ ] Alert on `p95 turns per task > baseline + 1`

> A cap in the system prompt is a suggestion. A counter in the loop is a fact.

## 6. Before you close it

- [ ] Add the triggering input to the golden set
- [ ] Confirm the iteration cap now fires on it
- [ ] Record the cost of the incident — it makes the case for the guard
- [ ] Check [cost cliffs](../frameworks/cost-cliff-map.md) 1, 2 and 3 all have guards, not just the one that fired

## The post-mortem question

> **Was there a cap, and if so why did it not bind?**

A cap set too high is the same as no cap, discovered more expensively.
