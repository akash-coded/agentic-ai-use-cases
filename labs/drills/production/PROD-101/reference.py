def log_record(response, model_id, primary_id, trace_id):
    usage = (response or {}).get("usage") or {}
    return {"trace_id": trace_id,
            "model_id": model_id,
            "degraded": model_id != primary_id,
            "tokens_in": int(usage.get("inputTokens") or 0),
            "tokens_out": int(usage.get("outputTokens") or 0),
            "stop_reason": (response or {}).get("stopReason") or ""}
