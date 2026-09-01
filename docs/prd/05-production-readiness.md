# 05 · Production Readiness — TravelMind

> The pre-flight. Every line is either ticked with evidence, or the release does not happen.
> Pairs with [Module 14's readiness checklist](../../modules/14-end-to-end-production/src/readiness_checklist.md).

**Status:** Gate 4 artefact · **Owner:** Engineering

## Release summary

| Field | Value |
| --- | --- |
| Version | from `version_manifest.json` |
| Model | primary + fallback, both recorded |
| Prompt version | versioned separately from code |
| Image digest | immutable reference |
| Evaluated at | timestamp of the passing gate run |

## Checklist

### Correctness
- [ ] All contract tests pass
- [ ] Golden set pass rate ≥ 0.85
- [ ] Safety pass rate = 1.0
- [ ] Adversarial slice passes — including policy text that instructs the agent to ignore policy
- [ ] Abstention cases abstain; they do not guess

### Grounding
- [ ] Every policy claim carries a citation
- [ ] Policy index freshness verified against the corpus source
- [ ] Citation points at a passage that actually supports the claim — spot-checked by a human on 10 cases

### Cost and performance
- [ ] Cost per enquiry ≤ $0.08 measured, not estimated
- [ ] p95 latency ≤ 12 s
- [ ] Budget alarm configured and tested
- [ ] Token growth per turn bounded — verified on the longest golden-set conversation

### Security
- [ ] All tools read-only; verified by reviewing each tool's IAM permissions
- [ ] Identity scoped per tool, least privilege
- [ ] PII guardrail tested with deliberate PII input
- [ ] No credentials in code, notebooks or notebook outputs

### Operability
- [ ] Trace id returned on every response
- [ ] CloudWatch queries documented for the three most likely failures
- [ ] Answering model logged on every response — failover cannot be silent
- [ ] On-call runbook exists and names a person

### Reversibility
- [ ] Previous version manifest deployable without a rebuild
- [ ] Rollback rehearsed, not assumed
- [ ] Rollback decision criteria written down before release

### Human factors
- [ ] Ops agents briefed that this recommends and does not decide
- [ ] Handoff path tested end to end
- [ ] Feedback route exists for ops agents to flag a wrong answer

## Sign-off

| Role | Name | Date | Decision |
| --- | --- | --- | --- |
| Engineering | | | |
| Product | | | |
| Ops lead | | | |

## Rollback criteria — agreed before release

Roll back if any of: a policy-contradicting answer reaches an ops agent; autonomous resolution drops below
35% over a rolling day; cost per enquiry exceeds $0.12; or p95 latency exceeds 20 s.

Decided in advance, because nobody makes this call well at 2 a.m.

---

**Next:** [post-launch review](06-post-launch-review.md)
