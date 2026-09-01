# Security Policy

## What this repository is

Teaching material: notebooks, decks, exercises and sample code. It is **not** production software and
should not be deployed as-is. IAM policies in the setup docs are deliberately broad for learning, and
[Module 11](modules/11-bedrock-agentcore/) is where you learn to scope them properly.

## Reporting a vulnerability

Use [private security advisories](https://github.com/akash-coded/aws-bedrock-agentcore-strands/security/advisories/new).
Do not open a public issue for a security problem.

## Reporting exposed credentials

If you find a credential, real AWS account ID, key or other secret anywhere in this repository — including
in notebook outputs or git history — **report it privately and immediately**.

This repository is scrubbed: account IDs are the placeholder `123456789012` and local paths are
`/workspace/`. Anything that looks real is a defect worth reporting urgently.

## Your own credentials

- Never commit `.env`, credentials files, or keys. The `.gitignore` blocks the common cases but cannot save
  you from a key pasted into a notebook cell.
- Notebook outputs leak — see [notebook hygiene](docs/setup/local-environment.md#notebook-hygiene-before-committing).
- Use a sandbox AWS account, not production.
- Set a [budget alarm](docs/setup/cost-controls.md) before Module 02.

## Running this material safely

- Every tool in the reference application is read-only by design. Keep it that way while learning.
- Tear down OpenSearch collections and AgentCore runtimes when you finish a module — they cost money for
  existing.
- Treat any agent with write access to a real system as production software, with the review that implies.
