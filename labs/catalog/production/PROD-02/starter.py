"""PROD-02 — failover that cannot be silent."""


def invoke_with_failover(request, models: list, classify_error) -> dict:
    """Try models in order, recording which one actually answered."""
    attempts = []

    # TODO 1 — try each model in order; stop at the first success.

    # TODO 2 — record EVERY attempt with its outcome, including the success.

    # TODO 3 — a fatal error stops the chain. Retrying a malformed request on a
    #          second model doubles the cost to produce the same failure.

    # TODO 4 — degraded is True whenever the answering model is not models[0].
    #          This is the field that makes failover observable.

    # TODO 5 — everything failed? Return failed=True. Never raise.

    raise NotImplementedError("implement invoke_with_failover()")
