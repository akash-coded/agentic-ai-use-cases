# Editing this wiki

Anyone with repository access can edit any page — click **Edit** at the top right. No pull request, no review queue. That is the point of a wiki, and it is why only certain things live here.

---

## What belongs here

| ✅ Here | ❌ In the repository |
| --- | --- |
| Things that change monthly ([region notes](Model-and-Region-Notes)) | The curriculum, labs, and field guide |
| Community-contributed data ([cost log](Cost-Log)) | Anything that ships with the code |
| Cross-surface navigation ([where do I find it](Where-do-I-find-it)) | Anything needing review before it is trusted |
| Growing collections ([error index](Error-Index)) | Anything a CI check validates |
| Calendar-shaped guidance ([study plans](Study-Plans)) | The role-based learning paths |

**The test:** *would being slightly wrong for a week be acceptable?* If yes, wiki. If no, it belongs in the repo behind a review.

**Never duplicate a repo page here.** Two copies drift, and the wiki copy is the one people find by search — so the wiki becomes the wrong answer. Link instead. If a repo page is hard to find, that is a job for [Where do I find…?](Where-do-I-find-it), not a copy.

---

## House style

Matching the repository's:

- **Plain and direct.** Say the thing. No throat-clearing.
- **Name the failure mode.** "This breaks when X" beats "be careful".
- **Numbers with denominators.** "87% on a 130-case set" not "very accurate".
- **Absolute links to the repo** — `https://github.com/akash-coded/…/blob/main/…`. Wiki pages are not in the repo tree, so relative links break.
- **Wiki-internal links use the page name**: `[Error Index](Error-Index)`.
- **Date anything volatile.** A region note with no date is a rumour.

---

## Adding to the high-traffic pages

**[Error Index](Error-Index)** — the most valuable page to contribute to.

```markdown
### `the exact error string, including punctuation`
**Cause.** What is actually wrong.
**Fix.** The command or change.
**How you found it.** ← the line people skip and everyone else needs.
```

Paste the exact string. People arrive here from a search engine with an error in their clipboard.

**[Cost Log](Cost-Log)** — add a row after finishing a module. Include whether you tore down the same day; it changes the number more than anything else.

**[Community Answers](Community-Answers)** — when a Q&A thread gets a good answer, add a one-sentence summary that is useful *without clicking through*.

**[Model & Region Notes](Model-and-Region-Notes)** — always with a date and what you actually verified.

---

## Adding a page

Keep it small. A wiki with 40 pages is a wiki nobody reads.

Before adding, check: could this be a section on an existing page? Usually yes.

If you do add one: add it to [`_Sidebar`](_Sidebar) and link it from [Home](Home). An unlinked wiki page does not exist.

---

## Reverting

Every wiki edit is a git commit — see the page history, revert anything. Wikis are lower-stakes than they feel.

## Not sure?

Edit anyway. A wrong edit is visible and fixable; a correction nobody made because they were unsure is neither.

Bigger questions belong in [Discussions](https://github.com/akash-coded/aws-bedrock-agentcore-strands/discussions/categories/general).
