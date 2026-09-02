# Changelog

Notable changes to this curriculum. Dates are when the change landed on `main`.

The format is loosely [Keep a Changelog](https://keepachangelog.com/). This is teaching material rather
than a released library, so there are no semantic versions — but breaking changes to structure are called
out, because people bookmark deep links.

---

## 2026-09-02 · Drills, assignments, and the boards that read the Arena

### Added
- **`/leaderboard`**, **`/progress`**, and a **weekly digest** posted to Announcements — all built from the ledger
- **Drills** — nineteen bite-sized, bot-graded items under `labs/drills/` in two laps in four kinds (implement, fix, blank,
  predict), chained across every track and ending at the first full lab
- **Skill-aware replies** — each Arena reply names the skill demonstrated, what to read, and the next item;
  misses get the drill's own diagnosis and one nudge, written per drill
- **`/assign`** for maintainers, with per-learner briefs and tracked assignments
- **A ledger in every bot reply**, making Discussions the source of truth for attempts
- **A live [Scoreboard](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Scoreboard) wiki page**, rebuilt every six hours and after every Arena run
- Boards: **Hands-on Tracker** (#9), **Repo Pulse** (#10), and **Agentic PDLC · Lifecycle Reference** (#8)
- **Codespaces**: one-click environment, `lab` command with completion, VS Code tasks, welcome page
- `labctl grade --json` and drill support in the runner and `verify`
- Four runnable public gists: the [history invariant](https://gist.github.com/akash-coded/12cd36b5e5ced3e0c5414af3abffa221), an [honest tool result](https://gist.github.com/akash-coded/e3748d8f0accfedf0a2509ee16195d51), a [release gate](https://gist.github.com/akash-coded/908a2f096a89de29d3b3221244773a1b), and an [H× calculator](https://gist.github.com/akash-coded/407c5e9ddcca84afe7099439591d3ec2)

### Needs a secret
- The two live boards are synced only when `PROJECT_TOKEN` (a fine-grained PAT with Projects read/write)
  exists. `GITHUB_TOKEN` cannot access Projects v2. The scoreboard works without it.

## 2026-09-01 · The field guide

### Added
- **[Field guide](cheatsheets/)** — 77 reference pages
  - 17 original frameworks with a procedure and an output: Autonomy Ladder, Token Tax Ledger, Handoff
    Multiplier, Abstention Budget, Grounding Triangle, Blast Radius Grid, Evidence Ladder, Failure
    Signature Catalog, Cost Cliff Map, Silent Degradation Watchlist, Context Budget Ledger, Three Clocks,
    Tool Surface Audit, Reversibility Test, Demo-to-Production Gap, Scope Fence, Value Trace, and the
    Agent Readiness Scorecard that composes them
  - 10 quick-reference sheets: Converse API, Strands, LangChain/LangGraph, AgentCore, RAG, IAM,
    observability, model selection, MCP/A2A, prompting
  - 9 runbooks for incidents and operations
  - 4 strategic playbooks
  - 6 interview guides, both sides of the table
  - 17 role-based how-tos across engineers, PMs, architects, business analysts, QA and engineering managers
- **[Extension roadmap](docs/extension-roadmap.md)** and its [public board](https://github.com/users/akash-coded/projects/6) — five phases, 22 specified items
- Index pages for `modules/`, `docs/`, `projects/`, `docs/concepts/`, `docs/setup/`, `docs/reference/`
- Every module README now links the field-guide pages relevant to it
- Social preview image, and its source
- `freshness.yml` — weekly link check that opens an issue when something rots
- `welcome.yml` — first-time contributor guidance
- `NOTICE.md` — third-party attribution

### Fixed
- **Licence.** The restructure commit had overwritten `LICENSE` with an MIT-0 file copied from a bundled
  AWS sample, wrongly attributing copyright to Amazon. The project's own MIT licence is restored.
- `bedrock-agentcore` moved from a pinned `==1.14.0` to a patched `>=1.18.1` floor across four requirements
  files; `mcp` lockfile bumped. Cleared 6 high-severity advisories.
- CI runs on Python 3.12 — the notebook-generator scripts under `labs/rag-labs/build/` use 3.12 f-string
  syntax. The labs themselves still run on 3.11.

---

## 2026-09-01 · Restructure

### Changed — **breaking for deep links**
- 118 flat root files reorganised into **16 topic modules** under `modules/`, each with
  `slides/ notebooks/ exercises/ solutions/ activities/ src/`. Any link to a root-level file from before
  this date will 404 — the [curriculum index](modules/) is the place to re-find things.

### Added
- ~200 previously unpublished files imported from the source material: **every exercise solution**, all of
  Module 04 (Agent Builder), Module 09 (LLM memory), Module 14 (end-to-end production), the full
  [`ragkit`](modules/10-rag-opensearch-litellm/labs/rag-labs/ragkit/) retrieval library, and the Module
  07/08/10 exercise and solution sets
- `docs/` — START-HERE, 5 learning paths, architecture HLD plus 16 per-module LLDs, portable-vs-AWS
  concept maps, 7 sample PRDs, setup and troubleshooting guides
- README with the curriculum map and reference architecture
- `CONTRIBUTING`, `CODE_OF_CONDUCT`, `SECURITY`, `CITATION.cff`, `.gitignore`, `requirements.txt`
- Issue, PR and discussion templates; `validate.yml` CI

### Removed
- Client branding from filenames, markdown, notebooks and the XML inside 31 PowerPoint/Excel files
- A real AWS account ID (replaced with the placeholder `123456789012`)
- Leaked local filesystem paths (replaced with `/workspace/`)
- AgentCore deploy logs, traces, a vendored 5,300-file dependency cache, and build output

---

## Before 2026-09-01

61 commits of course material published as it was delivered across three professional cohorts. Preserved
in history; the file layout from that period no longer exists on `main`.
