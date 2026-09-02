# Enabling the board sync: `PROJECT_TOKEN`

The [Hands-on Tracker](https://github.com/users/akash-coded/projects/9) and
[Repo Pulse](https://github.com/users/akash-coded/projects/10) boards are rebuilt by the
[Pulse workflow](../../.github/workflows/pulse.yml) — but only when a `PROJECT_TOKEN` secret exists.
Everything else (the [scoreboard](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Scoreboard),
`/leaderboard`, `/progress`, the digest) works without it.

## Why a secret is needed at all

The default `GITHUB_TOKEN` cannot read or write Projects v2. And because these boards are **owned by a
user account**, a fine-grained PAT cannot either — fine-grained tokens have no permission for user-owned
Projects ([GitHub community discussion](https://github.com/orgs/community/discussions/156512),
[actions/add-to-project#289](https://github.com/actions/add-to-project/issues/289)). That leaves one
option: a **classic** PAT with the single `project` scope.

A classic `project` scope covers *all* projects on the account, which cannot be narrowed. That is why the
token below has no other scope and a short expiry.

## Steps — about two minutes

**1. Create the token.**
GitHub → *Settings* → *Developer settings* → *Personal access tokens* → **Tokens (classic)** →
*Generate new token (classic)*.

| Field | Value |
| --- | --- |
| Note | `aws-bedrock-agentcore-strands · board sync` |
| Expiration | **90 days** — put the date in a calendar; see *Rotation* below |
| Scopes | **`project` only.** Not `repo`, not `workflow`, nothing else |

Generate, and copy it once — it is not shown again.

**2. Store it as a repository secret.** From a terminal where `gh` is signed in:

```bash
gh secret set PROJECT_TOKEN
```

Paste the token at the prompt. Do **not** pass it with `--body` or on the command line — that puts it in
shell history. (The web equivalent: repository *Settings* → *Secrets and variables* → *Actions* →
*New repository secret*.)

**3. Run the sync.**

```bash
gh workflow run pulse.yml
```

**4. Verify, about a minute later.**

```bash
gh run list --workflow=pulse.yml --limit 1
gh run view --log $(gh run list --workflow=pulse.yml --limit 1 --json databaseId --jq '.[0].databaseId') | grep -E "tracker board|pulse board|PROJECT_TOKEN"
```

You want to see `tracker board: N rows` and `pulse board: N live items`. If you see
`PROJECT_TOKEN not set — skipped`, the secret name is wrong; if you see a permission error, the token is
missing the `project` scope.

## Rotation

When the token expires the workflow **warns and continues** — the scoreboard still publishes, only the
boards stop refreshing, and the run summary carries a warning annotation. Repeat steps 1–2 and the next
scheduled run picks it up. Nothing else needs touching.

## Revoking

Delete the secret (`gh secret delete PROJECT_TOKEN`) and revoke the token in Developer settings. The
workflow returns to scoreboard-only mode on its own.

---

[⬅️ Setup](README.md) · [ARENA.md → Tracking](../../labs/ARENA.md#tracking) ·
[Maintainer Runbook](https://github.com/akash-coded/aws-bedrock-agentcore-strands/wiki/Maintainer-Runbook)
