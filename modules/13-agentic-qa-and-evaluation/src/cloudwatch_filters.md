# CloudWatch reference for TravelMind observability (Topic 3)

A short, copy-paste reference for finding things in agent traces. Every query
runs in **CloudWatch Logs Insights** against the `aws/spans` log group, which is
where AgentCore and Strands OpenTelemetry spans land.

> Read this alongside `debug_walkthrough.ipynb`. The notebook runs these queries
> from Python (`run_insights_query`); this file is the query catalogue.

---

## One-time setup checklist

Spans and traces do not appear until these are in place. Do them once per account
and Region.

1. **Enable Transaction Search.**
   CloudWatch Console -> Application Signals -> Transaction Search -> enable.
   This is the most common reason a fresh account shows empty dashboards.

2. **Instrument the agent.**
   - On AgentCore Runtime: automatic, nothing to do.
   - Outside Runtime (local, Lambda, ECS): add `aws-opentelemetry-distro` to
     `requirements.txt`, then launch with
     `opentelemetry-instrument python -m travelmind_agent`.

3. **Grant least-privilege read.**
   The principal querying needs `logs:StartQuery` and `logs:GetQueryResults` on
   the `aws/spans` log group. Nothing more for read.

---

## Find your real field names first

Field paths in `aws/spans` follow the OpenTelemetry GenAI semantic conventions
and can differ slightly by setup. Before refining a query, look at raw rows:

```
fields @timestamp, @message
| sort @timestamp desc
| limit 5
```

Read the JSON in `@message`, note the exact keys (span name, status, token
fields), then adapt the queries below to match.

---

## Query catalogue

### 1. Recent failed tool spans
The first place to look when an answer was wrong. A tool call with an error status
is often a swallowed failure the agent talked over.

```
fields @timestamp, name, durationNano, status.code
| filter name like /tool/
| filter status.code = "ERROR"
| sort @timestamp desc
| limit 20
```

### 2. Every span for one session (the localisation query)
Pull the full trace for a reported conversation, oldest first, then scan for the
error span.

```
fields @timestamp, name, status.code, durationNano
| filter sessionId = "SESSION_ID_HERE"
| sort @timestamp asc
| limit 100
```

### 3. Slowest spans (latency hunt)
`durationNano` is nanoseconds. Sorting by it surfaces the call that is dragging
p95 latency up.

```
fields @timestamp, name, durationNano
| sort durationNano desc
| limit 20
```

### 4. Token usage per span (cost hunt)
Tokens drive cost. A span burning far more tokens than its peers is a retry or a
runaway loop. Adjust the token field name to match step "find your real field
names" above.

```
fields @timestamp, name, attributes.gen_ai.usage.input_tokens, attributes.gen_ai.usage.output_tokens
| sort attributes.gen_ai.usage.output_tokens desc
| limit 20
```

### 5. Guardrail blocks
A guardrail rejection is a span carrying its action and category. This finds
content that was blocked, which is a safety signal, not an error to silence.

```
fields @timestamp, name, status.code, @message
| filter @message like /guardrail/
| sort @timestamp desc
| limit 20
```

### 6. Error count by session (find the worst conversations)
Roll errors up per session to see which conversations are failing the most.

```
fields sessionId, status.code
| filter status.code = "ERROR"
| stats count(*) as errors by sessionId
| sort errors desc
| limit 20
```

---

## Reading the results

- **A tool span with ERROR plus a normal-looking final model span** is the
  classic swallowed-tool-failure: the tool failed, the model answered anyway.
  Fix by returning tool errors to the model and adding a post-condition check.
- **One span with far more tokens than its siblings** points at a retry or a
  loop. Pair it with query 6 to see if it clusters in particular sessions.
- **Empty results when you expected data** usually means Transaction Search is
  off (step 1) or the field name is wrong (run the raw-rows query first).
