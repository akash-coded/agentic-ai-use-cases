"""PROD-02 — reference solution.

Retryable errors walk the chain; fatal errors stop it. The answering model is
always reported, because a fallback nobody can see is a quality drop nobody
can attribute.
"""


def invoke_with_failover(request, models: list, classify_error) -> dict:
    attempts = []

    for index, model in enumerate(models or []):
        model_id = model.get("id", f"model-{index}")
        try:
            response = model["call"](request)
        except BaseException as exc:  # noqa: BLE001 - classification decides, not the type
            try:
                kind = classify_error(exc)
            except BaseException:  # noqa: BLE001 - an unclassifiable error is fatal
                kind = "fatal"
            attempts.append({"model_id": model_id, "outcome": kind, "error": f"{type(exc).__name__}: {exc}"})
            if kind == "fatal":
                return {"response": None, "model_id": None, "attempts": attempts,
                        "degraded": False, "failed": True}
            continue

        attempts.append({"model_id": model_id, "outcome": "ok", "error": None})
        return {"response": response, "model_id": model_id, "attempts": attempts,
                "degraded": index > 0, "failed": False}

    return {"response": None, "model_id": None, "attempts": attempts,
            "degraded": False, "failed": True}
