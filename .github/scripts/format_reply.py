#!/usr/bin/env python3
"""Turn a `labctl grade --json` report into a Discussions reply.

The reply ends with an invisible ledger line the sync job reads back:
  <!-- lab-ledger {...} -->
Discussions are therefore the source of truth for attempts; the boards and
the scoreboard are derived views.
"""
import json, os, sys
from datetime import datetime, timezone
from pathlib import Path

REPO = "akash-coded/aws-bedrock-agentcore-strands"
RAW = f"https://github.com/{REPO}/blob/main"
TREE = f"https://github.com/{REPO}/tree/main"
lab = os.environ.get("LAB", "?")
learner = os.environ.get("LEARNER", "")
disc = os.environ.get("DISCUSSION_NUMBER", "")
path = Path(sys.argv[1])

def ledger(**kw):
    kw.update(v=1, ts=datetime.now(timezone.utc).isoformat(timespec="seconds"))
    return f"\n\n<!-- lab-ledger {json.dumps(kw, separators=(',', ':'))} -->"

if not path.exists():
    print(f"The grader did not produce a result for **{lab}** — a workflow bug, not yours. "
          f"Please [open an issue](https://github.com/{REPO}/issues/new/choose)."
          + ledger(type="attempt", item=lab, learner=learner, ok=False, passed=0, total=0,
                   kind="unknown", discussion=disc, error="no-report"))
    sys.exit(0)

r = json.loads(path.read_text())
out = []; A = out.append
is_drill = r.get("is_drill")
kind = r.get("kind") or "lab"
p = r.get("phases", {}).get("public", {})
b = r.get("phases", {}).get("break")

passed = p.get("passed", 0); total = p.get("total", 0)
ran = p.get("ran", False)
outcome = "pass" if r.get("ok") else ("partial" if ran and passed > 0 else "fail")

badge = f"`{kind}` · `{r.get('difficulty','')}`" if is_drill else f"lab · `{r.get('difficulty','')}`"
A(f"### {'✅' if outcome == 'pass' else '🔁' if outcome == 'partial' else '❌'} `{r['lab']}` · {r.get('title','')}")
A(f"<sub>{badge}</sub>"); A("")

def phase_block(label, ph):
    if not ph: return
    if not ph.get("ran"):
        A(f"**{label}** — could not run."); 
        if ph.get("error"):
            A(""); A(f"> {ph['error']}")
            d = (ph.get("detail") or "").strip()
            if d: A(""); A("```"); A(d[-600:]); A("```")
        A(""); return
    A(f"**{label} — {ph['passed']}/{ph['total']}**"); A("")
    for c in ph["checks"]:
        A(f"- {'✅' if c['ok'] else '❌'} {c['name']}")
        if not c["ok"]:
            msg = (c.get("message") or "").strip().splitlines()
            if msg: A(f"    <sub>{msg[0][:240]}</sub>")
            if c.get("teaches"): A(f"    <sub>💡 {c['teaches']}</sub>")
    A("")

phase_block("Checks" if is_drill else "Public checks", p)
if b: phase_block("Break phase", b)

# ---- the part that is not a diff: what this means, and where to go ----
fb = r.get("feedback", {}) or {}
block = fb.get(outcome, {})
A("---"); A("")
if block.get("message"):
    A(block["message"]); A("")
if outcome != "pass" and block.get("hint"):
    A(f"**Nudge:** {block['hint']}"); A("")

if outcome == "pass":
    if r.get("skill"):
        A(f"**Skill demonstrated:** {r['skill']}"); A("")
    reads = r.get("reads") or []
    if reads:
        A("**Go deeper:**")
        for rd in reads:
            A(f"- [{rd.get('label', rd.get('path'))}]({RAW}/{rd.get('path','')})")
        A("")
    if r.get("next"):
        nt = r.get("next_title", ""); np_ = r.get("next_path", "")
        A(f"**Next:** `/{'drill' if r.get('next_kind') != 'lab' else 'lab'} {r['next']}` — "
          f"[{nt}]({TREE}/{np_}) " + ("" if r.get("next_kind") != "lab" else "(a full lab — Break phase and hidden checks)"))
        A("")
    if not is_drill:
        A(f"The **hidden checks** did not run here — publishing them would spoil this thread. "
          f"`lab submit {r['lab']}` in a [Codespace](https://codespaces.new/{REPO}?quickstart=1) runs them.")
        A("")
elif outcome == "partial":
    A(f"{passed} of {total} passing. Post the next attempt in this thread — retries are tracked, and a pass after a retry counts more than a first-time pass on the scoreboard.")
    A("")
else:
    A(f"Nothing passed yet, which is fine — the brief is [here]({TREE}/{r.get('path','labs')}) and the nudge above is the one thing to change first.")
    A("")

A(f"<sub>Graded in a network-isolated sandbox · public{' and Break' if b else ''} checks only · "
  f"[how this works]({RAW}/labs/ARENA.md) · [scoreboard]({RAW}/labs/SCOREBOARD.md)</sub>")

print("\n".join(out) + ledger(type="attempt", item=r["lab"], kind=("drill:" + kind) if is_drill else "lab",
                              learner=learner, ok=bool(r.get("ok")), outcome=outcome,
                              passed=passed, total=total, discussion=disc,
                              track=r.get("track"), level=r.get("difficulty")))
