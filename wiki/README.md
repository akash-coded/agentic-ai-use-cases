# Wiki seed

The source for the [repository wiki](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki).

## Why the content is here as well as there

A wiki is a separate git repository with no review and no CI. Keeping the **seed** here means the initial
pages were reviewed, their links are checked by the `Validate` workflow, and the work is not lost if the
wiki is ever reset.

**After seeding, the wiki is the live copy.** These files are not auto-synced, deliberately — a sync job
would overwrite community edits, which are the entire point of a wiki. If you make a large structural
change to a page, edit the wiki and copy it back here.

## What is on the wiki, and why it is not in `docs/`

The rule is: **would being slightly wrong for a week be acceptable?**

| Page | Why it is wiki-shaped |
| --- | --- |
| `Home` · `Where-do-I-find-it` | Navigation across all four surfaces — repo, labs, field guide, discussions. No single surface can own it |
| `Error-Index` | Grows every time somebody hits a new error, with no PR. `docs/setup/troubleshooting.md` is the curated subset |
| `Model-and-Region-Notes` | Availability changes monthly; a versioned file would be wrong within a quarter |
| `Cost-Log` | Community-measured numbers, dated. `docs/setup/cost-controls.md` is the guidance |
| `Community-Answers` | Curated from Discussions as they get answered |
| `Study-Plans` | Calendar-shaped. The repo's learning paths are role-shaped |
| `Maintainer-Runbook` | Operational, not learner-facing |

Nothing here duplicates a repo page. Where the two touch, the wiki links out.

## Seeding or restoring the wiki

The wiki's git repository **does not exist until the first page is created in the web UI** — there is no
API for it, and `git push` to an unseeded wiki fails with `Repository not found`.

1. Open <https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki> and create any page
   (title `Home`, any body). This creates the underlying repository.
2. Then:

```bash
./wiki/sync.sh
```

That force-pushes every page in this directory to the wiki. It is a **seed/restore** operation — it
overwrites the wiki, so do not run it casually once people are editing.

## Conventions

- **Absolute links to the repo.** Wiki pages are not in the repo tree, so relative links break.
- **Wiki-internal links use the page name**: `[Error Index](Error-Index)`.
- `_Sidebar.md` and `_Footer.md` render on every page. Add new pages to the sidebar or they are invisible.
