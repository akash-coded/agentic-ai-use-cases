# Runbooks

Written to be opened **during** an incident, not read in advance. Each starts with the action that stops
the damage and only then moves to diagnosis.

---

## Incidents

| Runbook | Opens with | Severity |
| --- | --- | --- |
| 🔴 **[Wrong answers](incident-wrong-answers.md)** | Decide whether to keep serving | High |
| 💸 **[Cost spike](incident-cost-spike.md)** | Traffic or a cliff? Two different problems | Med-high |
| 🐌 **[Latency regression](incident-latency-regression.md)** | Split into three clocks first | Medium |
| ♾️ **[Runaway loop](incident-runaway-loop.md)** | **Stop it. Diagnose second.** | High |
| 📉 **[Stale knowledge base](incident-stale-knowledge.md)** | How old is the index? | High, silent |

## Operations

| Runbook | For |
| --- | --- |
| ✍️ **[Shipping a prompt change](deploy-prompt-change.md)** | The most ungoverned change in most agent systems |
| ↩️ **[Rolling back](rollback.md)** | Four things must roll back together — prompts are the usual gap |
| 📅 **[First 30 days in production](first-30-days-in-production.md)** | A schedule, window by window |
| 🎁 **[Inheriting an agent](inheriting-an-agent.md)** | Containment → observability → reversibility → evidence |

---

## The triage table

Symptom → runbook. Pin this somewhere.

| Symptom | Start here |
| --- | --- |
| Users report wrong or invented answers | [Wrong answers](incident-wrong-answers.md) |
| Bill jumped | [Cost spike](incident-cost-spike.md) |
| Responses got slow | [Latency regression](incident-latency-regression.md) |
| Tasks never finish / turns climbing | [Runaway loop](incident-runaway-loop.md) |
| Answers cite outdated policy | [Stale knowledge base](incident-stale-knowledge.md) |
| Quality dropped with no deploy | [Wrong answers](incident-wrong-answers.md) § failover |
| Nobody knows how this system works | [Inheriting an agent](inheriting-an-agent.md) |

## The five facts to gather before any diagnosis

Each is one log query. Together they eliminate most of the
[Failure Signature Catalog](../frameworks/failure-signature-catalog.md).

1. **Which model answered?**
2. **How many turns did the task take?**
3. **What were the input tokens on the last call?**
4. **Were any tool results empty?**
5. **Were citations present?**

If you cannot answer these in ten minutes, your first work item is
[observability](../quick-reference/observability.md), not the incident.

## Every post-mortem ends with the same question

> **How long was this happening before we noticed?**

More than a day means it is a monitoring failure, whatever the technical cause. That is the finding.

---

[⬅️ Field guide](../) · [🧠 Frameworks](../frameworks/) · [📋 Playbooks](../playbooks/)
