# Runbook · The knowledge base has gone stale

**Severity:** high and silent — the agent answers confidently from withdrawn information.
**First action:** establish how old the index is. That number decides everything else.

---

## 0. How stale? (2 minutes)

| Check | Command / query |
| --- | --- |
| Last successful ingestion | `aws bedrock-agent list-ingestion-jobs --knowledge-base-id KB123 --data-source-id DS123` |
| Newest document in the source | Check S3 `LastModified` on the prefix |
| Gap | source newest − index newest |

| Gap | Severity |
| --- | --- |
| < 1 sync interval | Normal |
| 1–2 intervals | Watch |
| > 2 intervals | **Incident** — the agent may be citing withdrawn policy |

## 1. Decide whether to keep serving

| Question | If yes |
| --- | --- |
| Has the source changed materially since the last sync? | Disable the grounded route; hand off to humans |
| Is the corpus governing (policy, pricing, compliance)? | Stop serving. A wrong policy answer is worse than none |
| Is it advisory (internal search, drafting)? | Keep serving; add a staleness banner |

## 2. Why did the sync stop?

| Cause | Check | Fix |
| --- | --- | --- |
| Ingestion job failing | `list-ingestion-jobs` status + `failureReasons` | Read the reason; usually a permissions or format error |
| Job never scheduled | Is there a trigger at all? | Many teams sync manually once and forget |
| Permissions changed | KB service role has `s3:GetObject`? | Restore |
| Source moved | Prefix or bucket changed | Update the data source |
| Documents rejected | Job succeeded but count is lower than expected | Check unsupported formats and size limits |

> **The most common cause is that nobody scheduled the sync.** A knowledge base does not re-read its
> source on its own.

## 3. Re-sync

```bash
aws bedrock-agent start-ingestion-job \
  --knowledge-base-id KB123 --data-source-id DS123

aws bedrock-agent get-ingestion-job \
  --knowledge-base-id KB123 --data-source-id DS123 --ingestion-job-id JOB123 \
  --query 'ingestionJob.{status:status,stats:statistics}'
```

Check `statistics` — documents scanned versus indexed. A gap means silent rejections.

## 4. Assess the damage

1. Which documents changed since the last good sync?
2. Which answers in that window touched those documents? Filter by trace, if you logged citations
3. Do any need proactive correction?

This is why citations are logged. Without them, the blast radius of a stale index is unknowable.

## 5. Prevent the recurrence

- [ ] **Freshness check in the [quality gate](../../modules/13-agentic-qa-and-evaluation/src/quality_gate.py)**
      — block release when `index_age > 2 × sync_interval`
- [ ] Alert on ingestion job failure, with an owner
- [ ] Alert on index age exceeding threshold
- [ ] Scheduled sync, not manual
- [ ] Corpus ownership named in the [PRD](../../docs/prd/01-discovery-prd.md) — "who owns the policy corpus
      and its update cadence" is a blocking question for a reason

## The post-mortem question

> **How would we have found out if a customer had not told us?**

If the honest answer is "we would not have", the fix is the freshness check, not the sync.

**Related:** [Silent Degradation Watchlist](../frameworks/silent-degradation-watchlist.md) ·
[Grounding Triangle](../frameworks/grounding-triangle.md)
