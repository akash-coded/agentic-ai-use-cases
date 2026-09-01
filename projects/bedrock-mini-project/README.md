# My Bedrock Mini-Project

> **TODO** — replace this section with a one-paragraph problem statement.
> Who is your user? What do they ask? What does success look like?

## Tier reached

- [ ] Core (4 hours)
- [ ] Stretch (+2 hours)
- [ ] Advanced (+2 hours, pick one challenge)

## Template chosen

- [ ] A — Internal Knowledge Assistant
- [ ] B — Customer Support Bot
- [ ] C — Research / Analysis Assistant

## How to run

```bash
# 1) Install dependencies
pip install boto3 python-dotenv

# 2) Set env vars (copy .env.example to .env and fill in your IDs)
cp .env.example .env
# Edit .env

# 3) Run the scripts in order
python scripts/01_hello_bedrock.py
python scripts/02_kb_query.py "your test question"
python scripts/03_app.py
```

## What's in this repo

| File | Purpose |
|---|---|
| `kb_docs/` | The 10-15 markdown documents I wrote for the Knowledge Base |
| `scripts/01_hello_bedrock.py` | Smoke test — confirms Bedrock access works |
| `scripts/02_kb_query.py` | KB-grounded query with guardrail |
| `scripts/03_app.py` | The main app — interactive loop |
| `scripts/tools.py` | (Stretch) tool definitions |
| `scripts/04_dashboard.py` | (Advanced A1) cost dashboard |
| `cost_log.json` | Auto-appended log of every query |
| `reflection.md` | My honest reflection on building this |
| `cost_analysis.xlsx` | Token tracking + monthly cost projection |

## Knowledge Base setup

- **S3 bucket**: `s3://my-kb-bucket/` *(replace with yours)*
- **KB ID**: stored in `.env` (not committed)
- **Embedding model**: Amazon Titan Embed
- **Vector store**: Amazon S3 Vectors

## Guardrail setup

- **Guardrail name**: *(replace)*
- **Filters enabled**:
  - [ ] Content filters (severity: ___)
  - [ ] Denied topics: ___
  - [ ] Word filters
  - [ ] Sensitive information filter
- **Version**: 1

## Test queries I ran

> Document at least 3 queries that *worked* and 1 that the *guardrail blocked*.

1. "Question..." → expected behavior → what happened
2. ...

## What's next

> Once you've completed your chosen tier, list what you'd do if you had another 2 hours.
