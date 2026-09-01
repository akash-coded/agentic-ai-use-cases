# Contributing

Corrections, clearer explanations, new exercises and updates for changed AWS behaviour are all welcome.
This is a teaching repository, so the bar is "does this help someone learn", not "is this clever".

## The most valuable contributions

1. **AWS behaviour that changed.** Services move; material goes stale. If a notebook no longer works, or an
   error message is different now, that is the single most useful thing you can report.
2. **An explanation that did not land.** If you got stuck on something the material claims is clear, say so.
   That is a defect in the writing.
3. **A new exercise with its solution.** Exercises are the point. New ones must ship with a worked solution.
4. **A failure mode we missed.** Every [LLD](docs/architecture/lld/) has a failure-modes table. Real
   production failures belong in them.

## Before you open a PR

- [ ] Notebooks run start to finish, or say clearly what they need
- [ ] **No credentials, account IDs or local paths** — see below
- [ ] New exercises include a solution in the module's `solutions/`
- [ ] Links are relative and resolve
- [ ] Module `README.md` updated if you added a file to the sequence

## Scrubbing before you commit

Notebook outputs are committed on purpose — expected output is part of the teaching. But outputs leak.

```bash
grep -rlE '[0-9]{12}' --include='*.ipynb' .          # AWS account ids
grep -rl "$(whoami)" --include='*.ipynb' .           # local paths in tracebacks
grep -rlE 'AKIA[0-9A-Z]{16}' .                       # access keys
```

Account IDs in this repo are the placeholder `123456789012`. Local paths are `/workspace/`.

## Style

- **Write for someone stuck at 11 p.m.** Direct, concrete, no throat-clearing.
- **Name the failure mode.** "This will break when X" is worth more than "be careful".
- **Show the wrong version too.** Most of the value in this repo is in the anti-patterns.
- **No unexplained jargon.** If a term is load-bearing, it belongs in the [glossary](docs/concepts/glossary.md).

## Repo conventions

| Thing | Convention |
| --- | --- |
| Module folders | `NN-kebab-case-topic/` |
| Subfolders | `slides/ notebooks/ exercises/ solutions/ activities/ src/ labs/ guides/ assets/` |
| Solutions | Same filename as the exercise, plus `_SOLUTION` or `Solution_` prefix |
| Client names | Never. This material is deliberately unbranded. |

## Adding a module

Rare, but if it is genuinely a new topic rather than a section of an existing one:

1. `modules/NN-topic/` with the standard subfolders
2. A `README.md` matching the existing shape — objectives, concept table, ordered sequence, recording row, common mistakes, folder map, navigation
3. An LLD at `docs/architecture/lld/NN-topic.md` — mechanism diagram, components, contracts, failure modes, "done when"
4. Rows added to the root `README.md` table and the relevant [learning paths](docs/learning-paths/)

## Questions

Open a [Discussion](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions) rather than an
issue. Issues are for defects — something is broken and a change fixes it. Everything else is a discussion.

[`docs/DISCUSSIONS.md`](docs/DISCUSSIONS.md) covers which category to use, the label taxonomy, and how to
find anything among the 60+ existing threads.
