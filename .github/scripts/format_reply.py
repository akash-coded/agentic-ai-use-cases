#!/usr/bin/env python3
"""Turn a `labctl grade --json` report into a Discussions reply."""
import json
import os
import sys
from pathlib import Path

REPO = "akash-coded/aws-bedrock-agentcore-strands"
report_path = Path(sys.argv[1])
lab = os.environ.get("LAB", "?")

if not report_path.exists():
    print(f"The grader did not produce a result for **{lab}**. "
          f"That is a bug in the workflow, not in your code — "
          f"please [open an issue](https://github.com/{REPO}/issues/new/choose).")
    sys.exit(0)

r = json.loads(report_path.read_text())
out = []
A = out.append

title = r.get("title", "")
A(f"### {'✅' if r.get('ok') else '❌'} `{r['lab']}` · {title}")
A("")

for phase in ("public", "break"):
    p = r.get("phases", {}).get(phase)
    if not p:
        continue
    if not p.get("ran"):
        A(f"**{phase} checks** — could not run.")
        if p.get("error"):
            A("")
            A(f"> {p['error']}")
            detail = (p.get("detail") or "").strip()
            if detail:
                A("")
                A("```")
                A(detail[-800:])
                A("```")
        A("")
        continue

    label = {"public": "Public checks", "break": "Break phase"}[phase]
    A(f"**{label} — {p['passed']}/{p['total']}**")
    A("")
    for c in p["checks"]:
        A(f"- {'✅' if c['ok'] else '❌'} {c['name']}")
        if not c["ok"]:
            msg = (c.get("message") or "").strip().splitlines()
            if msg:
                A(f"    <sub>{msg[0][:300]}</sub>")
            if c.get("teaches"):
                A(f"    <sub>💡 {c['teaches']}</sub>")
    A("")

if r.get("ok"):
    A("---")
    A("")
    A("Both phases pass. Two things worth doing next:")
    A("")
    A(f"1. **The hidden checks.** They are not run here on purpose — publishing them would spoil the lab "
      f"for everyone reading the thread. Run `lab submit {r['lab']}` "
      f"[in a Codespace](https://codespaces.new/{REPO}?quickstart=1) or locally.")
    A(f"2. **Write down the decision.** Every lab's Learn phase asks for one, and they accumulate into "
      f"the [seven PRD artefacts](https://github.com/{REPO}/tree/main/docs/prd).")
else:
    A("---")
    A("")
    A(f"Read the 💡 lines — they are the point of the failing check, not just a diff. "
      f"The [brief](https://github.com/{REPO}/tree/main/labs) and "
      f"`SOLUTION.md` are there when you want them, but try once more first.")

A("")
A(f"<sub>Graded automatically · public and Break phases only · "
  f"[how this works](https://github.com/{REPO}/blob/main/labs/ARENA.md)</sub>")
print("\n".join(out))
