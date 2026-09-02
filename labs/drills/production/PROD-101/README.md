# PROD-101 · Log the field that makes failover visible

`production` · **easy** · `implement` · ~8 min · no AWS account

Failover to a fallback model is the failure most likely to hurt you *while working exactly as designed*: requests succeed, latency is fine, error rate is zero, and answer quality drops for six weeks. One log field prevents that. Write the function that emits it.

```python
def log_record(response: dict, model_id: str, primary_id: str, trace_id: str) -> dict:
    """Build the per-response log record.

    Required keys:
      trace_id      as given
      model_id      the model that ACTUALLY answered
      degraded      True when model_id != primary_id
      tokens_in     response["usage"]["inputTokens"]  (0 if usage is missing)
      tokens_out    response["usage"]["outputTokens"] (0 if missing)
      stop_reason   response["stopReason"]           ("" if missing)
    Never raises on a partial response.
    """
    # TODO
```

````markdown
/drill PROD-101

```python
def log_record(response, model_id, primary_id, trace_id):
    ...
```
````

## What this proves

That you know which single field the silent-degradation watchlist depends on, and that a log function is a boundary — it must survive a malformed response rather than crash the request that produced it.
