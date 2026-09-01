# 00 · Idea Brief — TravelMind

> One page. Written before anyone commits time. If it cannot be argued with, it is not finished.

**Status:** approved at Gate 1 · **Owner:** Product · **Date:** stage artefact

## The problem

Travel operations staff spend a large share of their day on refund and disruption enquiries that follow
published policy. The policy is written down. The answer is usually deterministic given the booking, the
fare rules and the disruption reason. Staff are slow not because the decision is hard but because the
information is scattered across three systems.

## Who has it

Front-line travel operations agents, and the customers waiting on them.

## Why now

Policy documents are already digitised. Booking and disruption data are already reachable by API. The
missing piece — a system that can read policy, call the systems, and explain its reasoning — is now
buildable.

## What we would build

An assistant that answers a refund or disruption enquiry by retrieving the applicable policy, calling the
booking system for the specific case, and returning a decision with its reasoning and the policy citation.

## Why an agent rather than a workflow

The enquiry does not arrive classified. Which systems to call, and in what order, depends on what the
previous call returned — a cancelled-flight refund follows a different path from a voluntary change, and
you do not know which you have until you have looked. Control flow is genuinely decided at runtime.

> Run the [four-quadrant classifier](../../modules/00-agentic-foundations/activities/H1-01_Four-Quadrant_Classifier.xlsx)
> before accepting this reasoning. It is the most common place a project goes wrong.

## Success, stated so it can be argued with

- 60% of refund enquiries resolved without human handoff, within 90 days of release
- Under $0.04 per resolved enquiry, all-in
- Zero policy-contradicting answers in the evaluation set — this is a release blocker, not a target

## What we are not building

- Anything that moves money. The agent recommends; a human approves.
- Anything customer-facing in v1. Internal staff only.
- Multi-language. English only in v1.

## Biggest risk

The agent answers confidently from parametric knowledge instead of retrieved policy. Mitigation is
mandatory citation: an answer without a citation is a failure, not a fallback.

## Decision requested

One engineer, two weeks, to produce a [discovery PRD](01-discovery-prd.md) and a cost model.

---

**Gate 1 outcome:** proceed. **Condition:** classifier must be run and attached before Gate 2.
