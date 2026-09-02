<div align="center">

# 🧪 The L.A.B. Simulator

### Learn → Apply → Break

**Auto-graded, decision-driven labs for building agents that survive contact with production.**

Every lab makes you decide something before you write code, grades your implementation against checks that
explain themselves, and then **tries to break it** with the failure modes that do not appear in tutorials.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/akash-coded/aws-bedrock-agentcore-strands?quickstart=1)

**One click, zero setup.** Every lab is stdlib-only and offline, so the container is usable the moment it
starts — no dependencies to install, no AWS account, no credentials.

</div>

---

## Why this exists

Most coding-practice platforms give you a spec, a stub, and a happy-path test. You fill in the TODO, the
check goes green, and you have learned a mechanical transformation.

Agents do not fail on the happy path. They fail when a tool returns `[]` and the model reads it as
"nothing applies". They fail when a summary drops the one constraint the user stated. They fail when a
fallback model answers and nobody records which model it was.

So each lab here has three phases:

| | Phase | What happens |
| --- | --- | --- |
| **L** | **Learn** | A mental model, a diagram, and **one decision you must make** — with the trade-offs laid out and the answer withheld. Your decision changes what you build. |
| **A** | **Apply** | Implement against a spec. Public checks you can see, hidden checks on submit. Every check says what it teaches when it fails. |
| **B** | **Break** | Your working solution meets the cases that end real runs: `BaseException` from a library, a chunk bigger than the whole budget, a summariser that returns more than it was given. Survive them. |

The Break phase is the point. Anyone can pass a happy-path test.

---

## Start in 60 seconds

