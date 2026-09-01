# You are in a ready-made lab environment

Everything is installed. Nothing to configure. **No AWS account needed** — every lab here runs offline on
the standard library alone.

---

## Three commands

```bash
lab next                 # what you can start right now
lab start AGL-01         # copies a starter into your workspace
lab run   AGL-01         # public checks
```

Then, when those pass:

```bash
lab submit AGL-01        # + the hidden checks
lab break  AGL-01        # now survive the failures that end real runs
```

> Prefer clicking? **Terminal → Run Task** (or `⇧⌘P` → *Tasks: Run Task*) has all of these, with a lab
> picker. `Lab · what's next` is the default build task — `⇧⌘B`.

---

## Start here if you have never done this

**[`PDL-01`](catalog/product/PDL-01/)** — no prerequisites, no code required for the first half, and it is
the decision every agent project gets wrong first.

```bash
lab start PDL-01 && lab show PDL-01
```

If you would rather write code immediately: **[`AGL-01`](catalog/agent-loop/AGL-01/)**.

---

## How a lab works

| | Phase | What happens |
| --- | --- | --- |
| **L** | Learn | A mental model, a diagram, and **one decision with the answer withheld**. Your choice changes what you build |
| **A** | Apply | A spec. Public checks you can see, hidden checks on submit. Every check explains what it teaches when it fails |
| **B** | Break | Your *working* solution meets `SystemExit` from a library, a chunk bigger than the whole context budget, a footnote `[1]` corrupting your citation map |

The Break phase is the point. Passing a happy-path test is not evidence of much.

**Write your decision down** in `labs/workspace/<LAB>/DECISION.md`. They accumulate into the
[seven PRD artefacts](../docs/prd/) — you finish with a working system *and* the paperwork to defend it.

---

## The rest of the repository

| | |
| --- | --- |
| [`modules/`](../modules/) | 16 modules — the curriculum. **Notebooks need `lab deps` first** (a few minutes) |
| [`cheatsheets/`](../cheatsheets/) | 77 reference pages — every lab links to the relevant ones |
| [`labs/PATHWAY.md`](PATHWAY.md) | Why the labs are ordered the way they are |
| [Discussions](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions) | 66 threads, and a [Simulator Arena](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/categories/hands-on-labs) where a bot grades submissions |

## Want to run the notebooks too?

```bash
lab deps        # installs boto3, strands, langchain, litellm, opensearch-py …
```

Then add AWS credentials — **Codespaces secrets** are the clean way:
*Settings → Codespaces → Secrets*, add `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`.
They are injected as environment variables and never touch the repository.

⚠️ Before Module 02, read [cost controls](../docs/setup/cost-controls.md). Two things bill for *existing*,
not for use.

---

## Nothing to clean up

This container is disposable. Stop or delete the Codespace and nothing lingers — no AWS resources are
created by any lab.

**Your work is not disposable though.** Commit it, or it goes with the container:

```bash
git add labs/workspace && git commit -m "my solutions" && git push
```

Push to a fork and [the workflow grades your PR](../.github/workflows/labs.yml).
