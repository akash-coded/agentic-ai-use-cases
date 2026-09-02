#!/usr/bin/env python3
"""Parse a Simulator Arena comment.

Everything untrusted arrives via environment variables (COMMENT_BODY,
COMMENT_AUTHOR, AUTHOR_ASSOCIATION) — never argv, never shell interpolation.

Modes:
  grade   — "/lab ID" or "/drill ID" (either verb works for either kind) + one python fence
  assign  — "/assign @user … ID … [--session "…"] [--due YYYY-MM-DD]"  (maintainers only)

Outputs (GITHUB_OUTPUT): mode, found, lab, reason, assign  (assign is JSON)
"""
import json, os, re, sys
from pathlib import Path

BODY = os.environ.get("COMMENT_BODY", "")
AUTHOR = os.environ.get("COMMENT_AUTHOR", "")
ASSOC = os.environ.get("AUTHOR_ASSOCIATION", "NONE")
OUT = Path(os.environ.get("GITHUB_OUTPUT", "/dev/stdout"))
MAX_BYTES = 20_000
ID_RE = r"[A-Za-z]+-\d+"

def emit(**kw):
    with OUT.open("a") as f:
        for k, v in kw.items():
            f.write(f"{k}={v}\n")

def known_ids():
    ids = set()
    for pat in ("labs/catalog/*/*/lab.toml", "labs/drills/*/*/drill.toml"):
        for t in Path(".").glob(pat):
            ids.add(t.parent.name.upper())
    return ids

KNOWN = known_ids()

# ---------------------------------------------------------------- /assign
m = re.search(r"^/assign\b(.*)$", BODY, re.M)
if m:
    if ASSOC not in ("OWNER", "MEMBER", "COLLABORATOR"):
        emit(mode="assign", found="false", reason="assign-not-allowed"); sys.exit(0)
    rest = m.group(1)
    learners = [x.lower() for x in re.findall(r"@([A-Za-z0-9-]+)", rest)]
    items = [x.upper() for x in re.findall(rf"\b({ID_RE})\b", rest)]
    unknown = [i for i in items if i not in KNOWN]
    sess = re.search(r'--session\s+(?:"([^"]+)"|(\S+))', rest)
    due = re.search(r"--due\s+(\d{4}-\d{2}-\d{2})", rest)
    if not learners:
        emit(mode="assign", found="false", reason="assign-no-learners"); sys.exit(0)
    if not items:
        emit(mode="assign", found="false", reason="assign-no-items"); sys.exit(0)
    if unknown:
        emit(mode="assign", found="false", reason="assign-unknown-items", detail=",".join(unknown)); sys.exit(0)
    payload = {"learners": sorted(set(learners)), "items": list(dict.fromkeys(items)),
               "session": (sess.group(1) or sess.group(2)) if sess else "",
               "due": due.group(1) if due else "", "by": AUTHOR}
    emit(mode="assign", found="true", reason="ok", assign=json.dumps(payload))
    sys.exit(0)

# ---------------------------------------------------------------- /lab | /drill
m = re.search(rf"^/(?:lab|drill)\s+({ID_RE})\s*$", BODY, re.M)
if not m:
    emit(mode="grade", found="false", reason="no-trigger"); sys.exit(0)
lab_id = m.group(1).upper()
if lab_id not in KNOWN:
    emit(mode="grade", found="false", reason="unknown-lab", lab=lab_id); sys.exit(0)

fences = re.findall(r"```(?:python|py)\s*\n(.*?)```", BODY, re.S)
if not fences:
    emit(mode="grade", found="false", reason="no-code", lab=lab_id); sys.exit(0)
if len(fences) > 1:
    emit(mode="grade", found="false", reason="many-fences", lab=lab_id); sys.exit(0)
code = fences[0]
if len(code.encode()) > MAX_BYTES:
    emit(mode="grade", found="false", reason="too-long", lab=lab_id); sys.exit(0)
if not code.strip():
    emit(mode="grade", found="false", reason="empty-code", lab=lab_id); sys.exit(0)

Path("sub").mkdir(exist_ok=True)
Path("sub/solution.py").write_text(code, encoding="utf-8")
emit(mode="grade", found="true", reason="ok", lab=lab_id)
