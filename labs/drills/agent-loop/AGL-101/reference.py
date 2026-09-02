def answer_text(message: dict) -> str:
    blocks = message.get("content") or []
    parts = [b["text"] for b in blocks if isinstance(b, dict) and isinstance(b.get("text"), str)]
    return " ".join(p.strip() for p in parts if p.strip()).strip()
