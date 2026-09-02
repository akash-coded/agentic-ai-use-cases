# The map

Four surfaces, ~800 files, 66 discussion threads. This page exists because no single one of them can point at the other three.

| Surface | What it is | Best entry point |
| --- | --- | --- |
| 📚 **[Curriculum](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/modules)** | 16 modules · 102 notebooks · 92 exercises · 63 solutions | [START-HERE](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/docs/START-HERE.md) |
| 🧭 **[Field guide](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/cheatsheets)** | 77 reference pages — frameworks, runbooks, playbooks, interview guides | [Frameworks index](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/cheatsheets/frameworks) |
| 🧪 **[L.A.B. Simulator](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/labs)** | Auto-graded labs · Learn → Apply → Break | `python labs/runner/labctl.py next` |
| 💬 **[Discussions](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions)** | 66 threads, all tagged by track and level | [Index of every exercise and lab](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/64) |

**New here and want one link?** [START-HERE](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/docs/START-HERE.md).

---

## Pick a way in

| I want to… | Go |
| --- | --- |
| **Understand the concepts** | [Curriculum](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/modules) — read the module README first, always |
| **Prove I can build it** | [L.A.B. Simulator](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/labs) — graded, offline, no AWS account |
| **Look something up while working** | [Field guide](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/cheatsheets) |
| **Fix an error right now** | **[Error Index](Error-Index)** |
| **Fit this around a job** | **[Study Plans](Study-Plans)** |
| **Know what it will cost** | **[Cost Log](Cost-Log)** |
| **Find a specific thing** | **[Where do I find…?](Where-do-I-find-it)** |
| **Ten minutes, one idea, graded** | A [drill](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/labs/PATHWAY.md#the-drill-sequence) — post `/drill AGL-101` in the [Arena](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/75) |
| **See who is doing hands-on** | [Scoreboard](Scoreboard) · [Hands-on Tracker](https://github.com/users/akash-coded/projects/9) |
| **Get a lab graded without installing anything** | [Simulator Arena](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/75) — post a comment, a bot replies |
| **Ask a person** | [Q&A](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/categories/q-a) — check the [answered ones](Community-Answers) first |

---

## The three things worth knowing before you start

**1. Model access is not automatic.** It is granted per model, *per region*, on request, and approval is not always instant. Start [AWS setup](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/docs/setup/aws-account-setup.md) before you need it.

**2. Two things bill for existing, not for use.** OpenSearch Serverless collections and AgentCore runtimes. They are what people leave running by accident. [Teardown checklist](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/docs/setup/cost-controls.md#teardown-checklist).

**3. A lot of this needs no AWS account at all.** Modules 00, 01 and 15, every [L.A.B. lab](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/labs), `rag_by_hand.py` and `quality_gate.py`. That is 20+ hours of real work at zero cost while your model access is pending.

---

## What is on this wiki, and what is not

The repository is **canonical**: versioned, reviewed, and it ships with the code. Do not look for the curriculum here.

This wiki is the **connective and volatile layer** — the cross-surface maps, and the notes that would be embarrassing to freeze in a reviewed file:

| Page | Why it lives here |
| --- | --- |
| [Error Index](Error-Index) | Grows every time somebody hits a new one. No PR needed |
| [Model & Region Notes](Model-and-Region-Notes) | Availability changes monthly; a versioned file would be wrong within a quarter |
| [Cost Log](Cost-Log) | Real measured numbers from real people, not estimates |
| [Community Answers](Community-Answers) | Curated from discussions as they get answered |
| [Study Plans](Study-Plans) | Calendar-shaped, and everyone's calendar differs |
| [Maintainer Runbook](Maintainer-Runbook) | How the repo is run — not learner-facing |

**Anyone can edit these.** That is the point. [How to](Contributing-to-this-Wiki).
