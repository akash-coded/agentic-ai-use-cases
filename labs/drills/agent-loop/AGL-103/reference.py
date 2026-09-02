def call_signature(message):
    calls = []
    for b in (message or {}).get("content", []) or []:
        tu = b.get("toolUse") if isinstance(b, dict) else None
        if tu:
            calls.append((tu.get("name"), tuple(sorted((tu.get("input") or {}).items()))))
    return tuple(sorted(calls))

def is_oscillating(previous, current):
    return bool(current) and current == previous
