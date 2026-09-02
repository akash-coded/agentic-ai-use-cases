# The Simulator Arena

Submit a lab solution as a **discussion comment** and a bot grades it and replies in the thread — no
clone, no Codespace, no local Python. Useful on a phone, on a locked-down work laptop, or when you want
your reasoning visible to other people.

**Where:** any thread in
[Hands-on Labs](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/categories/hands-on-labs).

---

## Two kinds of thing to submit

| | Size | Shape | Submit with |
| --- | --- | --- | --- |
| **Drill** | 8–12 min | One idea, one function. Four kinds: `implement` (fill the TODO), `fix` (find the planted bug), `blank` (fill the blanks), `predict` (say what the code does, then check) | `/drill AGL-101` |
| **Lab** | 20–35 min | The full Learn → Apply → Break shape, with hidden checks | `/lab AGL-01` |

Either verb works for either kind. Drills are numbered `1xx` beside the lab they lead into, and chain with a
**Next** pointer: `AGL-101 → AGL-102 → TOOL-101 → RET-101 → MEM-101 → EVAL-101 → MAS-101 → PROD-101 → PDL-101 → AGL-01`.
Nine drills and you have touched every track once; the tenth step is your first full lab.

## The format

Two parts: a `/drill` or `/lab` line, and one `python` code block.

````markdown
/lab AGL-01

```python
def dispatch(tool_use, registry):
    tool_use_id = tool_use.get("toolUseId")
    name = tool_use.get("name")
    ...
```
````

Post it. Within a minute or two you get a threaded reply with every check, and — on failures — the line
explaining *why that check exists*.

Anything else in your comment is ignored, so explain your reasoning around the code block. That is the
part other people learn from.

---

## What the reply tells you

Not a diff. Each failing check carries the line explaining *why that check exists*. Then, from the drill's own
feedback file — written per drill, not generated:

- on a **pass**: the skill you just demonstrated, what to read to go deeper, and the next item
- on a **partial**: what that particular pattern of failure usually means, and one nudge
- on a **miss**: the one thing to change first

## What gets run

| | |
| --- | --- |
| ✅ **Public checks** | The same ones `lab run` gives you |
| ✅ **Break phase** | The failures that end real runs |
| ❌ **Hidden checks** | **Never here.** Publishing their output would spoil the lab for everyone reading the thread |

So a green reply in the Arena is *most* of the way, not all of it. For the hidden checks:

```bash
lab submit AGL-01
```

in a [Codespace](https://codespaces.new/akash-coded/aws-bedrock-agentcore-strands?quickstart=1) or locally.

---

## How your code is run

It executes on GitHub's runners, which means the design has to assume submissions are hostile:

- The grading job has **`permissions: {}`** — no `GITHUB_TOKEN` reaches it
- Your code runs in a container with **`--network none`**, 512 MB, 1 CPU, 128 PIDs, a read-only filesystem
  and a **45-second kill timeout**
- The comment body is passed as an **environment variable**, never interpolated into a shell command, so
  a comment cannot inject into the workflow
- The job that posts the reply never touches your code

Practical consequences for you: **no network, no filesystem, no long-running work.** Every lab is designed
to need none of those, so this only bites if you were doing something the lab did not ask for.

---

## For trainers: assigning work

Maintainers can assign drills or labs from any Hands-on Labs thread:

```
/assign @alice @bob AGL-101 TOOL-101 --session "Day 3" --due 2026-09-05
```

The bot replies with a per-item brief the learners can follow, records the assignment, and it appears under
**Assigned, not yet attempted** on the scoreboard until each learner posts a submission. Anyone else typing
`/assign` gets a polite pointer to `/drill`.

## Tracking

Every bot reply ends with an invisible ledger line. Discussions are therefore the **source of truth** for
attempts and assignments — public, auditable, and needing no extra permissions on the grading path. Three
derived views are rebuilt from it every six hours and after every Arena run:

| View | What it shows | Needs |
| --- | --- | --- |
| **[Scoreboard](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Scoreboard)** | Learners, attempts, passes, passes-after-retry, assigned-not-attempted, hardest items | nothing |
| **[Hands-on Tracker](https://github.com/users/akash-coded/projects/9)** | One row per learner × item, with outcome, attempt count, session and due date | `PROJECT_TOKEN` |
| **[Repo Pulse](https://github.com/users/akash-coded/projects/10)** | Hot threads, unanswered Q&A, open issues and PRs, what changed this week, Arena activity | `PROJECT_TOKEN` |

`GITHUB_TOKEN` cannot touch Projects v2, so the two boards need a fine-grained PAT with Projects read/write
stored as the `PROJECT_TOKEN` secret. Without it the scoreboard still updates and the run says so.

**A pass after a retry counts more than a first-time pass** on the scoreboard, deliberately. Retrying is the
behaviour being encouraged.

## Etiquette

- **Wrap a full working solution in `<details>`** if the thread is a shared exercise — let other people
  attempt it first.
- **Say what you decided and why.** Each lab's Learn phase asks for a decision; the Arena is a good place
  to argue about it, and the argument is more valuable than the code.
- **A failing submission is a fine thing to post.** "Here is my attempt and the check I cannot get past"
  gets better replies than silence.

---

## If the bot does not reply

| Symptom | Cause |
| --- | --- |
| Nothing at all | Your comment did not start with `/lab ` — that exact trigger is required |
| "I do not recognise that lab id" | Check the id against [PATHWAY.md](PATHWAY.md) |
| "no ```python block" | The fence needs the `python` (or `py`) language tag |
| "more than one ```python block" | Post one submission per comment |
| Reply says it timed out | 45 seconds. Usually an unbounded loop — which is itself the lesson in [AGL-03](catalog/agent-loop/AGL-03/) |

---

## Why this exists

The Arena is deliberately the *lightest* way in. The full experience is a
[Codespace](https://codespaces.new/akash-coded/aws-bedrock-agentcore-strands?quickstart=1) — hidden checks,
progress tracking, the prerequisite DAG, and the briefs open next to your editor.

But a fair number of people will never clone a repository to try something, and a comment box is a much
smaller ask than a dev environment. This meets them there, and the reply tells them what they would get by
going further.

---

[⬅️ L.A.B. Simulator](README.md) · [🗺️ Pathway](PATHWAY.md) ·
[💬 Hands-on Labs](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/categories/hands-on-labs)
