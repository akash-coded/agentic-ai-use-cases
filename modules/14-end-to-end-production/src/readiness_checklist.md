# Production Readiness Checklist

Use this as a gate, not a wish-list. If a row is unchecked, the agent is a
prototype in production clothing. Ten items; all ten, or it is not done.

### Deploy
- [ ] **Health and port contract.** `GET /ping` returns healthy; the container
  listens on 8080. The load balancer can tell it is alive.
- [ ] **Least-privilege execution role.** Invoke only the models you use, write
  only the log group you need. No long-lived access keys in code or image.

### Model
- [ ] **Inference profile pinned.** Model id carries the `us.` prefix. Retries
  (adaptive) and a request timeout are set. Throttles are expected at scale.

### Versioning and gate
- [ ] **Versioned artifact.** Prompt + config + model in one manifest, with a
  prompt sha. Prompt logic lives outside app code so it versions on its own.
- [ ] **Promotion gate.** Eval pass rate, cost per resolution, p95 latency, and
  safety all checked. The gate blocks promotion on failure, it does not warn.

### Rollout and rollback
- [ ] **Staged rollout.** Shadow or canary, then progressive, behind a feature
  flag so deploy and activation are separate decisions.
- [ ] **Tested rollback.** A named `rollback_target`; rollback redirects traffic
  rather than redeploying; you have actually run it once.

### Operate
- [ ] **Bounded routing fallback.** If you use a gateway, the fallback is behind
  a circuit breaker, and you evaluate the fallback path, not just the primary.
- [ ] **Observability from day one.** Trajectory spans plus CloudWatch are on at
  deploy. You cannot debug a non-deterministic agent from logs you did not keep.
- [ ] **Cost guardrail.** A per-resolution budget and an alarm on spikes. A
  silent loop is a quality bug and a cost bug at once.

### Transfer (optional but telling)
- [ ] **Domain-swappable.** Tools and prompts are externalized, so the same
  pipeline serves a second domain by swapping them (see CargoTrace in the deck).

---

**How to read a failed row.** It is not a nice-to-have you defer. It is the
specific way this agent will fail in production, named in advance. Fix it before
you call it shipped.
