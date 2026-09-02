def validate_args(schema, args):
    args = args or {}
    props = (schema or {}).get("properties") or {}
    required = (schema or {}).get("required") or []
    unknown = sorted(k for k in args if k not in props)
    missing = sorted(k for k in required if k not in args)
    if not unknown and not missing:
        return {"ok": True}
    valid = ", ".join(sorted(props)) or "(none)"
    parts = []
    if unknown: parts.append(f"unknown argument(s) {', '.join(unknown)}")
    if missing: parts.append(f"missing required {', '.join(missing)}")
    return {"ok": False, "unknown": unknown, "missing": missing,
            "advice": f"{'; '.join(parts)}. Valid arguments are: {valid}. Retry with those names."}
