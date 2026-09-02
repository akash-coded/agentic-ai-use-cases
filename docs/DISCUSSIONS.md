# Using Discussions

Sixty-plus threads across eight categories. This is how they are organised, what belongs where, and how
to find anything.

The live version of this page is the
[discussion map](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/65) — same
content, but you can reply to it.

---

## Where to post what

| You want to… | Post in | Why there |
| --- | --- | --- |
| Ask something and get an answer | **[Q&A](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/categories/q-a)** | Answerable — good answers get marked and stay findable |
| Report a broken notebook or wrong doc | **[Issues](https://github.com/akash-coded/aws-bedrock-agentcore-strands/issues/new/choose)** | Not a discussion. Issues get tracked and closed |
| Work an exercise, or compare answers | **[Exercises](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/categories/exercises)** | Reply *in that exercise's thread* |
| Work a multi-hour lab or capstone | **[Hands-on Labs](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/categories/hands-on-labs)** | Same, for longer builds |
| **Get a lab solution graded by a bot** | **[Simulator Arena](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/75)** | Post `/lab <ID>` + a python block; a workflow grades it and replies in-thread |
| Share what you built | **[Show and tell](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/categories/show-and-tell)** | The most persuasive content here |
| Propose a topic, lab or improvement | **[Ideas](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/categories/ideas)** | Feeds the [extension roadmap](extension-roadmap.md) |
| Vote on what gets built next | **[Polls](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/categories/polls)** | Reaction-vote threads that steer the roadmap |
| Anything else | **[General](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/categories/general)** | Introductions, war stories, opinions |
| See what changed | **[Announcements](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/categories/announcements)** | Maintainer-only, low traffic |

**Discussion or issue?** An issue has a *closed* state — something is broken and a change fixes it. A
discussion does not. "This notebook fails" is an issue. "Why is it done this way?" is a discussion.

---

## The label taxonomy

Every practice thread carries three labels. They compose, so you can filter to exactly what you want.

| Dimension | Labels |
| --- | --- |
| **Track** | `foundations` `product` `bedrock` `agent-loop` `tools` `frameworks` `memory` `retrieval` `multi-agent` `agentcore` `interop` `evaluation` `production` |
| **Level** | `foundational` · `intermediate` · `advanced` |
| **Format** | `code` · `no-code` · `design` |
| **Type** | `exercise` · `lab` · `capstone` · `guide` · `reference` · `vote` |

Filter in the Discussions search box:

```
label:"track: retrieval" label:"level: foundational"
label:"format: no-code"                     # no AWS account needed
label:"type: capstone"
```

**Level means how much it assumes**, not how long it takes. `foundational` needs nothing before it;
`advanced` assumes several tracks.

---

## Finding things

1. **[The index](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/64)** — every
   exercise and lab, grouped by track, sorted by level.
2. **Labels** — the table above.
3. **The [Q&A category](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/categories/q-a)**
   — questions with marked answers, which is usually faster than asking again.

---

## Asking well

Four things turn a question that sits for a week into one answered in an hour:

- **The module or lab** — "Module 11" or "AGL-02"
- **The exact error**, pasted in full. Not summarised — the exact string is what makes it searchable
- **Your region**
- **What you already tried**, including anything from [troubleshooting](setup/troubleshooting.md)

> ⚠️ **Remove your AWS account ID and any credentials before pasting.** Account IDs here are the
> placeholder `123456789012`. This is not hypothetical: a real account ID was found in an existing thread
> and scrubbed.

## Answering well

Beginners asking beginner questions is what the category is for. "Just read the docs" helps nobody. If you
know the answer, the two minutes it takes to write it saves someone an evening.

Where a question has a definite answer, maintainers mark one — that is what makes Q&A worth searching.

---

## Conventions

| | |
| --- | --- |
| **Reply in the thread** | One exercise thread with fifteen replies beats fifteen threads |
| **Titles survive as search results** | "Help!!" and "question about RAG" get retitled |
| **Spoilers wrapped** | `<details><summary>Solution</summary>` so others can still attempt it |
| **Code in fences**, with a language tag | And errors in full |
| **Disagreement is welcome** | On specifics. Several exercises have more than one defensible answer |

---

## The Simulator Arena

[Hands-on Labs](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/categories/hands-on-labs) doubles as a graded arena. A comment containing a
`/lab <ID>` line and one ```python block is picked up by the
[Simulator Arena workflow](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/.github/workflows/discussion-lab.yml), run against that lab's
public and Break checks, and answered with a threaded reply.

Hidden checks never run there — publishing their output would spoil the lab for everyone reading. Full
mechanics and the sandbox design: [ARENA.md](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/labs/ARENA.md).

**Drills** are the 8–12-minute version (`/drill AGL-101`), nineteen of them in two chained laps across every track.
`/leaderboard` and `/progress` work in any Hands-on Labs thread, and a **weekly digest** lands in Announcements every Monday.
**Maintainers assign** with `/assign @user AGL-101 --session "Day 3" --due 2026-09-05`; the bot briefs the
learner and the item shows as *assigned, not yet attempted* on the
[scoreboard](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Scoreboard) until
they submit. Every bot reply carries an invisible ledger line — Discussions are the source of truth for
attempts, and the [Hands-on Tracker](https://github.com/users/akash-coded/projects/9) and
[Repo Pulse](https://github.com/users/akash-coded/projects/10) boards are rebuilt from it.

---

## For maintainers

New practice threads need a track, a level and a format label, and a row in the index. The index is
generated from live data — regenerate it rather than hand-editing.

Titles follow `<Topic> <N> · <what it teaches>`. No day numbers, no cohort references, no schedule
artefacts — those mean nothing to someone arriving from a search engine, and this repository's discussions
are a large part of how people find it.

**Not creatable via the API** (both are UI-only, in repo settings):

- **Discussion categories** — there is no `createDiscussionCategory` mutation
- **Native polls** — `CreateDiscussionInput` takes only title, body and category, so the poll threads here
  use reactions as votes

---

[🏠 Repository](../) · [💬 Discussions](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions) · [🤝 Contributing](../CONTRIBUTING.md)