**In Codespaces** — [open one](https://codespaces.new/akash-coded/aws-bedrock-agentcore-strands?quickstart=1) and type `lab next`. That is the whole setup.

**Locally:**

```bash
python labs/runner/labctl.py list          # the catalog
python labs/runner/labctl.py next          # what you can start right now
python labs/runner/labctl.py start PDL-01  # copies a starter into your workspace
python labs/runner/labctl.py show  PDL-01  # the brief
python labs/runner/labctl.py run   PDL-01  # public checks
python labs/runner/labctl.py submit PDL-01 # public + hidden, records the attempt
python labs/runner/labctl.py break PDL-01  # now survive the Break phase
python labs/runner/labctl.py progress      # per-track progress bars
```

No dependencies. No API keys. Python 3.11+ and nothing else — every lab is deterministic and offline, so
the whole catalog runs in CI in seconds.

> **New here?** [`PDL-01`](catalog/product/PDL-01/) needs no prerequisites and no cloud account, and it is
> the decision every agent project gets wrong first. Or read the
> **[pathway](PATHWAY.md)** to see how the labs compose.

---

## The catalog

<!-- LABS:START -->

**10 labs built** · 4h 40m of hands-on work · every one runs offline, with no AWS account.

### 📋 Product & PDLC
<sub>Decide what to build before building it</sub>

| Lab | Difficulty | Time | Teaches | Break phase |
| --- | --- | --- | --- | --- |
| **[PDL-01](catalog/product/PDL-01/)** · Agent, workflow, or script | `easy` | 25m | autonomy ladder, control flow, scoping | ✓ |

### 🔁 Agent Loop
<sub>The loop, by hand, until nothing is magic</sub>

| Lab | Difficulty | Time | Teaches | Break phase |
| --- | --- | --- | --- | --- |
| **[AGL-01](catalog/agent-loop/AGL-01/)** · Dispatch a tool call | `easy` | 20m | tool dispatch, toolUse / toolResult, unknown-tool handling | ✓ |
| **[AGL-02](catalog/agent-loop/AGL-02/)** · Close the loop | `easy` | 25m | message history, role alternation, parallel tool calls | ✓ |
| **[AGL-03](catalog/agent-loop/AGL-03/)** · Stop the loop | `medium` | 30m | termination, step budget, oscillation | ✓ |

### 🔧 Tools
<sub>Schemas, contracts and honest failure</sub>

| Lab | Difficulty | Time | Teaches | Break phase |
| --- | --- | --- | --- | --- |
| **[TOOL-03](catalog/tools/TOOL-03/)** · Fail honestly: no bare empties | `medium` | 25m | failure honesty, empty vs absent, tool contracts | ✓ |

### 🧠 Memory
<sub>What the agent keeps, and what it drops</sub>

| Lab | Difficulty | Time | Teaches | Break phase |
| --- | --- | --- | --- | --- |
| **[MEM-01](catalog/memory/MEM-01/)** · A buffer that cannot overflow | `medium` | 30m | context budget, eviction policy, summarisation threshold | ✓ |

### 📚 Retrieval
<sub>Grounding you can actually verify</sub>

| Lab | Difficulty | Time | Teaches | Break phase |
| --- | --- | --- | --- | --- |
| **[RET-05](catalog/retrieval/RET-05/)** · Citations that survive verification | `medium` | 35m | citation integrity, grounding, provenance | ✓ |

### 🕸️ Multi-Agent
<sub>Topologies, and what they cost</sub>

| Lab | Difficulty | Time | Teaches | Break phase |
| --- | --- | --- | --- | --- |
| **[MAS-02](catalog/multi-agent/MAS-02/)** · Cost a topology before you build it | `medium` | 30m | handoff multiplier, context re-transmission, merge cost | ✓ |

### 🔬 Evaluation
<sub>Proving it works, and blocking it when it does not</sub>

| Lab | Difficulty | Time | Teaches | Break phase |
| --- | --- | --- | --- | --- |
| **[EVAL-03](catalog/evaluation/EVAL-03/)** · A gate that can say no | `medium` | 30m | release gating, absolute vs average metrics, threshold governance | ✓ |

### 🚀 Production
<sub>Deployed, observable, reversible</sub>

| Lab | Difficulty | Time | Teaches | Break phase |
| --- | --- | --- | --- | --- |
| **[PROD-02](catalog/production/PROD-02/)** · Failover that cannot be silent | `medium` | 30m | model failover, silent degradation, observable fallback | ✓ |

<!-- LABS:END -->

More labs are specified and open for contribution — see the
**[full pathway](PATHWAY.md#the-complete-pathway)** for the 41-lab map and
[how to author one](CONTRIBUTING-A-LAB.md).

---

## What makes a lab here different

**A decision, not just a spec.** [MEM-01](catalog/memory/MEM-01/) does not tell you what to evict when the
buffer overflows. It lays out the options, tells you every buffer has an eviction policy and most have an
accidental one, and asks you to choose. Then the hidden checks assume you can defend it.

**Checks that teach.** A failing check does not print a diff. It prints what you got wrong and why it
matters:

```
FAIL  an unknown tool becomes an error result, not an exception
      The loop must survive the model inventing a tool.
      why this matters: Raising here turns a recoverable turn into an outage.
```

**Failures from real systems.** The Break phases are not edge cases invented for difficulty. `SystemExit`
from a library that calls `sys.exit()`. A footnote `[1]` inside a retrieved chunk corrupting your citation
map. A summariser returning more tokens than it was given. Each has ended a real run.

**Self-verifying.** CI proves every reference solution passes all three phases **and** that every starter
fails — so no lab can ship with TODOs that do not actually need doing.
That gate has already caught four bugs in these labs' own reference solutions.

---

## The PDLC thread

Each lab's Learn-phase decision produces a fragment of a real product artefact, and they accumulate:

| Lab | Stage | Artefact fragment it produces |
| --- | --- | --- |
| [PDL-01](catalog/product/PDL-01/) | Discovery | The rung each use case actually needs |
| [TOOL-03](catalog/tools/TOOL-03/) | Spec | Your tool return contract |
| [MAS-02](catalog/multi-agent/MAS-02/) | Spec | Your topology's H×, and what it buys |
| [AGL-03](catalog/agent-loop/AGL-03/) | Build | Your termination policy |
| [MEM-01](catalog/memory/MEM-01/) | Build | Your eviction policy |
| [RET-05](catalog/retrieval/RET-05/) | Validate | Your citation contract |
| [EVAL-03](catalog/evaluation/EVAL-03/) | Release | Your gate thresholds |
| [PROD-02](catalog/production/PROD-02/) | Operate | Your failover policy and its signal |

Write each into `workspace/<LAB>/DECISION.md` as you go. By the end you have not just working code — you
have the [seven PRD artefacts](../docs/prd/) filled in for a system you actually built. That is the
difference between finishing exercises and being able to defend a design.

---

## Drills — the bite-sized sequence

Nine 8–12-minute drills in [`drills/`](drills/), thread-native and bot-graded, in four kinds: **implement**,
**fix** (a planted bug), **blank**, and **predict** (say what the code does before running it). They chain:

`AGL-101 → AGL-102 → TOOL-101 → RET-101 → MEM-101 → EVAL-101 → MAS-101 → PROD-101 → PDL-101 → AGL-01`

Each reply names the skill you demonstrated and points at the next one. Do them in the
[Simulator Arena](ARENA.md) with nothing installed, or locally with `lab grade --lab AGL-101 --file mine.py`.
Progress lands on the **[scoreboard](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Scoreboard)**.

## Three ways to run a lab

| | Setup | You get |
| --- | --- | --- |
| 🚀 **[Codespaces](https://codespaces.new/akash-coded/aws-bedrock-agentcore-strands?quickstart=1)** | One click | Everything — hidden checks, progress, the DAG, briefs beside your editor |
| 💻 **Local** | `git clone`, Python 3.11+ | The same, on your machine |
| 💬 **[Simulator Arena](ARENA.md)** | None. A comment box | Public + Break checks, graded by a bot in the thread |

The Arena is the lightest way in — paste a solution as a discussion comment and a bot replies with every
check. Hidden checks never run there, deliberately: publishing them would spoil the lab for the thread.

## Grading in CI

Fork the repo, commit your solutions under [`workspace/`](workspace/), and open a pull request. The
[labs workflow](../.github/workflows/labs.yml) grades every solution you have touched and comments the
result — the same feedback you get locally, on every push.

Maintainers get `labctl verify`, which is what keeps the catalog honest.

---

## How this relates to the rest of the repo

| | |
| --- | --- |
| [**Curriculum**](../modules/) | 16 modules — where you *learn* the concepts, with slides, notebooks and exercises |
| [**Field guide**](../cheatsheets/) | 77 reference pages — the frameworks each lab links back to |
| **L.A.B. Simulator** | Where you *prove* you can build it, graded, one bite-sized decision at a time |

Every lab links to the module that teaches its concept and the framework that explains its failure mode.
You can start here and read backwards, or work the curriculum and use labs as checkpoints.

---

[🏠 Repository](../) · [🗺️ Pathway](PATHWAY.md) · [✍️ Author a lab](CONTRIBUTING-A-LAB.md) ·
[📚 Curriculum](../modules/) · [🧭 Field guide](../cheatsheets/)
