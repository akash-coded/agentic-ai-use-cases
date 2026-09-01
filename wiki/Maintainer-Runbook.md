# Maintainer Runbook

How this repository is actually run. Not learner-facing — it lives here rather than in `docs/` because it is operational, and it changes as the tooling does.

---

## The four surfaces, and what governs each

| Surface | Governed by | Gate |
| --- | --- | --- |
| `modules/` | Review | `Validate` workflow |
| `cheatsheets/` | Review | `Validate` workflow |
| `labs/` | Review + **self-verification** | `L.A.B. Simulator` workflow |
| Discussions | Labels + conventions | Human |

## CI, and what each job protects

| Workflow | Protects against |
| --- | --- |
| **Validate** | Broken notebook JSON, Python syntax errors, broken relative links, leaked secrets/account IDs/local paths, client branding returning |
| **L.A.B. Simulator** | A lab shipping broken: every reference must pass all three phases, every starter must **fail**, the index must be current, no lab may touch the network |
| **Freshness** (weekly) | Link rot — opens or comments on an issue when something breaks |
| **Welcome** | First-contribution friction |

**The account-ID check is the one to never weaken.** It greps for any 12-digit number that is not the placeholder `123456789012`. It has already caught a real leak.

---

## Adding a module

1. `modules/NN-topic/` with `slides/ notebooks/ exercises/ solutions/ activities/ src/`
2. A `README.md` matching the existing shape — objectives, concept table, ordered sequence, recording row, common mistakes, folder map, navigation
3. An LLD at `docs/architecture/lld/NN-topic.md`
4. Rows in the root `README.md` table, `modules/README.md`, and the relevant [learning paths](https://github.com/akash-coded/aws-bedrock-agentcore-strands/tree/main/docs/learning-paths)
5. A **Field guide for this module** section linking the relevant frameworks

## Adding a lab

Seven files; `labctl verify` enforces the two rules that matter.

```bash
python labs/runner/labctl.py verify          # references pass, starters fail, DAG acyclic
python labs/runner/labctl.py index --write   # regenerate the catalog table
```

Then mark it ✅ in [`PATHWAY.md`](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/labs/PATHWAY.md). Full guide: [`CONTRIBUTING-A-LAB.md`](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/labs/CONTRIBUTING-A-LAB.md).

> `verify` caught four real bugs in the labs' own reference solutions during authoring. Never bypass it.

## Adding a discussion

Every practice thread needs a **track**, a **level** and a **format** label, and a row in the [index](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/64).

Titles: `<Topic> <N> · <what it teaches>`. No day numbers, no cohort references, no schedule artefacts — discussions are a large part of how people find this repository, and those mean nothing in a search result.

Taxonomy and conventions: [`docs/DISCUSSIONS.md`](https://github.com/akash-coded/aws-bedrock-agentcore-strands/blob/main/docs/DISCUSSIONS.md).

---

## Content hygiene — the standing rules

Three things have leaked before and are now checked:

| Never | Placeholder |
| --- | --- |
| Real AWS account IDs | `123456789012` |
| Local filesystem paths | `/workspace/` |
| Client or cohort branding | — |

**Notebook outputs are committed on purpose** — seeing expected output is part of the teaching. That is exactly why they leak. Before committing a notebook you ran:

```bash
grep -rlE '[0-9]{12}' --include='*.ipynb' .
grep -rl "$(whoami)" --include='*.ipynb' .
```

**Discussions are not covered by CI.** They were scrubbed by hand once, after a real account ID was found in a thread. Check any long paste before posting.

---

## Not possible via the API

Save the rediscovery:

| Thing | Why |
| --- | --- |
| Creating discussion **categories** | No `createDiscussionCategory` mutation — repo settings only |
| Creating **native polls** | `CreateDiscussionInput` takes only title, body, category. Poll threads here use reactions |
| **Pinning** discussions | No `pinDiscussion` mutation — UI only |
| Setting the **social preview** image | No REST field; the API silently ignores it — Settings → General |
| Creating the **wiki** | No API. The wiki git repo does not exist until the first page is created in the UI |

---

## Release rhythm

No versions — this is teaching material, not a library. Instead:

1. Land the change with CI green
2. Add a `CHANGELOG.md` entry, calling out anything that breaks deep links
3. For anything learner-visible, add a section to the [release notes discussion](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/1)

**Deep links matter more than usual here.** People bookmark specific exercises and modules. Moving a file is a breaking change; say so.

---

## Triage

| Comes in as | Route |
| --- | --- |
| Broken notebook / wrong doc | Issue → fix → note in changelog if learner-visible |
| "AWS changed" | **Highest priority.** Nothing degrades this material faster |
| Question | Q&A. Mark the answer. Add a row to [Community Answers](Community-Answers) |
| Idea | Ideas → [extension board](https://github.com/users/akash-coded/projects/6) if adopted |
| New error | [Error Index](Error-Index); promote to `troubleshooting.md` once seen twice |

---

## Weekly, five minutes

- [ ] `Freshness` workflow result — any link rot?
- [ ] Open issues labelled `aws-update`
- [ ] Unanswered Q&A older than a week
- [ ] Dependabot alerts
- [ ] New discussions missing labels
