#!/usr/bin/env python3
"""Reply to a maintainer's /assign with a clear brief for each learner, plus a ledger line."""
import json, os, sys, tomllib
from datetime import datetime, timezone
from pathlib import Path

REPO = "akash-coded/aws-bedrock-agentcore-strands"
TREE = f"https://github.com/{REPO}/tree/main"
a = json.loads(os.environ["ASSIGN_JSON"])
disc = os.environ.get("DISCUSSION_NUMBER", "")

def meta(item):
    for pat in (f"labs/catalog/*/{item}/lab.toml", f"labs/drills/*/{item}/drill.toml"):
        for t in Path(".").glob(pat):
            m = tomllib.loads(t.read_text()); m["_path"] = str(t.parent); m["_drill"] = t.name == "drill.toml"
            return m
    return {"title": item, "_path": "labs", "_drill": False}

out = []; A = out.append
who = " ".join(f"@{l}" for l in a["learners"])
A(f"### 📌 Assigned to {who}")
bits = []
if a.get("session"): bits.append(f"session **{a['session']}**")
if a.get("due"): bits.append(f"due **{a['due']}**")
if bits: A("<sub>" + " · ".join(bits) + f" · set by @{a['by']}</sub>")
A(""); A("| Item | What it is | Time | Submit with |"); A("| --- | --- | --- | --- |")
for it in a["items"]:
    m = meta(it)
    verb = "drill" if m["_drill"] else "lab"
    A(f"| [`{it}`]({TREE}/{m['_path']}) | {m.get('title','')} · `{m.get('difficulty','')}` | ~{m.get('est_minutes','?')} min | `/{verb} {it}` + a ```python block |")
A("")
A("Post each solution as a **comment in this thread** (or the item's own Arena thread). The bot grades it and replies; retries are welcome and tracked — a pass after a retry counts.")
A("")
A(f"<sub>Progress appears on the [Hands-on Tracker](https://github.com/users/akash-coded/projects/9) and in [SCOREBOARD.md](https://github.com/{REPO}/blob/main/labs/SCOREBOARD.md) after the next sync.</sub>")
led = {"v": 1, "type": "assignment", "learners": a["learners"], "items": a["items"],
       "session": a.get("session", ""), "due": a.get("due", ""), "by": a["by"],
       "discussion": disc, "ts": datetime.now(timezone.utc).isoformat(timespec="seconds")}
print("\n".join(out) + f"\n\n<!-- lab-ledger {json.dumps(led, separators=(',', ':'))} -->")
