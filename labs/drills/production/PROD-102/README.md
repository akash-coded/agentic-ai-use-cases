# PROD-102 · Retryable or fatal — and what an unknown error is

`production` · **easy** · `implement` · ~8 min · no AWS account

Retrying a throttle is sensible — capacity comes back. Retrying a malformed request on a second model doubles the latency and the cost to produce the same failure. The classifier decides, and its **default** is the decision that matters.

```python
def classify_error(exc: BaseException) -> str:
    """Return "retryable" or "fatal", by the exception's class name.

    retryable: ThrottlingException, ServiceUnavailableException, TimeoutError,
               ModelTimeoutException, ConnectionError
    fatal:     ValidationException, AccessDeniedException, ResourceNotFoundException
    anything else: decide — and be able to say why.
    """
```

````markdown
/drill PROD-102

```python
def classify_error(exc):
    ...
```
````

## What this proves

That your failover chain retries the things that can succeed on retry, and that you chose the safe default for the error nobody has seen before.
