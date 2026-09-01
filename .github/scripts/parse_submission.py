#!/usr/bin/env python3
"""Parse a Discussions submission comment.

Reads the comment body from the COMMENT_BODY environment variable — never from
argv or a shell interpolation, so a comment can never inject into a command.

Emits GitHub Actions outputs: found, lab, reason.
Writes the extracted code to sub/solution.py when found.
"""
import os
import re
import sys
from pathlib import Path

BODY = os.environ.get("COMMENT_BODY", "")
CATALOG = Path("labs/catalog")

OUT = Path(os.environ.get("GITHUB_OUTPUT", "/dev/stdout"))
MAX_BYTES = 20_000


def emit(**kw):
    with OUT.open("a") as f:
        for k, v in kw.items():
            f.write(f"{k}={v}\n")


def fail(reason):
    emit(found="false", reason=reason)
    sys.exit(0)


# 1. the trigger must be explicit — bots that respond to everything are noise
m = re.search(r"^/lab\s+([A-Za-z]+-\d+)\s*$", BODY, re.M)
if not m:
    fail("no-trigger")
lab_id = m.group(1).upper()

# 2. the lab must exist
if not any(p.name == lab_id for p in CATALOG.glob("*/*")):
    fail("unknown-lab")

# 3. exactly one python fence, please
fences = re.findall(r"```(?:python|py)\s*\n(.*?)```", BODY, re.S)
if not fences:
    fail("no-code")
if len(fences) > 1:
    fail("many-fences")

code = fences[0]
if len(code.encode()) > MAX_BYTES:
    fail("too-long")
if not code.strip():
    fail("empty-code")

Path("sub").mkdir(exist_ok=True)
Path("sub/solution.py").write_text(code, encoding="utf-8")
emit(found="true", lab=lab_id, reason="ok")
